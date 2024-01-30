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
    parser.add_argument('--key-file',
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

    key_file = pd.read_csv(args.key_file)

    # create final dataframe that will be added to as we go
    final_dataframe = pd.DataFrame(columns=[all_variables])

    # load in all the source file names

    source_files = [file for file in os.listdir(args.source_files) if file.endswith('.json')]

    for file in source_files:

        subjectkey = keep_all_before_non_alphanumeric(file)

        final_dataframe = add_key_file_info(subjectkey, key_file, file, final_dataframe)

        final_dataframe.to_csv('/n/nrg_l3/Lab/users/dasay/nda/df_test.csv', index=False)



def add_key_file_info(subjectkey, key_file, orig_file, final_dataframe):
    """
    Gather info from the key file for this file
    """

    key_row = key_file.index[key_file['subjectkey'] == subjectkey].tolist()[0]

    final_dataframe['subjectkey'] = subjectkey
    final_dataframe['src_subject_id'] = key_file.at[key_row, 'src_subject_id']
    final_dataframe['interview_date'] = key_file.at[key_row, 'interview_date']
    final_dataframe['interview_age'] = key_file.at[key_row, 'interview_age']
    final_dataframe['sex'] = key_file.at[key_row, 'sex']
    final_dataframe['comments_misc'] = keep_after_first_non_alphanumeric(orig_file)

    return final_dataframe

def keep_all_before_non_alphanumeric(string):
    match = re.search(r'\W', string)
    if match:
        index = match.start()
        return string[:index]
    else:
        return string

def keep_after_first_non_alphanumeric(input_string):
    pattern = r'[^a-zA-Z0-9](.*)$'
    match = re.search(pattern, input_string)
    if match:
        return match.group(1)
    else:
        return input_string





if __name__ == '__main__':
    main()

