'''
#######################################################################################
###
###  Script to split on input CSV file as per input Ratio for Train: Dev: Test.
###  Ratio to split can be specified in two ways:
###        a) Type of ratio Flag=N: Numbers of rows required for each output file
###           (values MUST sum number of data rows of input)
###                                       OR
###        b) Type of ratio Flag=P: percentage values specified
###           (values MUST sum to exactly 100.0)
###
###  Flag to Shuffle or not before the splitting: S for Shuffle OR NS for NoShuffle
###
###  Output three CSV files. Input Filename appended with _TRAIN.csv _DEV.csv and _TEST.csv
###  Location of output files as input file location.
###
###  Expects exactly 6 Command line arguments (including the script name) for both cases.
###
###  Option 1: with Flag = 1 and absolute number of data rows specified for each output file.
###  NOTE: Values MUST total the number of data rows of input, else will FAIL.
###  0)  ScriptName.py
###  1)  Absolute path and name of the input file
###  2)  Type of ratio Flag = N
###  3)  Numbers specified as "three integers for TRAIN DEV TEST, space separated, in double quotes"
###  4)  Log file name with path
###  5)  Shuffle Flag either as <S> or <NS>
###
###  Usage example with position numbers indicated:
###                        0                          1                  2                 3
###  python </script/path/programName.py> <path/with/inputFilename.csv> <N> <"intTrain intDev intTest">
###                        4                        5
###         </path/for/logFile/logFileName.log> <S or NS>
###
###  example:
###  python </script/path/programName.py> <path/with/inputFilename.csv> <N> <"35 18 7"> </path/for/logFile/logFileName.log> <S or NS>
###
###  Option 2: with Flag = P and absolute number of data rows specified for each output file.
###  NOTE: Values MUST total to exactly 100.0, else will FAIL.
###  0)  ScriptName.py
###  1)  Absolute path and name of the input file
###  2)  Type of ratio Flag = P
###  3)  Percentages specified as "three floats for TRAIN DEV TEST, space separated, in double quotes"
###  4)  Log file name with path
###
###  Usage example with position numbers indicated:
###                        0                          1                  2                 3
###  python </script/path/programName.py> <path/with/inputFilename.csv> <P> <"floatTrain floatDev floatTest">
###                        4                        5
###         </path/for/logFile/logFileName.log> <S or NS>
###
###  example:
###  python </script/path/programName.py> <path/with/inputFilename.csv> <P> <"65.0 25.0 10.0"> </path/for/logFile/logFileName.log>  <S or NS>
###
#######################################################################################
'''
import logging
import csv
import sys
import os
import pandas as pd
#
### ----------------- FUNCTIONs AND CLASS DEFINITIONS START ------------- ###
####
def checkRatioValues(_ratioFlag, _inRatioStr, _extractedRatioList, _lenInputData):
    ## check the ratio values are consistent with the type of flag.
    ##       Extract values as integers or floats into the list and return with RC = 0 and no error message.
    ##       If any problem, return with non-zero RC and appropriate error message.
    try:
        _extractedRatioList = _inRatioStr.split()
        if len(_extractedRatioList) != 3 :
            return 10, _extractedRatioList, f"Expected 3 space separated values, but found {len(_extractedRatioList)} values."
        #
        ## there are three values, so far ok. Now process for percentage and numbers.
        #
        if _ratioFlag.lower() == 'n' :
            ## its numbers
            _extractedRatioList = [int(ele) for ele in _extractedRatioList]
            sum = 0
            for ele in _extractedRatioList :
                sum += ele
            if sum != _lenInputData :
                return 15, _extractedRatioList, f"Sum of Ratios = {sum}, and does not match length of input data = {_lenInputData}."
        else:
            ## its percentages
            _extractedRatioList = [float(ele) for ele in _extractedRatioList]
            sum = 0.0
            for ele in _extractedRatioList :
                sum += ele
            if sum != 100.0 :
                return 20, _extractedRatioList, f"Sum of Ratios = {sum}, and does not match the value of 100.0."

    except:
        return -1, _extractedRatioList, f"Unexpected error while processing the Ratio values."   
    #
    ## all good if it reaches here. List already populated with appropriate values. so return 0 with no error message.
    return 0, _extractedRatioList, ""
####
def getFileNameWithoutExtension(_inFileWithPath):
    ## get the filename from the input string.
    try:
        lastSlashPos = _inFileWithPath.rfind('/')
        lastDotPos   = _inFileWithPath.rfind('.')
        if lastSlashPos != -1 and lastDotPos != -1 and lastSlashPos < lastDotPos :
            ## path with filename with extension
            _fileNameWithoutExtension = _inFileWithPath[ lastSlashPos +1 : lastDotPos ]
        elif lastSlashPos == -1 and lastDotPos != -1 :
            ## no path, only filename with extension
            _fileNameWithoutExtension = _inFileWithPath[ 0 : lastDotPos ]
        elif lastSlashPos != -1 and lastDotPos == -1 :
            ## path with filename without extension
            _fileNameWithoutExtension = _inFileWithPath[ lastSlashPos +1 :  ]
        elif lastSlashPos == -1 and lastDotPos == -1 :
            ## no path, no extension
            _fileNameWithoutExtension = _inFileWithPath
        else:
            ## unknown issue
            _fileNameWithoutExtension = None
    except:
        _fileNameWithoutExtension = None
    #
    return _fileNameWithoutExtension
####
### ----------------- FUNCTIONs AND CLASS DEFINITIONS  END  ------------- ###
###
### ------------------- MAIN LOGIC STARTS HERE  -------------- ###
#
print(f"\n\n")
#
## check all the command line arguments and assign variables, 5 expected including scriptname
if len(sys.argv) != 6:
    print(f"\n\nERROR: number of command line arguments entered = {len(sys.argv)}")
    print(f"ERROR: Including scriptname, expected exactly 5 command line arguments in one of these two formats:")
    print(f'\npython </script/path/programName.py> <path/with/inputFilename.csv> <N> <"35 18 7"> </path/for/logFile/logFileName.log> <S or NS>\n')
    print(f"        OR")
    print(f'\npython </script/path/programName.py> <path/with/inputFilename.csv> <P> <"65.0 25.0 10.0"> </path/for/logFile/logFileName.log>  <S or NS>\n')
    print(f"\nExiting program with return code = 10\n")
    exit(10)
#
try:
    inFileWithPath   = sys.argv[1]
    ratioFlag        = sys.argv[2]
    inRatioStr       = sys.argv[3]
    logFileWithPath  = sys.argv[4]
    shuffleFlag      = sys.argv[5]
except:
    print(f"\n\nERROR: error assigning the arguments to variables.")
    print(f"Exiting program with return code = 11\n")
    exit(11)
#
## check input file exists
if not os.path.isfile(inFileWithPath):
    print(f"\n\nERROR: Input file not found here:\n{inFileWithPath}")
    print(f"Exiting program with return code = 50.\n")
    exit(50)
#
## check valid input for ratio split flag
if ratioFlag.lower() not in ['p', 'n']:
    print(f"\n\nERROR: Invalid Flag input for Split Ratio. Expected single character of P (for percentage) or N (for numbers).")
    print(f"Exiting program with return code = 51.\n")
    exit(51)
#
## check valid input for shuffle flag
if shuffleFlag.lower() not in ['s', 'ns']:
    print(f"\n\nERROR: Invalid Flag for Shuffle option. Expected single character of S (for shuffle) or NS (for no shuffle).")
    print(f"Exiting program with return code = 52.\n")
    exit(52)
#
## extract the filename only without extension
fileNameWithoutExtension = getFileNameWithoutExtension(inFileWithPath)
if fileNameWithoutExtension is None:
    print(f"\n\nERROR: Unable to get only the filename without extension from the input data.")
    print(f"Exiting program with return code = 53.\n")
    exit(53)
#
## https://www.patricksoftwareblog.com/python-logging-tutorial/
logging.basicConfig(level=logging.WARNING, filename=logFileWithPath,                                                       \
    filemode='w', format='%(asctime)s : %(message)s')
#
print(f"\nThe command line arguments assigned to variables as follows:\n")
print(f"\t1) Input File: inFile = {inFileWithPath}")
print(f"\t2) Ratio type Flag (P for percentage , N for number): ratioFlag = {ratioFlag}")
print(f"\t3) String input for Ratio values: inRatioStr = {inRatioStr}")
print(f"\t4) Log file: logFileWithPath = {logFileWithPath}")
#
logging.warning(f"\nThe command line arguments assigned to variables as follows:\n")
logging.warning(f"\t1) Input File: inFile = {inFileWithPath}")
logging.warning(f"\t2) Ratio type Flag (P for percentage , N for number): ratioFlag = {ratioFlag}")
logging.warning(f"\t3) String input for Ratio values: inRatioStr = {inRatioStr}")
logging.warning(f"\t4) Log file: logFileWithPath = {logFileWithPath}")
#
print(f"\n\nProceeding to main logic.\n")
logging.warning(f"\n\nProceeding to main logic.\n")
#
## now main logic starts
#
print(f"\n")
logging.warning(f"\n")
#
## read data from input file
dfIn = pd.read_csv( inFileWithPath, sep=',', header = 0, low_memory=False )
lenDfIn = len(dfIn)
#
## verify the ratio values specified are correct, and put into the list if so.
extractedRatioList = []
checkRatioValues_RC, extractedRatioList, checkRatioValues_errorMsg = checkRatioValues( ratioFlag, inRatioStr, extractedRatioList, lenDfIn)
## the check function returns with RC = 0 if all ok, else non-zero RC
if checkRatioValues_RC != 0:
    print(f"\nERROR: Inconsistent ratio values specified.")
    print(f"\nFor flag type P, enter three floats totalling to exactly 100.0.")
    print(f"\nFor flag tpye N, enter three integers totalling the number of data rows in input file.")
    print(f"\nError message from function: {checkRatioValues_errorMsg}\nReturn code from function = {checkRatioValues_RC}")
    print(f"\nExiting program with return code = 60.\n")
    exit(60)
else:
    print(f"\nAll ok with checkRatioValues function call.\nextractedRatioList = {extractedRatioList}")
    logging.warning(f"\nAll ok with checkRatioValues function call.\nextractedRatioList = {extractedRatioList}")
#
## convert input numbers (or percents) to derived percents (or numbers)
if ratioFlag.lower() == 'n':
    extractedRatioListNumbers = extractedRatioList.copy()
    extractedRatioListPercents = [round(ele*100.0/lenDfIn, 2) for ele in extractedRatioListNumbers]
    extractedRatioListPercents[2] = round(100.00 - extractedRatioListPercents[0] - extractedRatioListPercents[1], 2)
else:
    extractedRatioListPercents = extractedRatioList.copy() 
    extractedRatioListNumbers = [int(ele*lenDfIn/100.0) for ele in extractedRatioListPercents]
    extractedRatioListNumbers[2] = lenDfIn - extractedRatioListNumbers[0] - extractedRatioListNumbers[1]
#
## check if there is too little input data
if 0 in extractedRatioListNumbers :
    print(f"\nERROR: Too few input data rows to split as desired or zero specified.")
    print(f"\nValue for the split numbers = {extractedRatioListNumbers}")
    print(f"\nExiting program with return code = 70.\n")
    exit(70)
#
## shuffle input, create the dataframes for TRAIN, DEV and TEST and write to output files
if shuffleFlag.lower() == 's':
    dfIn = dfIn.sample(frac = 1)
    dfIn.reset_index(drop=True, inplace=True)
#
## split the input dataframe and write csv files
dfTrain = dfIn.loc[ 0 : extractedRatioListNumbers[0] - 1 ]
dfDev   = dfIn.loc[ extractedRatioListNumbers[0] : extractedRatioListNumbers[0] + extractedRatioListNumbers[1] - 1 ]
dfTest  = dfIn.loc[ extractedRatioListNumbers[0] + extractedRatioListNumbers[1] : ]
dfTrain.to_csv(inFileWithPath + '_TRAIN.csv', index=False)
dfDev.to_csv(inFileWithPath + '_DEV.csv', index=False)
dfTest.to_csv(inFileWithPath + '_TEST.csv', index=False)
#
# Print the summary info
#
print(f"\n\n ########## SUMMARY ######### SUMMARY ######### SUMMARY #########\n")
print(f"Input file  =\n\t{inFileWithPath}\n")
if ratioFlag.lower() == 'p':
    print(f"Split request based on Percentage.")
    print(f"Percentages used = {extractedRatioListPercents}")
    print(f"Percents mapped to Numbers used = {extractedRatioListNumbers}")
else:
    print(f"Split request based on Number.")
    print(f"Numbers used = {extractedRatioListNumbers}")
    print(f"Numbers as Percents = {extractedRatioListPercents}")
print(f"\nInput data {'WAS' if shuffleFlag.lower() == 's' else 'WAS NOT'} shuffled before splitting.")
print(f"\n# Data rows in input file = {dfIn.shape[0]}\n")
print(f"\n# Data rows in TRAIN file = {dfTrain.shape[0]}")
print(f"# Data rows in DEV   file = {dfDev.shape[0]}")
print(f"# Data rows in TEST  file = {dfTest.shape[0]}")
print(f"\nTRAIN file  =\n\t{inFileWithPath + '_TRAIN.csv'}")
print(f"DEV   file  =\n\t{inFileWithPath + '_DEV.csv'}")
print(f"TEST  file  =\n\t{inFileWithPath + '_TEST.csv'}")
#
logging.warning(f"\n\n ########## SUMMARY ######### SUMMARY ######### SUMMARY #########\n")
logging.warning(f"Input file  =\n\t{inFileWithPath}\n")
if ratioFlag.lower() == 'p':
    logging.warning(f"Split request based on Percentage.")
    logging.warning(f"Percentages used = {extractedRatioListPercents}")
    logging.warning(f"Percents mapped to Numbers used = {extractedRatioListNumbers}")
else:
    logging.warning(f"Split request based on Number.")
    logging.warning(f"Numbers used = {extractedRatioListNumbers}")
    logging.warning(f"Numbers as Percents = {extractedRatioListPercents}")
logging.warning(f"\nInput data {'WAS' if shuffleFlag.lower() == 's' else 'WAS NOT'} shuffled before splitting.")
logging.warning(f"\n# Data rows in input file = {dfIn.shape[0]}\n")
logging.warning(f"\n# Data rows in TRAIN file = {dfTrain.shape[0]}")
logging.warning(f"# Data rows in DEV   file = {dfDev.shape[0]}")
logging.warning(f"# Data rows in TEST  file = {dfTest.shape[0]}")
logging.warning(f"\nTRAIN file  =\n\t{inFileWithPath + '_TRAIN.csv'}")
logging.warning(f"DEV   file  =\n\t{inFileWithPath + '_DEV.csv'}")
logging.warning(f"TEST  file  =\n\t{inFileWithPath + '_TEST.csv'}")
#
print(f"\n\nNormal Exit")
logging.warning(f"\n\nNormal Exit")
exit(0)
### -------------------  MAIN LOGIC ENDS HERE   -------------- ###