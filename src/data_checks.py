import argparse
import csv  # Python Standard Library

def check_csv(input_file):
    assert input_file[-3:] == 'csv', 'IO Error: File should have a .csv extension'
    
def check_for_required_columns(file_path, 
                               fields=['CASE_STATUS', 
                                       'WORKSITE_STATE', 
                                       'SOC_CODE', 
                                       'JOB_TITLE']):
    '''
    Checks to make sure input file has the necessary fields
    to perform the data processing.
    
    args:
        file_path <str>: 
            filepath of H1B_FY csv file
        fields <list>: 
            columns required from the input csv to process data
        
    returns:
        True if the fields exist
        
    Example:
        >>> check_for_required_colums('input/H1B_FY_2015.csv')
    '''
    
    with open(file_path) as f:
        readers = csv.reader(f, delimiter=';')
        headers = next(readers)
    
    error_str = (
            'Read Error: Missing required columns ' +
            'from data file. \n\n' +
            'Required fields (column headers) for data processing:\n')
    
    for f in fields: 
        error_str += '\t{}\n'.format(f)
        
    error_str += '\nAvailable fields from {}:\n\n'.format(file_path)
    for i, col in enumerate(headers):
                error_str += '{:50}'.format(col)
                error_str += '\n' if i % 2 or i == 1 else ''
                
    for f in fields:
        assert f in headers, error_str
        
            
                
if __name__ == '__main__':
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input_file", 
                    required=True,
                    help="path to input file. Example: ./input/H1B_FY_2014.csv")
    
    args = vars(ap.parse_args())
    
    check_for_required_columns(args['input_file'])
                 