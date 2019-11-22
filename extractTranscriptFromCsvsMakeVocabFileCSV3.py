'''
#######################################################################################
###  
###  From the CSV input file or files, create a new file as the vocabulary file.
###  
###  NOTE: Input files are assumed to be comma delimited, with the transcript being the third field.
###  
###  Expects exactly 4 Command line arguments (including the script name):
###  0)  ScriptName.py
###  1)  Input files specified in one of the 3 ways shown below in double quotes
###  2)  Absolute path where to save the output vocabulary file
###  3)  Log file name with path
###
###  Usage: There are three ways in which to specify the input files:
###   python /path/to/scriptName.py "/home/data/*.csv" /path/to/output/vocabFilename.txt /path/for/logFile/logFileName.log
###                         OR
###   python /path/to/scriptName.py "/home/data/file1.csv" /path/to/output/vocabFilename.txt /path/for/logFile/logFileName.log
###                         OR
###   python /path/to/scriptName.py "train.csv test.csv" /path/to/output/vocabFilename.txt /path/for/logFile/logFileName.log
###
#######################################################################################
'''
import logging
import csv
import sys
import glob
import pandas as pd
#
### ----------------- FUNCTION DEFINITIONS START ------------- ###
def processEntriesOfOneCSVFile(inFile2PRocess, nRows2Read, nRows2Skip, vocabFile, countLinesReadArr, idxCSVFile):
    '''
    Read in the transcripts from the input CSV file into a dataframe.
    Write it to the vocabFile.
    '''
    #print(f"\nnRowsRead passed to function = {nRows2Read}")
    if nRows2Read == -1:
        # more basic version WITHOUT nrows and skiprows parameters
        #print(f"Reading the ENTIRE CSV file into memory.")
        logging.warning(f"Reading the ENTIRE CSV file into memory.")
        df = pd.read_csv( inFile2PRocess, delimiter=',',                                             \
        header=0, usecols = ["transcript"] )
    else:
        # nrows and skiprows parameters being used
        #print(f"Skipped {nRows2Skip} rows of CSV file.")
        #print(f"\nReading {nRows2Read} rows from CSV file into memory.")
        logging.warning(f"\nReading {nRows2Read} rows from CSV file into memory.")
        logging.warning(f"Skipped {nRows2Skip} rows of CSV file.")
        df = pd.read_csv( inFile2PRocess, delimiter=',', nrows = nRows2Read, skiprows = nRows2Skip,   \
        header=0, usecols = ["transcript"] )
    
    # vocab file should have no header, so appending the data from the file
    df.to_csv(path_or_buf = vocabFile, header = False, mode = 'a', index = None)
    
    countLinesReadArr[idxCSVFile] = df.shape[0]
    print(f"Wrote {countLinesReadArr[idxCSVFile]} data rows to the vocab file.")
    logging.warning(f"Wrote {countLinesReadArr[idxCSVFile]} data rows to the vocab file.")

    return
####
### ----------------- FUNCTION DEFINITIONS  END  ------------- ###

### ------------------- MAIN LOGIC STARTS HERE  -------------- ###
#
print(f"\n\n")
#
#vocabDir = '/home/rohit/dpspTraining/data/wavFiles/commVoiceSet5-1kTotal/vocabDir/'
#vocabFileName = 'vocabulary-Set5First1050.txt'
#vocabDirFullPathWithFileName = vocabDir + vocabFileName
#
## check all the command line arguments and assign variables, 5 expected including scriptname
if len(sys.argv) != 4:
    print(f"\n\nERROR: number of command line arguments entered = {len(sys.argv)}")
    print(f"ERROR: Including scriptname, expected exactly 4 command line arguments in one of these formats:")
    print(f'\npython /path/to/scriptName.py "/home/data/*.csv" /path/to/output/vocabFilename.txt /path/for/logFile/logFileName.log\n')
    print(f'        OR')
    print(f'\npython /path/to/scriptName.py "/home/data/file1.csv" /path/to/output/vocabFilename.txt /path/for/logFile/logFileName.log\n')
    print(f'        OR')
    print(f'\npython /path/to/scriptName.py "train.csv test.csv" /path/to/output/vocabFilename.txt /path/for/logFile/logFileName.log\n')
    print(f"\nExiting program with return code = 10\n")
    exit(10)
#
try:
    inFiles                      = sys.argv[1]
    vocabDirFullPathWithFileName = sys.argv[2]
    logFilePathAndName           = sys.argv[3]
except:
    print(f"\n\nERROR: error assigning the arguments to variables.")
    print(f"Exiting program with return code = 11\n")
    exit(11)
#
## https://www.patricksoftwareblog.com/python-logging-tutorial/
logging.basicConfig(level=logging.WARNING, filename=logFilePathAndName,                                                       \
    filemode='w', format='%(asctime)s : %(message)s')
#
print(f"\nThe command line arguments assigned to variables as follows:\n")
print(f"\t1) Input File or Files: inFiles = {inFiles}")
print(f"\t2) Output vocabulary file: vocabDirFullPathWithFileName = {vocabDirFullPathWithFileName}")
print(f"\t3) Log file: logFilePathAndName = {logFilePathAndName}")
if "*" in inFiles:
    print(f"\tNOTE: ALL CSV files present in input file folder will be treated as input files.")
#
logging.warning(f"\nThe command line arguments assigned to variables as follows:\n")
logging.warning(f"\t1) Input File or Files: inFiles = {inFiles}")
logging.warning(f"\t2) Output vocabulary file: vocabDirFullPathWithFileName = {vocabDirFullPathWithFileName}")
logging.warning(f"\t3) Log file: logFilePathAndName = {logFilePathAndName}")
if "*" in inFiles:
    logging.warning(f"\tNOTE: ALL CSV files present in input file folder will be treated as input files.")
#
print(f"\n\nProceeding to main logic.\n")
logging.warning(f"\n\nProceeding to main logic.\n")
#
if "*" in inFiles:
    inFiles = glob.glob(inFiles)
else:
    inFiles = inFiles.split()
#
if len(inFiles) == 0:
    print(f"\n\nERROR: No CSV files found for processing.")
    print(f"Exiting program with return code = 20.\n")
    exit(20)
#
######### TEMP CODE for testing   --- START
#inFiles = ['C:/Users/DEROBEW/Desktop/rohitTemp/dpspTraining/data/wavFiles/wav33/csvFiles/train33.csv',
#   'C:/Users/DEROBEW/Desktop/rohitTemp/dpspTraining/data/wavFiles/wav33/csvFiles/dev33.csv',
#   'C:/Users/DEROBEW/Desktop/rohitTemp/dpspTraining/data/wavFiles/wav33/csvFiles/test33.csv']
######### TEMP CODE for testing   --- END
#
print("\n### Processing the following transcript files: ###")
for file in inFiles:
    print(f"\t{file}")
logging.warning("\n### Processing the following transcript files: ###")
for file in inFiles:
    logging.warning(f"\t{file}")
#
print(f"\n\n")
logging.warning(f"\n\n")
#
# open and close the vocab file to create it if required and clear any existing contents
with open(vocabDirFullPathWithFileName, 'w') as vocabFile:
    print(f"\nOpened and Closed vocab file.\n")
    logging.warning(f"\nOpened and Closed vocab file.\n")
#
numRows2ReadAtATime4mCSV = -1
numRowsToSkip = 0
countLinesFromCSVArr = [0] * len(inFiles)

for idx, inFile in enumerate(inFiles):
    print(f"\n\nStarting to process CSV file {idx + 1} = \n{inFile}")
    logging.warning(f"\n\nStarting to process CSV file {idx + 1} = \n{inFile}")
    processEntriesOfOneCSVFile(inFile, numRows2ReadAtATime4mCSV, numRowsToSkip, vocabDirFullPathWithFileName, countLinesFromCSVArr, idx)
#
## reload, remove any duplicates and rewrite file.
df = pd.read_csv( vocabDirFullPathWithFileName, sep=',', header = None, low_memory=False )
df.drop_duplicates(keep='first', inplace=True)
df.to_csv(vocabDirFullPathWithFileName, index=False, header = False, mode = 'w')
#
# Print the summary info
#
print(f"\n\n ########## SUMMARY ######### SUMMARY ######### SUMMARY #########\n")
logging.warning(f"\n\n ########## SUMMARY ######### SUMMARY ######### SUMMARY #########\n")
print(f"\nVocabulary output file created here:\n{vocabDirFullPathWithFileName}")
logging.warning(f"\nVocabulary output file created here:\n{vocabDirFullPathWithFileName}")
print(f"\nRead in:")
logging.warning(f"\nRead in:")
for idx, lineCount in enumerate(countLinesFromCSVArr):
    print(f"\tFrom file #number {idx + 1},\t\t{lineCount} transcripts,,\t\tfilename =\n{inFiles[idx]}")
    logging.warning(f"\tFrom file #number {idx + 1},\t\t{lineCount} transcripts,,\t\tfilename =\n{inFiles[idx]}")
print(f"\nTotal transcripts available (WITH duplicates) = {sum(countLinesFromCSVArr)}")
logging.warning(f"\nTotal transcripts available (WITH duplicates) = {sum(countLinesFromCSVArr)}")
print(f"\nTotal transcripts written WITHOUT duplicates in vocab file = {len(df)}")
logging.warning(f"\nTotal transcripts written WITHOUT duplicates in vocab file = {len(df)}")
#
print(f"\n\nNormal exit\n\n")
logging.warning(f"\n\nNormal exit\n\n")
exit(0)