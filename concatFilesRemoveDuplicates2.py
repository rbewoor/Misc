'''
#######################################################################################
###
###  Concatenate the input files, remove duplicates and write output file.
###  
###  Use case for Deespeech: combine different vocabulary files.
###
###  NOTE: Uses pandas. 
###
###  Expects exactly 6 Command line arguments (including the script name) for both cases.
###  0)  ScriptName.py
###  1)  Absolute path and name of the output file
###  2)  Log file name with path
###  3)  Absolute path input file (do not specify any files)
###  4)  Space separated Filename or Filenames in double quotes
###  5)  Separator for pandas to use while reading each file.
###
###  Usage example with position numbers indicated:
###                        0                                     1                           2
###  python </script/path/programName.py> </path/for/output/outputFilename.ext> </path/for/logFile/logFileName.log>
###                           3                                        4
###         <write H or NH as Header Indicator> <"space separated individual files in double quotes">
###                           5                                        4
###         <"separator character in double quotes">
###
### example:
### to use WITH header 
### python </script/path/programName.py> </path/for/output/outputFilename.ext> </path/for/logFile/logFileName.log> <H> <"/path/file1.ext /path/file2.ext /path/etc.ext"> <"separator character in double quotes">
### to use WITHOUT header 
### python </script/path/programName.py> </path/for/output/outputFilename.ext> </path/for/logFile/logFileName.log> <NH> <"/path/file1.ext /path/file2.ext /path/etc.ext"> <"separator character in double quotes">
###
#######################################################################################
'''
import pandas as pd
import os
import sys
import logging
#
### ----------------- FUNCTIONs AND CLASS DEFINITIONS START ------------- ###
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
    print(f"ERROR: Including scriptname, expected exactly 6 command line arguments in one of these two formats:")
    print(f'\npython </script/path/programName.py> </path/for/output/outputFilename.ext> </path/for/logFile/logFileName.log> <H> <"/path/file1.ext /path/file2.ext /path/etc.ext"> <"separator character in double quotes">\n')
    print(f"        OR")
    print(f'\npython </script/path/programName.py> </path/for/output/outputFilename.ext> </path/for/logFile/logFileName.log> <NH> <"/path/file1.ext /path/file2.ext /path/etc.ext"> <"separator character in double quotes">\n')
    print(f"\nExiting program with return code = 10\n")
    exit(10)
#
try:
    outFile               = sys.argv[1]
    logFilenameWithPath   = sys.argv[2]
    headerIndicator       = sys.argv[3]
    inFilesCLA            = sys.argv[4]
    separatorChar         = sys.argv[5]
except:
    print(f"\n\nERROR: error assigning the arguments to variables.")
    print(f"Exiting program with return code = 11\n")
    exit(11)
#
## convert the input files from command line format to list, and check each file exists
inFilesList = inFilesCLA.split()
for f in inFilesList:
    if not os.path.isfile(f):
        print(f"\n\nERROR: Input file not found here:\n{f}")
        print(f"Exiting program with return code = 50.\n")
        exit(50)
#
## 
if headerIndicator.lower() not in ['h', 'nh']:
    print(f"\n\nERROR: Invalid input for Header Indicator. Expected either H to say header is present or NH to indicate no header is present.")
    print(f"Exiting program with return code = 53.\n")
    exit(53)
#
## check the separator is only one character long, else pandas will fail later
if len(separatorChar) != 1:
    print(f"\n\nERROR: Invalid input for Separator character for pandas. Expected length of 1, but found length = {len(separatorChar)}")
    print(f"Exiting program with return code = 55.\n")
    exit(55)
#
## https://www.patricksoftwareblog.com/python-logging-tutorial/
logging.basicConfig(level=logging.WARNING, filename=logFilenameWithPath,                                                       \
    filemode='w', format='%(asctime)s : %(message)s')
#
print(f"\nThe command line arguments assigned to variables as follows:\n")
print(f"\t1) Output File: outFile = {outFile}")
print(f"\t2) Log file: logFilenameWithPath = {logFilenameWithPath}")
print(f"\t3) Header Indicator: headerIndicator = {headerIndicator}")
print(f"\t4) Input file as command line arg: inFilesCLA = {inFilesCLA}")
print(f"\t5) Separator character: separatorChar = {separatorChar}")
#
logging.warning(f"\nThe command line arguments assigned to variables as follows:\n")
logging.warning(f"\t1) Output File: outFile = {outFile}")
logging.warning(f"\t2) Log file: logFilenameWithPath = {logFilenameWithPath}")
logging.warning(f"\t3) Header Indicator: headerIndicator = {headerIndicator}")
logging.warning(f"\t4) Input file as command line arg: inFilesCLA = {inFilesCLA}")
logging.warning(f"\t5) Separator character: separatorChar = {separatorChar}")
#
print(f"\n\nProceeding to main logic.\n")
logging.warning(f"\n\nProceeding to main logic.\n")
#
## now main logic starts
#
print(f"\n\n")
logging.warning(f"\n\n")
#
if headerIndicator.lower() == 'h':
    headerInFilesFlag = True
else:
    headerInFilesFlag = False
#
myStr = f"\nGoing to concatenate following files ="
for fileNum, inFile in enumerate(inFilesList):
    myStr += f"\nFile {fileNum + 1} ::: {inFile}"
print(f"{myStr}")
logging.warning(f"{myStr}")
#
dfOut = pd.DataFrame()
print(f"\n\n")
logging.warning(f"\n\n")
#
## make sure to use a separator that is not present in the input data
for fileNum, inFile in enumerate(inFilesList):
    if headerInFilesFlag == True:
        dfIn = pd.read_csv( inFile, sep=separatorChar, header = 0, dtype=str, keep_default_na=False, low_memory=False )
    else:
        dfIn = pd.read_csv( inFile, sep=separatorChar, header = None, dtype=str, keep_default_na=False, low_memory=False )
    #
    myStr = f"File {fileNum + 1} lines before deduplication =\t{len(dfIn)}"
    print(f"{myStr}")
    logging.warning(f"{myStr}")
    dfIn.drop_duplicates( keep='first', inplace=True )
    myStr = f"File {fileNum + 1} lines after deduplication =\t{len(dfIn)}"
    print(f"{myStr}")
    logging.warning(f"{myStr}")
    dfOut = pd.concat([dfOut, dfIn], ignore_index=True)
#
print(f"\nRead in all files, removed duplicates in each, then concatenated contents.\n")
logging.warning(f"\nRead in all files, removed duplicates in each, then concatenated contents.\n")
#
print(f"\nOutput Dataframe: Total lines before deduplication =\t{len(dfOut)}")
logging.warning(f"\nOutput Dataframe: Total lines before deduplication =\t{len(dfOut)}")
#
dfOut.drop_duplicates( keep='first', inplace=True )
if headerInFilesFlag == True:
    dfOut.to_csv(outFile, index=False, header=True)
else:
    dfOut.to_csv(outFile, index=False, header=False)
#
print(f"\nOutput File: Total lines after deduplication =\t{len(dfOut)}")
logging.warning(f"\nOutput File: Total lines after deduplication =\t{len(dfOut)}")
#
print(f"\n\nNormal exit.")
logging.warning(f"\n\nNormal exit.")
#
exit(0)
### -------------------  MAIN LOGIC ENDS HERE   -------------- ###