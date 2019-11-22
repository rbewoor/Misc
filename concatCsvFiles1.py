'''
#######################################################################################
###
###  Script to concatenate CSV files with comamnd line parameters.
###  Can be used to either:
###        a) Combine all CSV files in the specified folder,  OR
###        b) Provide specific names of files which ARE ALL IN SAME input folder
###
###  Expects exactly 5 Command line arguments (including the script name) for both cases.
###
###  Option 1: with STAR to say process all CSV files found as input files.
###  0)  ScriptName.py
###  1)  Absolute path and name of the output file
###  2)  Log file name with path
###  3)  Absolute path input file (do not specify any files)
###  4)  Just the * in double quotes
###
###  Usage example with position numbers indicated:
###                        0                                     1                           2
###  python </script/path/programName.py> </path/for/output/outputFilename.csv> </path/for/logFile/logFileName.log>
###                      3            4
###         <path/for/input/files/> <"*">
###
###  example:
###  python </script/path/programName.py> </path/for/output/outputFilename.csv> </path/for/logFile/logFileName.log> <path/for/input/files/> <"*">
###
###  Option 2: with specific individual input filenames.
###  0)  ScriptName.py
###  1)  Absolute path and name of the output file
###  2)  Log file name with path
###  3)  Absolute path input file (do not specify any files)
###  4)  Space separated Filename or Filenames in double quotes
###
###  Usage example with position numbers indicated:
###                        0                                     1                           2
###  python </script/path/programName.py> </path/for/output/outputFilename.csv> </path/for/logFile/logFileName.log>
###                      3                          4
###         <path/for/input/files/> <"space separated individual files">
###
###  example:
###  python </script/path/programName.py> </path/for/output/outputFilename.csv> </path/for/logFile/logFileName.log> <path/for/input/files/> <"file1.csv file2.csv etc.csv">
###
#######################################################################################
'''
import logging
import csv
import sys
import os
import glob
import pandas as pd
#
### ----------------- FUNCTIONs AND CLASS DEFINITIONS START ------------- ###
####
def getFilesInFolder(_inFilePath):
    ## find all .csv files in folder and return them as a list
    listOfCsvFilesFound = []
    for file in os.listdir(_inFilePath):
        if file.endswith(".csv"):
            listOfCsvFilesFound.append(file)
    return listOfCsvFilesFound
####
def addEachFilesDataToOutputFile(_inFileWithPath, _outFile):
    ## append the data of input file to the output file. The header should already be in output file.
    dfIn =  pd.read_csv( _inFileWithPath, sep=',', header = 0, low_memory=False )
    dfIn.to_csv(_outFile, index=False, header=False, mode='a')
####
### ----------------- FUNCTIONs AND CLASS DEFINITIONS  END  ------------- ###
###
### ------------------- MAIN LOGIC STARTS HERE  -------------- ###
#
print(f"\n\n")
#
## check all the command line arguments and assign variables, 5 expected including scriptname
if len(sys.argv) != 5:
    print(f"\n\nERROR: number of command line arguments entered = {len(sys.argv)}")
    print(f"ERROR: Including scriptname, expected exactly 5 command line arguments in one of these two formats:")
    print(f'\npython </script/path/programName.py> </path/for/output/outputFilename.csv> </path/for/logFile/logFileName.log> <path/for/input/files/> <"*">\n')
    print(f"        OR")
    print(f'\npython </script/path/programName.py> </path/for/output/outputFilename.csv> </path/for/logFile/logFileName.log> <path/for/input/files/> <"file1.csv file2.csv etc.csv">\n')
    print(f"\nExiting program with return code = 10\n")
    exit(10)
#
try:
    outFilePathWithName   = sys.argv[1]
    logFilePathAndName    = sys.argv[2]
    inFilePath            = sys.argv[3]
    inFiles               = sys.argv[4]
except:
    print(f"\n\nERROR: error assigning the arguments to variables.")
    print(f"Exiting program with return code = 11\n")
    exit(11)
#
## add slash at end if not there already
if inFilePath[-1] != '/':
    inFilePath += '/'
#
## check input directory exists
if not os.path.isdir(inFilePath):
    print(f"\n\nERROR: Input files directory not found.")
    print(f"Exiting program with return code = 50.\n")
    exit(50)
#
## https://www.patricksoftwareblog.com/python-logging-tutorial/
logging.basicConfig(level=logging.WARNING, filename=logFilePathAndName,                                                       \
    filemode='w', format='%(asctime)s : %(message)s')
#
print(f"\nThe command line arguments assigned to variables as follows:\n")
print(f"\t1) Output File: outFilePathWithName = {outFilePathWithName}")
print(f"\t2) Log file: logFilePathAndName = {logFilePathAndName}")
print(f"\t3) Input file(s) folder: inFilePath = {inFilePath}")
print(f"\t4) Input Files: inFiles = {inFiles}")
if inFiles == '*':
    print(f"\tNOTE: ALL CSV files present in input file folder will be treated as input files.")
#
logging.warning(f"\nThe command line arguments assigned to variables as follows:\n")
logging.warning(f"\t1) Output File: outFilePathWithName = {outFilePathWithName}")
logging.warning(f"\t2) Log file: logFilePathAndName = {logFilePathAndName}")
logging.warning(f"\t3) Input file(s) folder: inFilePath = {inFilePath}")
logging.warning(f"\t4) Input Files: inFiles = {inFiles}")
if inFiles == '*':
    logging.warning(f"\tNOTE: ALL CSV files present in input file folder will be treated as input files.")
#
print(f"\n\nProceeding to main logic.\n")
logging.warning(f"\n\nProceeding to main logic.\n")
#
## now main logic starts
#
print(f"\n\n")
logging.warning(f"\n\n")
#
## figure out the input files
if inFiles == '*':
    inFiles = getFilesInFolder(inFilePath)
else:
    inFiles = inFiles.split(' ')
#
if len(inFiles) == 0:
    print(f"\n\nERROR: No CSV files found for processing.")
    print(f"Exiting program with return code = 51.\n")
    exit(51)
#
## create outfile with just the header
dfOut = pd.read_csv( inFilePath + inFiles[0], sep=',', header = 0, nrows=0, low_memory=False )
dfOut.to_csv(outFilePathWithName, index=False, header=True)
#
for fileNum, file in enumerate(inFiles):
    addEachFilesDataToOutputFile(inFilePath + file, outFilePathWithName)
    dfOut = pd.read_csv( outFilePathWithName, sep=',', header = 0, low_memory=False )
    print(f"Output File shape after appending file number {fileNum+1} = {dfOut.shape}")
    logging.warning(f"Output File shape after appending file number {fileNum+1} = {dfOut.shape}")
#
# Print the summary info
#
print(f"\n\n ########## SUMMARY ######### SUMMARY ######### SUMMARY #########\n")
print(f"Input File(s) location      = {inFilePath}")
print(f"# Input File(s) processed   = {len(inFiles)}")
print(f"The Input File(s) were      =")
for file in inFiles:
    print(f"\t\t{file}")
print(f"Output File                 =\n{outFilePathWithName}")
print(f"Output File Rows            = {dfOut.shape[0]}")
print(f"Output File Columns         = {dfOut.shape[1]}")
#
logging.warning(f"\n\n ########## SUMMARY ######### SUMMARY ######### SUMMARY #########\n")
logging.warning(f"Input File(s) location      = {inFilePath}")
logging.warning(f"# Input File(s) processed   = {len(inFiles)}")
logging.warning(f"The Input File(s) were      =")
for file in inFiles:
    logging.warning(f"\t\t{file}")
logging.warning(f"Output File                 =\n{outFilePathWithName}")
logging.warning(f"Output File Rows            = {dfOut.shape[0]}")
logging.warning(f"Output File Columns         = {dfOut.shape[1]}")
#
print(f"\n\nNormal Exit")
logging.warning(f"\n\nNormal Exit")
exit(0)
### -------------------  MAIN LOGIC ENDS HERE   -------------- ###