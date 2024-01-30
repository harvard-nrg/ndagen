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
import os

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

    """
    This script will go row by row in building the final csv/dataframe. Every row represents a nifti file that will be uploaded
    """

    nda_config = yaml.safe_load(open(args.nda_config))

    task_list = yaml.safe_load(open(args.task_list))

    all_variables = nda_config['nda_variables']

    tasks = task_list['tasks']

    # create final dataframe that will be added to as we go
    final_dataframe = pd.DataFrame(columns=[all_variables])

    # load in all the source file names

    source_files = [file for file in os.listdir(args.source_files) if file.endswith('.json')]

    for file in source_files:

        print(file)

        sys.exit()

        subjectkey = find_first_non_alphanumeric(file)

        add_key_file_info(args, subjectkey)



def add_key_file_info(args, subjectkey):
    """
    Gather info from the key file for this file
    """
    key_row = args.key_file.index[args.key_file['subjectkey'] == subjectkey[0]].tolist()[0]

    print(key_row)

def find_first_non_alphanumeric(string):
    match = re.search(r'\W', string)
    if match:
        index = match.start()
        return string[:index]
    else:
        return string






if __name__ == '__main__':
    main()

