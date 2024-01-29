#!/usr/bin/env python

import sys
import nibabel as nib
import json
import pandas as pd
from pathlib import Path
from argparse import ArgumentParser
import logging
import yaml
import re
import ndagen.config as config

logger = logging.getLogger('nda_gen')
logging.basicConfig(level=logging.INFO)

def main():
    parser = ArgumentParser()
    parser.add_argument('--source-files', type=Path,
        help='Path to NIFTI Files to be uploaded')
    parser.add_argument('--key-file', type=Path,
        help='Path to subject key csv file')
    parser.add_argument('--nda-config', default=config.spreadsheet_variables(),
        help='YAML file with all the column names for the NDA Spreadsheet')
    parser.add_argument('--task-list', default=config.tasks(),
        help='YAML file of all tasks and their corresponding NDA number')
    args = parser.parse_args()

    nda_config = yaml.safe_load(open(args.nda_config))

    task_list = yaml.safe_load(open(args.task_list))

    all_variables = nda_config['nda_variables']

    tasks = task_list['tasks']

    # create final dataframe that will be added to as we go
    final_dataframe = pd.DataFrame({})

    # load in all the source file names

    source_files = [file for file in os.listdir(args.source_files) if file.endswith('.json')]

    for file in source_files:

        subjectkey = find_first_non_alphanumeric(file)

        print(subjectkey)

        sys.exit()

        add_key_file_info(subjectkey)



    
def find_first_non_alphanumeric(string):
    match = re.search(r'\W', string)
    if match:
        return match.group()
    else:
        return None


def add_key_file_info():
    pass




if __name__ == '__main__':
    main()

