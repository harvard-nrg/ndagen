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
from datetime import datetime

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
    parser.add_argument('--reface-info',
        help='Pass the name of the software used to reface T1w images')
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

    os.chdir(args.source_files)

    ### construct all variables for each row, add each row to final dataframe

    for file in source_files:

        subjectkey = keep_all_before_non_alphanumeric(file)

        current_row = []

        # get column info from the input key file
        current_row = add_key_file_info(subjectkey, key_file, file)

        # add the image info

        current_row = add_image_info(subjectkey, file, current_row, args, tasks)

        print(current_row)

        sys.exit()




        final_dataframe = add_row_to_final_df(subjectkey, current_row, final_dataframe)


    write_dataframe_to_csv(final_dataframe, args)    


def add_key_file_info(subjectkey, key_file, orig_file, current_row=[]):
    """
    Gather info from the key file for this file
    """

    key_row = key_file.index[key_file['subjectkey'] == subjectkey].tolist()[0]

    current_row.append(key_file.at[key_row, 'src_subject_id']) # for src_subject_id column
    current_row.append(validate_date(key_file.at[key_row, 'interview_date'])) # for interview_date column
    current_row.append(key_file.at[key_row, 'interview_age']) # for interview_age column
    current_row.append(key_file.at[key_row, 'sex']) # for sex column
    current_row.append(keep_after_first_non_alphanumeric(orig_file).replace('.json', '')) # for comments_misc column

    return current_row

def add_image_info(subjectkey, file, current_row, args, tasks):
    with open(file) as f:
        json_data = json.load(f)

    current_row.append(file.replace('.json', '.nii.gz')) # for image_file column
    current_row.append('') # for image_thumbnail_file column
    current_row.append(get_image_description(file, args.source_files)) # for image_description column
    current_row.append(get_experiment_id(file, tasks)) # for experiment_id column
    current_row.append(get_scan_type(file, args.source_files)) # for scan_type column
    current_row.append('Live') # for scan_object column
    current_row.append('NIFTI') # for image_file_format column
    current_row.append('') # for data_file2 column
    current_row.append('') # for data_file2_type column
    current_row.append('MRI') # for image_modality column
    current_row.append(json_data['Manufacturer']) # for scanner_manufacturer_pd column
    current_row.append(json_data['ManufacturersModelName']) # for scanner_type_pd column
    current_row.append(json_data['SoftwareVersions']) # for scanner_software_versions_pd column
    current_row.append(json_data['MagneticFieldStrength']) # for magnetic_field_strength column
    current_row.append(json_data['RepetitionTime']) # for mri_repetition_time_pd column
    current_row.append(json_data['EchoTime']) # for mri_echo_time_pd column
    current_row.append(json_data['FlipAngle']) # for flip_angle column
    current_row.append(json_data['AcquisitionMatrixPE']) # for acquisition_matrix column
    current_row.append(get_field_of_view(json_data)) # for mri_field_of_view_pd column
    current_row.append(json_data['PatientPosition']) # for patient_position column
    current_row.append('MONOCHROME2') # for photomet_interpret column
    current_row.append(json_data['ReceiveCoilName']) # for receive_coil column
    current_row.append('Body') # for transmit_coil column
    current_row.append('No') # for transformation_performed column
    current_row.append('') # for transformation_type column
    current_row.append(add_reface_info(json_data, args)) # for image_history column
    current_row.append(get_image_dimensions(file.replace('.json', '.nii.gz'))) # for image_num_dimensions column
    current_row.append(get_image_extent1(file.replace('.json', '.nii.gz'), json_data)) # for image_extent1 column
    current_row.append(get_image_extent2(file.replace('.json', '.nii.gz'), json_data)) # for image_extent2 column
    current_row.append(get_image_extent3(file.replace('.json', '.nii.gz'), json_data)) # for image_extent3 column    
    current_row.append(get_image_extent4(file.replace('.json', '.nii.gz'), json_data)) # for image_extent4 column
    current_row.append('Time')

    return current_row


def validate_date(input_date):
    try:
        parsed_date = datetime.strptime(input_date, '%m/%d/%Y')
        return parsed_date
    except ValueError:
        print('The date on the key file csv is not in valid format. Please change it to MM-DD-YYYY format and try again. Exiting.')
        sys.exit(1)

def get_image_extent4(nifti_file, json_data):
    nifti_img = nib.load(nifti_file)
    dimensions = nifti_img.header.get_data_shape()
    if len(dimensions) > 3:
        return round(dimensions[3] * json_data['RepetitionTime'])
    else:
        return ''    

def get_image_extent3(nifti_file, json_data):
    nifti_img = nib.load(nifti_file)
    dimensions = nifti_img.header.get_data_shape()
    if 'T1' in json_data['SeriesDescription']:
        return round(dimensions[0] * json_data['SliceThickness'])    
    else:
        return round(dimensions[2] * json_data['SliceThickness'])


def get_image_extent2(nifti_file, json_data):
    nifti_img = nib.load(nifti_file)
    dimensions = nifti_img.header.get_data_shape()
    return round(dimensions[1] * json_data['SliceThickness'])


def get_image_extent1(nifti_file, json_data):
    nifti_img = nib.load(nifti_file)
    dimensions = nifti_img.header.get_data_shape()
    if 'T1' in json_data['SeriesDescription']:
        return round(dimensions[2] * json_data['SliceThickness'])
    else:
        return round(dimensions[0] * json_data['SliceThickness'])



def get_image_dimensions(nifti_file):
    nifti_img = nib.load(nifti_file)
    dimensions = nifti_img.header.get_data_shape()
    return len(dimensions)


def add_reface_info(json, args):
    if args.reface_info:
        if 'T1' in json['SeriesDescription']:
            return args.reface_info
    else:
        return ''

def get_field_of_view(json_file):
    dim1 = round((json_file['BaseResolution']) * (json_file['SliceThickness']))
    dim2 = round((json_file['AcquisitionMatrixPE']) * (json_file['SliceThickness']))

    return f'{dim1}x{dim2}'
 

def get_scan_type(json_file, source_files_dir):
    with open(f'{source_files_dir}/{json_file}') as f:
        json_file = json.load(f)

    if 'T2' in json_file['SeriesDescription']:
        return 'MR structural (T2)'
    elif 'T1' in json_file['SeriesDescription'] or 'MPR' in json_file['SeriesDescription']:
        return 'MR structural (T1)'
    elif 'FMAP' in json_file['SeriesDescription']:
        return 'Field Map'
    else:
        return 'fMRI'

def get_experiment_id(file, tasks):
    for task in tasks.keys():
        if task in file:
            return tasks[task]

def get_image_description(json_file, source_files_dir):
    with open(f'{source_files_dir}/{json_file}') as f:
        json_file = json.load(f)

    if 'T2' in json_file['SeriesDescription']:
        return 'MRI_T2'
    elif 'T1' in json_file['SeriesDescription'] or 'MPR' in json_file['SeriesDescription']:
        return 'MRI_T1_MEMPR'
    elif 'FMAP' in json_file['SeriesDescription']:
        return 'MRI_fieldmap'
    else:
        return 'fMRI'


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

def add_row_to_final_df(subject_key, row_data, final_df):

    final_df.loc[subjectkey] = row_data

    return final_df

def write_dataframe_to_csv(final_df, args):
    final_df.to_csv(args.source_files, index=False)



if __name__ == '__main__':
    main()

