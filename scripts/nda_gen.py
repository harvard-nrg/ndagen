#!/usr/bin/env python

import os
import sys
import json
import pandas as pd

# Set the path for source files and key file
source_files_dir = '/ncf/sba10/iCere_full/Data_sharing/NDA_upload_data_sharing/Task_fieldmap_data/All_NIFTI/'
key_file_dir = '/ncf/sba10/iCere_full/Data_sharing/NDA_upload_data_sharing/code/NDA_spreadsheet_subjectkey_230111.csv'

# Get the list of source files
source_files = [file for file in os.listdir(source_files_dir) if file.endswith('.json')]

# Read the key file
key_file = pd.read_csv(key_file_dir)

# Define experiment information
#experiment = ['EPROJ', 'NBACK', 'PAIN', 'FALSBEL', 'LANG', 'MOTOR', 'VISME', 'VODDK', 'REST']
#all_experiment_id = [2337, 2348, 2351, 2350, 2344, 2347, 2352, 2353, 2349]

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

# Create empty lists to store data
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



# Loop through source files
for source_file in source_files:
    # Construct the full path for the source file
    fname = os.path.join(source_files_dir, source_file)
    
    # Open and read JSON file
    with open(fname) as f:
        val = json.load(f)
    
    # Extract data and append to lists
    subjectkey.append(source_file[:12])
    
    # Find the index of the corresponding subjectkey in the key_file DataFrame
    key_row = key_file.index[key_file['subjectkey'] == subjectkey[0]].tolist()[0]
    
    # Append values to respective lists
    src_subject_id.append(key_file.at[key_row, 'src_subject_id'])
    interview_date.append(key_file.at[key_row, 'interview_date'])
    interview_age.append(key_file.at[key_row, 'interview_age'])
    sex.append(key_file.at[key_row, 'sex'])
    comments_misc.append(source_file[13:-5])

    image_file.append(source_file[: -5] + '.nii.gz')
    image_thumbnail_file.append('')
    if 'ANAT_HCPT2' in source_file:
        image_description.append('MRI_T2')
        experiment_id.append(None)
        mri_field_of_view_pd.append('256x240')
        scan_type.append('MR structural (T2)')
        image_extent1.append(256)
        image_extent2.append(240)
        image_extent3.append(166)
    elif 'ANAT' in source_file:
        image_description.append('MRI_T1_MEMPR')
        experiment_id.append(None)
        scan_type.append('MR structural (T1)')
        if '_HCPT1' in source_file:
            mri_field_of_view_pd.append('256x240')
            image_extent1.append(256)
            image_extent2.append(240)
            image_extent3.append(166)
        else:
            mri_field_of_view_pd.append('230x230')
            image_extent1.append(230)
            image_extent2.append(230)
            image_extent3.append(173)  # Adjust based on conditions
    elif 'FMAP' in source_file:
        image_description.append('MRI_fieldmap')
        experiment_id.append(None)
        scan_type.append('Field Map')
        image_extent1.append(round((val['BaseResolution']) * (val['SliceThickness'])))
        image_extent2.append(round((val['AcquisitionMatrixPE']) * (val['SliceThickness'])))
        image_extent3.append(156)
        mri_field_of_view_pd.append(f"{image_extent1[-1]}x{image_extent2[-1]}")
    else:
        image_description.append('fMRI')
        #for i in range(len(experiment)):
        for task_name in tasks.keys():
        	if task_name in source_file:
        		experiment_id.append(tasks[task_name])
        		experiment_description.append(task_name)

        		print(experiment_id)
        		print(experiment_description)
        		sys.exit()
            #if experiment[i] in source_file:
                #experiment_id.append(all_experiment_id[i])
                #experiment_description.append(experiment[i])
        image_num_dimensions.append(4)
        image_extent4.append(422)
        extent4_type.append('Time')
        image_unit4.append('Seconds')
        image_resolution4.append(1)
        STtemp = ', '.join(map(str, val['SliceTiming']))
        slice_timing.append(f"[{STtemp}]")
        scan_type.append('fMRI')
        image_extent1.append(round((val['BaseResolution']) * (val['SliceThickness'])))
        image_extent2.append(round((val['AcquisitionMatrixPE']) * (val['SliceThickness'])))
        image_extent3.append(len(val['SliceTiming']) * (val['SliceThickness']))
        mri_field_of_view_pd.append(f"{image_extent1[-1]}x{image_extent2[-1]}")

    scan_object.append('Live')
    image_file_format.append('NIFTI')
    data_file2.append('')
    data_file2_type.append('')
    image_modality.append('MRI')
    scanner_manufacturer_pd.append('Siemens')
    scanner_type_pd.append('Prisma_fit')
    scanner_software_versions_pd.append('syngo_MR_E11')
    magnetic_field_strength.append(3)
    mri_repetition_time_pd.append(val['RepetitionTime'])
    if 'HCPT1' in source_file:
        mri_echo_time_pd.append('[0.00181,0.00360,0.00539,0.00718]')
        image_history.append('Refaced using NITRC mri_deface_0.3; https://www.nitrc.org/projects/mri_reface')
    elif 'HCPT2' in source_file:
        mri_echo_time_pd.append(str(val['EchoTime']))
        image_history.append('Refaced using NITRC mri_deface_0.3; https://www.nitrc.org/projects/mri_reface')
    elif 'ANAT' in source_file:
        mri_echo_time_pd.append('[0.00157,0.00339,0.00521,0.00703]')
        image_history.append('Refaced using NITRC mri_deface_0.3; https://www.nitrc.org/projects/mri_reface')
    else:
        mri_echo_time_pd.append(str(val['EchoTime']))
        image_history.append('')
    
    flip_angle.append(val['FlipAngle'])
    acquisition_matrix.append(val['BaseResolution'])
    patient_position.append('HFS')
    photomet_interpret.append('MONOCHROME2')
    receive_coil.append(val['ReceiveCoilName'])
    transmit_coil.append('Body')
    transformation_performed.append('No')
    transformation_type.append('')
    
    if 'ANAT' in source_file or 'FMAP' in source_file:
        image_num_dimensions.append(3)
        image_extent4.append(None)
        extent4_type.append('')
        image_unit4.append('')
        image_resolution4.append(None)
        experiment_description.append('')
        slice_timing.append('')
    
    image_extent5.append(None)
    extent5_type.append('')
    image_unit1.append('Millimeters')
    image_unit2.append('Millimeters')
    image_unit3.append('Millimeters')
    image_unit5.append('')
    image_resolution1.append(val['SliceThickness'])  # assuming isovoxel
    image_resolution2.append(image_resolution1[-1])
    image_resolution3.append(image_resolution1[-1])
    image_resolution5.append(None)
    image_slice_thickness.append(val['SliceThickness'])
    
    if 'ANAT' in source_file:
        image_orientation.append('Sagittal')
    else:
        image_orientation.append('Axial')
    
    qc_outcome.append('')
    qc_description.append('')
    qc_fail_quest_reason.append('')
    decay_correction.append('')
    frame_end_times.append('')
    frame_end_unit.append('')
    frame_start_times.append('')
    frame_start_unit.append('')
    pet_isotope.append('')
    pet_tracer.append('')
    time_diff_inject_to_image.append(None)
    time_diff_units.append('')
    
    # Joanna's edits
    pulse_seq.append(val['PulseSequenceDetails'])
    slice_acquisition.append(None)
    software_preproc.append('dcm2niix v1.0.20190902 GCC4.8.2')
    study.append('')
    week.append(None)
    visit.append(source_file[13:19])
    
    # Fix Slice Timing
    bvek_bval_files.append('')
    bvecfile.append('')
    bvalfile.append('')
    deviceserialnumber.append(val['DeviceSerialNumber'])
    procdate.append('')
    visnum.append(None)
    manifest.append('')
    emission_wavelingth.append(None)
    objective_magnification.append(None)
    objective_na.append(None)
    immersion.append(None)
    exposure_time.append(None)
    camera_sn.append('')
    block_number.append(None)
    level.append('')
    cut_thickness.append(None)
    stain.append('')
    stain_details.append('')
    pipeline_stage.append(None)
    deconvolved.append(None)
    decon_software.append('')
    decon_method.append('')
    psf_type.append('')
    psf_file.append('')
    decon_snr.append(None)
    decon_iterations.append(None)
    micro_temmplate_name.append('')
    in_stack.append(None)
    decon_template_name.append('')
    stack.append('')
    slices.append(None)
    slice_number.append(None)
    slice_thickness.append(None)
    type_of_microscopy.append('')
    excitation_wavelength.append(None)
    year_mta.append(None)

# Create a DataFrame
data = pd.DataFrame({
    'subjectkey': subjectkey,
    'src_subject_id': src_subject_id,
    'interview_date': interview_date,
    'interview_age': interview_age,
    'sex': sex,
    'comments_misc': comments_misc,
    'image_file': image_file,
    'image_thumbnail_file': image_thumbnail_file,
    'image_description': image_description,
    'experiment_id': experiment_id,
    'scan_type': scan_type,
    'scan_object': scan_object,
    'image_file_format': image_file_format,
    'data_file2': data_file2,
    'data_file2_type': data_file2_type,
    'image_modality': image_modality,
    'scanner_manufacturer_pd': scanner_manufacturer_pd,
    'scanner_type_pd': scanner_type_pd,
    'scanner_software_versions_pd': scanner_software_versions_pd,
    'magnetic_field_strength': magnetic_field_strength,
    'mri_repetition_time_pd': mri_repetition_time_pd,
    'mri_echo_time_pd': mri_echo_time_pd,
    'flip_angle': flip_angle,
    'acquisition_matrix': acquisition_matrix,
	'mri_field_of_view_pd': mri_field_of_view_pd,
	'patient_position': patient_position,
	'photomet_interpret': photomet_interpret,
	'receive_coil': receive_coil,
	'transmit_coil': transmit_coil,
	'transformation_performed': transformation_performed,
	'transformation_type': transformation_type,
	'image_history': image_history,
	'image_num_dimensions': image_num_dimensions,
    'image_extent1': image_extent1,
    'image_extent2': image_extent2,
    'image_extent3': image_extent3,
    'image_extent4': image_extent4,
    'extent4_type': extent4_type,
    'image_extent5': image_extent5,
    'extent5_type': extent5_type,
    'image_unit1': image_unit1,
    'image_unit2': image_unit2,
    'image_unit3': image_unit3,
    'image_unit4': image_unit4,
    'image_unit5': image_unit5,
    'image_resolution1': image_resolution1,
    'image_resolution2': image_resolution2,
    'image_resolution3': image_resolution3,
    'image_resolution4': image_resolution4,
    'image_slice_thickness': image_slice_thickness,
    'image_orientation': image_orientation,
    'qc_outcome': qc_outcome,
    'qc_description': qc_description,
    'qc_fail_quest_reason': qc_fail_quest_reason,
    'decay_correction': decay_correction,
    'frame_end_times': frame_end_times,
    'frame_end_unit': frame_end_unit,
    'frame_start_times': frame_start_times,
    'frame_start_unit': frame_start_unit,
    'pet_isotope': pet_isotope,
    'pet_tracer': pet_tracer,
    'time_diff_inject_to_image': time_diff_inject_to_image,
    'time_diff_units': time_diff_units,
    'pulse_seq': pulse_seq,
    'slice_acquisition': slice_acquisition,
    'software_preproc': software_preproc,
    'study': study,
    'week': week,
    'experiment_description': experiment_description,
    'visit': visit,
    'slice_timing': slice_timing,
    'bvek_bval_files': bvek_bval_files,
    'bvecfile': bvecfile,
    'bvalfile': bvalfile,
    'deviceserialnumber': deviceserialnumber,
    'procdate': procdate,
    'visnum': visnum,
    'manifest': manifest,
    'emission_wavelingth': emission_wavelingth,
    'objective_magnification': objective_magnification,
    'objective_na': objective_na,
    'immersion': immersion,
    'exposure_time': exposure_time,
    'camera_sn': camera_sn,
    'block_number': block_number,
    'level': level,
    'cut_thickness': cut_thickness,
    'stain': stain,
    'stain_details': stain_details,
    'pipeline_stage': pipeline_stage,
    'deconvolved': deconvolved,
    'decon_software': decon_software,
    'decon_method': decon_method,
    'psf_type': psf_type,
    'psf_file': psf_file,
    'decon_snr': decon_snr,
    'decon_iterations': decon_iterations,
    'micro_temmplate_name': micro_temmplate_name,
    'in_stack': in_stack,
    'decon_template_name': decon_template_name,
    'stack': stack,
    'slices': slices,
    'slice_number': slice_number,
    'slice_thickness': slice_thickness,
    'type_of_microscopy': type_of_microscopy,
    'excitation_wavelength': excitation_wavelength,
    'year_mta': year_mta
})


# Write DataFrame to CSV file
data.to_csv('/n/nrg_l3/Lab/users/dasay/nda/test.csv', index=False)
