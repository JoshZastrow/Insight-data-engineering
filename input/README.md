# Your Input Data

The `run.sh` shell script processes an input file stored as `./input/h1b_input.csv`. If you would like to use the `run.sh` command,
please have the data formatted to meet the following conditions:

- The file name is `h1b_input.csv`, stored in the top `input` folder.
- The file contains the following column headers 
  - CASE_STATUS
  - JOB_TITLE
  - WORKSITE_STATE
  - SOC_CODE
  - WORKSITE_STATE
  
If you are processing 2014 or older data, try running the following script from the command line:

`$ python ./src/process.py  -i ./input/h1b_input.csv -o ./output -y 2014`
