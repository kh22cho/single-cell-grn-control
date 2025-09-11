# import modules

import pandas as pd
import os
import shutil
import tempfile
import subprocess
import json

# netctrl file path
netctrl = '/home/Program/netctrl/build/src/ui/netctrl'

# make inferred-GRN file name dictionary
file_name = {}
basic_path = "../.."

for i in range(1, 5):
    file_name[f'phase{i}'] = os.listdir(basic_path + f"/data/inferred_grn/phase{i}/")

# result dictionary
netctrl_results = {}

# edge cutting for loop
for i in range(1, 5):
    # phase key in result dictionary
    phase_key = f'phase{i}'
    netctrl_results[phase_key] = {}

    for n in file_name[f'phase{i}']:
        # network name key in phase key
        network_key = n
        netctrl_results[phase_key][network_key] = {}

        # ncol file path
        input_file = os.path.join(f'{basic_path}/data/inferred_grn/', phase_key, n)

        # number of lines of original file
        wc_output = subprocess.check_output(['wc', '-l', input_file], text=True)
        num_lines = int(wc_output.split()[0])  # the first line is a number of lines 

        # make temp directory
        temp_dir = tempfile.mkdtemp(prefix="network_edges_")

        # read original file
        with open(input_file, 'r') as f:
            lines = f.readlines()

        # make a new network file with edge removal
        for l in range(len(lines)):
            output_file = os.path.join(temp_dir, f"{l+1}.ncol")
            with open(output_file, 'w') as f:
                for j, line in enumerate(lines):
                    if j != l:
                        f.write(line)
            
            # netctrl result value
            command = f"{netctrl} -m liu {output_file} | wc -l"
            netctrl_output = subprocess.check_output(command, shell=True, text=True).strip()

            # save result
            netctrl_results[phase_key][network_key][l+1] = int(netctrl_output)  # format; edge number : netctrl result

        # remove a temp directory
        shutil.rmtree(temp_dir)

# save final result into JSON format
output_json_path = f"{basic_path}/data/result/netctrl_results_liu.json"
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(netctrl_results, json_file, ensure_ascii=False, indent=4)
