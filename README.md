# Table of Contents
1. [Problem](README.md#problem)
2. [Input Dataset](README.md#input-dataset)
3. [Approach](README.md#Approach)
4. [Run](README.md#Run)

# Problem

A newspaper editor was researching immigration data trends on H1B(H-1B, H-1B1, E-3) visa application processing over the past years, trying to identify the occupations and states with the most number of approved H1B visas. She has found statistics available from the US Department of Labor and its [Office of Foreign Labor Certification Performance Data](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis). But while there are ready-made reports for [2018](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2018/H-1B_Selected_Statistics_FY2018_Q4.pdf) and [2017](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2017/H-1B_Selected_Statistics_FY2017.pdf), the site doesn’t have them for past years. 

This repo functions as a data pipeline to analyze past years data, specificially calculate two metrics: **Top 10 Occupations** and **Top 10 States** for **certified** visa applications.

# Input Dataset

Raw data could be found [here](https://www.foreignlaborcert.doleta.gov/performancedata.cfm) under the __Disclosure Data__ tab (i.e., files listed in the __Disclosure File__ column with ".xlsx" extension). 
There are converted Excel files into a semicolon separated (";") format placed  into this Google drive [folder](https://drive.google.com/drive/folders/1Nti6ClUfibsXSQw5PUIWfVGSIrpuwyxf?usp=sharing). 

# Run

- Clone this repository: `$ git clone` and navigate to the top folder `$ cd`
- Save the `.csv` file you want processed in the `./input` folder, renaming the file to `h1b_input.csv`.
- run the .sh script `$ sh run.sh`

**NOTE:** If you are running the script on immigration data from 2014 or earlier, modify the `./run.sh` script to specify the year:
```
python ./src/data_checks.py -i ./input/h1b_input.csv
python ./src/process.py  -i ./input/h1b_input.csv -o ./output -y 2014
```

Alternatively, you can call the process command from the terminal:

`$ python .src/process.py -i ./input/h1b_input.csv -o ./output -y 2014`

This allows you to specify the input file path and output folder. see `python .src/process.py --help` for more details.

**Directory before running script**

```
      ├── README.md 
      ├── run.sh
      ├── src
      │   └──h1b_counting.py
      ├── input
      │   └──h1b_input.csv
      ├── output
 ```
 **Directory after running script** 
 ```
      ├── README.md 
      ├── run.sh
      ├── src
      │   └──h1b_counting.py
      ├── input
      │   └──h1b_input.csv
      ├── output
      |   └── top_10_occupations.txt
      |   └── top_10_states.txt
 ```
 

# Approach 

The input data gets processed through two functions: `data_checks.py` and `process.py` located in the `\src` directory. The `data_checks.py` makes sure the columns needed in `process.py` exist. 

The `process.py` module reads in the CSV line by line, checks the `CASE_STATUS` field for `CERTIFIED` visas, then increments the counts in a dictionary that contains the states and a dictionary that contains the SOC codes. The equivalent `Job Title` label is stored in a dictionary according to the `SOC Codes`, but was not used as the `key-value` pair because there were a few typos and multiple job names for a given SOC Code. 

The dictionary is then processed into a list containing tuples of the desired output, namely:
      - OCCUPATION / STATE
      - NUMBER CERTIFIED APPLICATIONS
      - PERCENTAGE

The list is sorted using Python's built in [Timsort](https://en.wikipedia.org/wiki/Timsort) by `NUMBER CERTIFIED APPLICATIONS` then equivalent `OCCUPATION / STATE` label. This sorted list is filter for the top 10 rows if there are more than 10 rows.

The resulting output is written to the output file specified in the bash command, which can be found in `./run.sh`. The function will overwrite the output files if they already exist.

NOTE: Data from 2014 and earlier contain different column names -- the function `get_top_10_occupations_and_states` in `process.py` is able to process these column names, but they will not pass `data_checks.py`. 

## Repo directory structure

The directory structure for your repo should look like this:
```
      ├── README.md 
      ├── run.sh
      ├── src
      │   └──h1b_counting.py
      ├── input
      │   └──h1b_input.csv
      ├── output
      |   └── top_10_occupations.txt
      |   └── top_10_states.txt
      ├── insight_testsuite
          └── run_tests.sh
          └── tests
              └── test_1
              |   ├── input
              |   │   └── h1b_input.csv
              |   |__ output
              |   |   └── top_10_occupations.txt
              |   |   └── top_10_states.txt
              ├── your-own-test_1
                  ├── input
                  │   └── h1b_input.csv
                  |── output
                  |   |   └── top_10_occupations.txt
                  |   |   └── top_10_states.txt
```

