#!/bin/bash
#
# Use this shell script to compile (if necessary) your code and then execute it. Below is an example of what might be found in this file if your program was written in Python
#
python ./src/data_checks.py -i ./input/h1b_input.csv
python ./src/process.py  -i ./input/h1b_input.csv -o ./output