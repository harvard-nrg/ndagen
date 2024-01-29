#!/usr/bin/env python

import sys
import nibabel as nib
import json
import pandas as pd
from pathlib import Path
from argparse import ArgumentParser
import logging
import re

logger = logging.getLogger('nda_gen')
logging.basicConfig(level=logging.INFO)

def main():
    parser = ArgumentParser()
    parser.add_argument('--source-files', type=Path,
        help='Path to NIFTI Files to be uploaded')
    parser.add_argument('--key-file', type=Path,
        help='Path to subject key csv file')
    args = parser.parse_args()

    tasks = {
    'EPROJ': 2337,
    'NBACK': 2348,
    'PAIN': 2351,
    'FALSBEL': 2350,
    'LANG': 2344,
    'MOTOR': 2347,
    'VISME': 2352,
    'VODDK': 2353,
    'REST': 2349
    }

    master_list = [
    'subjectkey',
    'src_subject_id',
    'interview_date',
    'interview_age',
    'sex',
    'comments_misc',
    'image_file',
    'image_thumbnail_file',
    'scan_object',
    'image_file_format',
    'experiment_id',
    'image_description',
    'mri_field_of_view_pd',
    'scan_type',
    'data_file2',
    'data_file2_type',
    'image_extent1',
    'image_extent2',
    'image_extent3',
    'image_extent4',
    'extent4_type',
    'image_extent5',
    'extent5_type',
    'image_unit1,'
    'image_unit2',
    'image_unit3',
    'image_unit4',
    'image_unit5',
    'image_resolution1',
    'image_resolution2',
    'image_resolution3',
    'image_resolution4',
    'image_slice_thickness',
    'image_orientation',
    'image_num_dimensions',
    'qc_outcome',
    'qc_description',
    'qc_fail_quest_reason',
    'decay_correction',
    'frame_end_times',
    'frame_end_unit',
    'frame_start_times',
    'frame_start_unit',
    'pet_isotope',
    'pet_tracer',
    'time_diff_inject_to_image',
    'time_diff_units',
    'pulse_seq',
    'slice_acquisition',
    'software_preproc',
    'study',
    'week',
    'experiment_description',
    'visit',
    'slice_timing',
    'bvek_bval_files',
    'bvecfile',
    'bvalfile',
    'deviceserialnumber',
    'procdate',
    'visnum',
    'manifest',
    'emission_wavelingth',
    'objective_magnification',
    'objective_na',
    'immersion',
    'exposure_time',
    'camera_sn',
    'block_number',
    'level',
    'cut_thickness',
    'stain',
    'stain_details',
    'pipeline_stage',
    'deconvolved',
    'decon_software',
    'decon_method',
    'psf_type',
    'psf_file',
    'decon_snr',
    'decon_iterations',
    'micro_temmplate_name',
    'in_stack',
    'decon_template_name',
    'stack',
    'slices',
    'slice_number',
    'slice_thickness',
    'type_of_microscopy',
    'excitation_wavelength',
    'year_mta',
    'image_modality',
    'scanner_manufacturer_pd',
    'scanner_type_pd'
    'scanner_software_versions_pd',
    'magnetic_field_strength',
    'mri_repetition_time_pd',
    'mri_echo_time_pd',
    'flip_angle',
    'acquisition_matrix',
    'patient_position',
    'photomet_interpret',
    'receive_coil',
    'transmit_coil',
    'transformation_performed',
    'transformation_type',
    'image_history'
    ]


    subjectkey, src_subject_id, interview_date, interview_age, sex = ([] for _ in range(5))
    comments_misc, image_file, image_thumbnail_file, scan_object, image_file_format = ([] for _ in range(5))
    experiment_id, image_description, mri_field_of_view_pd, scan_type, data_file2, data_file2_type = ([] for _ in range(6))
    image_extent1, image_extent2, image_extent3 = ([] for _ in range(3))
    image_extent4, extent4_type, image_extent5, extent5_type = ([] for _ in range(4))
    image_unit1, image_unit2, image_unit3, image_unit4, image_unit5 = ([] for _ in range(5))
    image_resolution1, image_resolution2, image_resolution3, image_resolution4, image_resolution5 = ([] for _ in range(5))
    image_slice_thickness, image_orientation, image_num_dimensions = ([] for _ in range(3))
    qc_outcome, qc_description, qc_fail_quest_reason, decay_correction, frame_end_times = ([] for _ in range(5))
    frame_end_unit, frame_start_times, frame_start_unit, pet_isotope, pet_tracer = ([] for _ in range(5))
    time_diff_inject_to_image, time_diff_units, pulse_seq, slice_acquisition = ([] for _ in range(4))
    software_preproc, study, week, experiment_description, visit = ([] for _ in range(5))
    slice_timing, bvek_bval_files, bvecfile, bvalfile, deviceserialnumber = ([] for _ in range(5))
    procdate, visnum, manifest, emission_wavelingth, objective_magnification = ([] for _ in range(5))
    objective_na, immersion, exposure_time, camera_sn, block_number = ([] for _ in range(5))
    level, cut_thickness, stain, stain_details, pipeline_stage = ([] for _ in range(5))
    deconvolved, decon_software, decon_method, psf_type, psf_file = ([] for _ in range(5))
    decon_snr, decon_iterations, micro_temmplate_name, in_stack, decon_template_name = ([] for _ in range(5))
    stack, slices, slice_number, slice_thickness, type_of_microscopy = ([] for _ in range(5))
    excitation_wavelength, year_mta, image_modality, scanner_manufacturer_pd, scanner_type_pd = ([] for _ in range(5))
    scanner_software_versions_pd, magnetic_field_strength, mri_repetition_time_pd, mri_echo_time_pd, flip_angle = ([] for _ in range(5))
    acquisition_matrix, patient_position, photomet_interpret, receive_coil, transmit_coil, transformation_performed = ([] for _ in range(6))
    transformation_type, image_history = ([] for _ in range(2))

    # create final dataframe that will be added to as we go
    final_dataframe = pd.DataFrame({})

    # load in all the source file names

    source_files = [file for file in os.listdir(args.source_files) if file.endswith('.json')]

    for file in source_files:

        subjectkey = get_subject_key(source_files)

        add_key_file_info(subjectkey)

    

def get_subject_key(args):

    
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

