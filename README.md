# ndagen

Ndagen is a python command line tool to generate the spreadsheet necessary for uploading data to the NIMH Data Archive (NDA)

# USAGE

nda_gen.py [-h] --source-files SOURCE_FILES --key-file KEY_FILE [--nda-config NDA_CONFIG] [--task-list TASK_LIST]
                  [--reface-info REFACE_INFO] [--echo-times ECHO_TIMES]

options:
  -h, --help            show this help message and exit

  --source-files SOURCE_FILES
                        Path to NIFTI Files to be uploaded

  --key-file KEY_FILE   Path to subject key csv file

  --nda-config NDA_CONFIG
                        YAML file with all the column names for the NDA Spreadsheet

  --task-list TASK_LIST
                        YAML file of all tasks and their corresponding NDA number

  --reface-info REFACE_INFO
                        Pass the name of the software used to reface T1w images
                        
  --echo-times ECHO_TIMES
                        Path to YAML file with series descriptions and associated echo times

# Documenation

Check out the user docs here: https://ndagen.readthedocs.io/en/latest/index.html