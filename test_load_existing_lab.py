import ruamel.yaml as yaml
import pprint
import re
from pathlib import Path


def reformat_yaml_txt(file):
# Open and read Text file
    with open(file, "r+") as txt_file:
        disp_data = txt_file.readlines()
        # print()
        # pprint.pprint(disp_data)
        # print()
        # print(disp_data[0])
        # print(type(disp_data[0]))
        # print(type(disp_data))
        # print(type(disp_data))
        # print(len(disp_data))

        disp_data_new = []

        counter = 0

        for line in disp_data:
            if 'nodes' in line or 'links' in line:
                # print(line)
                # print(type(line))
                # print("-" in line)
                line = line.replace('-', '')
                # print(line)
            elif 'ceos' in line and 'eth' not in line:
                # print(line)
                # print(type(line))
                # print("-" in line)
                line = line.replace('-', '')
                # print(line)
            disp_data_new.append(line)
            counter += 1


    # Reopening the file with "W" flag instead of "R" so we avoid using Truncate file so ew dont get the Byte error
    with open("dynamic_topology.txt", "w") as txt_file:
        pass
        txt_file.writelines(disp_data_new)

    # pprint.pprint(disp_data_new)

    p = Path("dynamic_topology.txt")
    p.rename(p.with_suffix('.yml'))

reformat_yaml_txt("dynamic_topology.txt")