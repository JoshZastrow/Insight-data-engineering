import csv
from operator import itemgetter
import os
import argparse
import sys
from __future__ import print_function

def get_top_10_occupations_and_states(input_file, output_path, year=2019):
    '''
    Calculates the top 10 occupations and top 10 states that have received
    certified H1B visas. Writes the total count of certified visas per
    occupation and per state, as well as the percentage compared to total
    visas, to .txt files in the /output folder.
    
    Performs the following functions:
        1) reads in CSV file
        2) filters rows where STATUS is CERTIFIED
        3) counts the number of CERTIFIED rows for all SOC codes and States
        3) calculates the percentage of certified rows
        4) filters for the top 10 highest counts 
        5) Replaces the SOC code with the equivalent job title
        6) writes results to .txt file in the output folder
    
    
    NOTE: In cases where there are multiple job titles (LCA_CASE_JOB_TITLE) 
    for a given SOC code, this function stores the first job title seen.
    
    
    args:
        input_file <str>: 
            file path of CSV containing H1B data
        output_path <str>: 
            directory path to store the following files:
                - top_10_occupations.txt
                - top_10_states.txt
        
    returns:
        None
        
    '''
    
    print(sys.version)
    assert input_file[-4:] == '.csv', 'IO Error: Input File should be in .csv format'
    assert os.path.exists(input_file), 'Cannot find {}'.format(input_file)
    assert os.path.isdir(output_path), ('{} not found. Cannot write output.'.format(output_path))
    
    # Establish variables
    label_name = {}
    top_rows = 10
    counts = [{}, {}]  # Stores dictionary of count each occupation and state
    
    # Year 2014 has different column names -- quick fix for now
    if year <= 2014:
        STATUS = 'STATUS'
        labels = ['LCA_CASE_JOB_TITLE', 'LCA_CASE_EMPLOYER_STATE']
        items  = ['LCA_CASE_SOC_CODE', 'LCA_CASE_EMPLOYER_STATE']
    else:
        STATUS = 'CASE_STATUS'
        labels = ['JOB_TITLE', 'WORKSITE_STATE']
        items  = ['SOC_CODE', 'WORKSITE_STATE']
        
    fnames = ['top_10_occupations.txt', 'top_10_states.txt']
    col_id = ['TOP_OCCUPATIONS', 'TOP_STATES']
    total_certified = 0
    
    # Read in csv file
    with open(input_file) as f:
        readers = csv.DictReader(f, delimiter=';')

        for row in readers:
            # Skip uncertified entries
            if row[STATUS] != 'CERTIFIED':
                for k,v in row.items():
                    if k in ['CASE_STATUS', 'JOB_TITLE', 'WORKSITE_STATE']:
                        print(v)
                        print('; ')
                print()
                continue
            
            total_certified += 1

            for k,v in row.items():
                if k in ['CASE_STATUS', 'JOB_TITLE', 'WORKSITE_STATE']:
                    print(v, end='; ')
            print()           
            # Count occurences of SOC Codes and State
            for count, data, lbl in zip(counts, items, labels):
                item = row[data]
                
                if item in count:
                    count[item] += 1
                else:
                    count[item] = 1
                    label_name[item] = row[lbl]
    print('total certified:', total_certified)
    print('length of stored counts: {} occ, {} states'.format(len(counts[0]), len(counts[1])))
    # Convert dictionary of counts into list
    for count, fname, id in zip(counts, fnames, col_id):
        
        results = [None] * len(count.keys())
        for i, item in enumerate(count.keys()):

            # Retrieve metrics
            NAME = label_name[item]
            NUMBER_CERTIFIED = count[item]
            PERCENTAGES = round(count[item] / total_certified * 100,1)
            
            row_result = (NAME, NUMBER_CERTIFIED, '{:0.2f}%'.format(PERCENTAGES))
            results[i] = row_result

        # Sort list by count, name
        results = sorted(results, key=itemgetter(1,0), reverse=True)

        print('Original length of result: {}'.format(len(results)))
        # Filter for top results
        if len(results) > top_rows:
            results = results[:top_rows]
        print('top length of results:', len(results))
        # Write
        with open(os.path.join(output_path, fname), 'w') as f:
            output = csv.writer(f, delimiter=';')
            output.writerow([id, 'NUMBER_CERTIFIED_APPLICATIONS','PERCENTAGE'])
            for row_data in results:
                output.writerow(row_data)
                
if __name__ == '__main__':
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input_file", 
                    required=True,
                    help="path to input file. Example: ./input/H1B_FY_2014.csv")
    ap.add_argument("-o", "--output_folder", 
                    required=True,
                    help="path to output folder")
    ap.add_argument("-y", "--year", 
                    required=False,
                    help="2014 dataset has different column names. If processing" + 
                   " data from 2014, set this equal to 2014")
    args = vars(ap.parse_args())
    
    if not args['year']: args['year'] = 2019
    get_top_10_occupations_and_states(args['input_file'], 
                                      args['output_folder'],
                                      args['year'])