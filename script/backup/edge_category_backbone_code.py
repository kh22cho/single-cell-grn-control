#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# %% [markdown]
"""
# LIU 모델 Edge Category 추출 (GML + JSON)

- 목적: 각 phase 폴더의 `.ncol` 네트워크를 `netctrl`로 분석하여,
  - GML 파일을 저장하고,
  - GML에서 `edgeclass`(critical/ordinary/redundant)와 노드 이름을 파싱해
  - JSON 사전 구조로 저장합니다: `dic[phase][network][category] = [[src, tgt], ...]`
- 전제: `netctrl` 바이너리가 설치되어 있고, LIU 모델을 사용할 수 있어야 합니다.
- 경로 전제: 이 노트북은 `script/04_find_critical_edge` 디렉토리에서 실행한다고 가정합니다.

출력 위치
- GML: `../../data/result/gml/{phase}/{network}.gml`
- JSON: `../../data/result/edge_classes_liu.json`
"""

# %%
from pathlib import Path
import os, re, json, subprocess

# netctrl 바이너리 자동 탐지 (기본 경로 우선)
DEFAULT_NETCTRL = '/home/Program/netctrl/build/src/ui/netctrl'
NETCTRL_BIN = DEFAULT_NETCTRL if os.path.exists(DEFAULT_NETCTRL) else 'netctrl'
print('Using netctrl:', NETCTRL_BIN)

# 이 노트북이 위치한 디렉토리 기준으로 상위 경로 계산
# script/04_find_critical_edge/test.ipynb 에서 실행한다고 가정하면,
# Path.cwd().parents[2] -> 프로젝트 루트(single-cell-grn-control)
NOTEBOOK_DIR = Path.cwd()
BASE_DIR = NOTEBOOK_DIR.parents[2]
INFERRED_DIR = BASE_DIR / 'data' / 'inferred_grn'
RESULT_DIR = BASE_DIR / 'data' / 'result'
GML_ROOT = RESULT_DIR / 'gml'
RESULT_JSON = RESULT_DIR / 'edge_classes_liu.json'

print('BASE_DIR     =', BASE_DIR)
print('INFERRED_DIR =', INFERRED_DIR)
print('RESULT_DIR   =', RESULT_DIR)
print('GML_ROOT     =', GML_ROOT)
print('RESULT_JSON  =', RESULT_JSON)

# %% [markdown]
"""
## 유틸 함수 (GML 생성 및 파싱)
- `run_netctrl_to_gml`: `.ncol` 입력을 받아 netctrl로 GML 생성
- `parse_gml_edge_classes`: GML 파일을 읽어 `edgeclass`와 노드 이름을 추출하여 카테고리별 엣지 목록 생성

참고: GML에는 `edge_class`가 아닌 `edgeclass`로 저장됩니다.
"""

# %%
# netctrl 실행: .ncol -> .gml 생성
def run_netctrl_to_gml(ncol_path: Path, gml_path: Path):
    gml_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [str(NETCTRL_BIN), '-m', 'liu', '-M', 'graph', '-F', 'gml', '-o', str(gml_path), str(ncol_path)]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f'netctrl failed ({res.returncode}) for {ncol_path}\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}')

# GML 파싱: edgeclass + 노드 이름 추출
NAME_RE = re.compile(r'^name\s+\"(.*)\"\s*$')
EDGECLASS_RE = re.compile(r'^edgeclass\s+\"(.*)\"\s*$')

def parse_gml_edge_classes(gml_path: Path):
    id_to_name = {}
    categories = { 'critical': [], 'ordinary': [], 'redundant': [] }

    in_node = False
    in_edge = False
    node_id = None
    node_name = None
    src = None
    tgt = None
    cls = None

    def commit_node():
        if node_id is not None:
            id_to_name[str(node_id)] = node_name if node_name is not None else str(node_id)

    def commit_edge():
        if src is None or tgt is None:
            return
        edge_class = (cls or '').lower()
        if edge_class not in categories:
            return
        s = id_to_name.get(str(src), str(src))
        t = id_to_name.get(str(tgt), str(tgt))
        categories[edge_class].append([s, t])

    with open(gml_path, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            # 블록 시작
            if line.startswith('node') and not in_node and not in_edge:
                in_node = True
                node_id = None
                node_name = None
                continue
            if line.startswith('edge') and not in_edge and not in_node:
                in_edge = True
                src = None
                tgt = None
                cls = None
                continue

            # 블록 종료
            if line == ']':
                if in_node:
                    commit_node()
                    in_node = False
                    node_id = None
                    node_name = None
                    continue
                if in_edge:
                    commit_edge()
                    in_edge = False
                    src = None
                    tgt = None
                    cls = None
                    continue

            # node 블록 내부
            if in_node:
                if line.startswith('id '):
                    try:
                        node_id = int(line.split()[1])
                    except Exception:
                        pass
                    continue
                m = NAME_RE.match(line)
                if m:
                    node_name = m.group(1)
                    continue

            # edge 블록 내부
            if in_edge:
                if line.startswith('source '):
                    try:
                        src = int(line.split()[1])
                    except Exception:
                        pass
                    continue
                if line.startswith('target '):
                    try:
                        tgt = int(line.split()[1])
                    except Exception:
                        pass
                    continue
                m = EDGECLASS_RE.match(line)
                if m:
                    cls = m.group(1)
                    continue

    return categories

# %% [markdown]
"""
## 대상 phase / 네트워크 선택 (옵션)
- `PHASE_FILTER`를 비워두면 `phase*` 전부 처리
- `NETWORK_LIMIT`를 설정하면 각 phase에서 앞 N개만 처리
"""

# %%
# 선택 옵션
PHASE_FILTER = []  # 예: ['phase4'] 또는 [] 전체
NETWORK_LIMIT = None  # 예: 5 또는 None

# 출력 디렉토리 생성
RESULT_DIR.mkdir(parents=True, exist_ok=True)
GML_ROOT.mkdir(parents=True, exist_ok=True)

# 입력 폴더 존재 검증
assert INFERRED_DIR.exists(), f'입력 폴더가 없습니다: {INFERRED_DIR}'

# %% [markdown]
"""
## 실행: GML 생성 및 JSON 누적
- 각 네트워크별 요약을 화면에 출력합니다.
"""

# %%
result = {}

# phase 디렉토리 순회
phase_dirs = sorted([p for p in INFERRED_DIR.iterdir() if p.is_dir() and p.name.startswith('phase')])
for phase_dir in phase_dirs:
    phase = phase_dir.name
    if PHASE_FILTER and phase not in PHASE_FILTER:
        continue
    result.setdefault(phase, {})

    # .ncol 네트워크 파일 순회
    ncols = sorted(phase_dir.glob('*.ncol'))
    if NETWORK_LIMIT is not None:
        ncols = ncols[:NETWORK_LIMIT]

    for ncol_path in ncols:
        network_name = ncol_path.stem
        gml_dir = GML_ROOT / phase
        gml_path = gml_dir / f'{network_name}.gml'

        # 1) netctrl 실행하여 GML 생성
        run_netctrl_to_gml(ncol_path, gml_path)

        # 2) GML 파싱하여 카테고리별 엣지 목록 추출
        categories = parse_gml_edge_classes(gml_path)
        result[phase][network_name] = categories

        c = categories
        print(f"{phase}/{network_name}: critical={len(c['critical'])}, ordinary={len(c['ordinary'])}, redundant={len(c['redundant'])}")

# %% [markdown]
"""
## JSON 저장 및 샘플 확인
"""

# %%
with open(RESULT_JSON, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print('Saved JSON to', RESULT_JSON)
# 샘플로 첫 phase/네트워크 키 출력
if result:
    p0 = sorted(result.keys())[0]
    n0 = sorted(result[p0].keys())[0] if result[p0] else None
    print('Sample keys:', p0, '->', n0)
    if n0:
        print('Sample categories counts:', {k: len(v) for k,v in result[p0][n0].items()})

