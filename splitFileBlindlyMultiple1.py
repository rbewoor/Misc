'''
#######################################################################################
###
###  Script to split any input file into equal sized output files (except possibly last file).
###  Will ouput necessary number of files in same location as input file.
###  Each output file appended with the row number start to row number end -- wrt data row position in input file.
###     E.g. input file has 1000 rows and the number of rows specified = 300.
###          so here, 4 output files with names as:
###            file_1_300, file_301_600, file_601_900, file_901_1000
###  If header is present, then specify it in the argument, else the first row will be treated as a data row and
###     included in the first file only.
###
###  Expects exactly 5 Command line arguments (including the script name) for both cases.
###
###  0)  ScriptName.py
###  1)  Absolute path and name of the input file
###  2)  Number of rows in each output file
###  3)  Indicate whether Header is present or not: H => Header is present, NH => No header present
###  4)  Log file name with path
###
###  Usage example with position numbers indicated:
###                        0                          1                           2                   3                        4
###  python </script/path/programName.py> <path/with/inputFilename.csv> <rows per output file> <H or NH> </path/for/logFile/logFileName.log>
###
###  example:
###  python </script/path/programName.py> <path/with/inputFilename.csv> 100 <H or NH> </path/for/logFile/logFileName.log>
###
#######################################################################################
'''
import logging
import csv
import sys
import os
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
if len(sys.argv) != 5:
    print(f"\n\nERROR: number of command line arguments entered = {len(sys.argv)}")
    print(f"ERROR: Including scriptname, expected exactly 5 command line arguments in one of these two formats:")
    print(f'\npython </script/path/programName.py> <path/with/inputFilename.csv> 100 <H or NH> </path/for/logFile/logFileName.log>\n')
    print(f"\nExiting program with return code = 10\n")
    exit(10)
#
try:
    inFileWithPath   = sys.argv[1]
    numRowsPerOpFile = sys.argv[2]
    headerIndicator  = sys.argv[3]
    logFileWithPath  = sys.argv[4]
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
## check number of rows required per output file is valid -- current string
try:
    numRowsPerOpFile = int(numRowsPerOpFile)
except:
    print(f"\n\nERROR: Problem with value specified for number of rows per output file.")
    print(f"Exiting program with return code = 52.\n")
    exit(52)
#
## 
if headerIndicator.lower() not in ['h', 'nh']:
    print(f"\n\nERROR: Invalid input for Header presence. Expected either H to say header is present or NH to indicate no header is present.")
    print(f"Exiting program with return code = 53.\n")
    exit(53)
#
## extract the path, only filename and the extension for use later
inFilePath, inFileWithExt = os.path.split(inFileWithPath)
inFilenameOnlyWithoutExt, InFileExt = os.path.splitext(inFileWithExt)
if inFilePath != '':
    inFilePath += r'/'
#
## https://www.patricksoftwareblog.com/python-logging-tutorial/
logging.basicConfig(level=logging.WARNING, filename=logFileWithPath,                                                       \
    filemode='w', format='%(asctime)s : %(message)s')
#
print(f"\nThe command line arguments assigned to variables as follows:\n")
print(f"\t1) Input File: inFile = {inFileWithPath}")
print(f"\t2) Number of rows required per output file = {numRowsPerOpFile}")
print(f"\t3) Header Indicator = {headerIndicator}")
print(f"\t4) Log file: logFileWithPath = {logFileWithPath}")
#
logging.warning(f"\nThe command line arguments assigned to variables as follows:\n")
logging.warning(f"\t1) Input File: inFile = {inFileWithPath}")
logging.warning(f"\t2) Number of rows required per output file = {numRowsPerOpFile}")
logging.warning(f"\t3) Header Indicator = {headerIndicator}")
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
countDataLinesInInputFile = 0
#
## not using pandas read_csv as want to handle any kind of file and separator unknown
with open(inFileWithPath, 'r') as inF:
    for line in inF:
        countDataLinesInInputFile += 1
#
if headerIndicator.lower() == 'h':
    headerPresent = True
    countDataLinesInInputFile -= 1
else:
    headerPresent = False
#
print(f"\nNumber of lines in input file = {countDataLinesInInputFile}\n")
logging.warning(f"\nNumber of lines in input file = {countDataLinesInInputFile}\n")
#
## calculate how many files will be output
if countDataLinesInInputFile % numRowsPerOpFile == 0:
    numOpFilesRequired = int( countDataLinesInInputFile / numRowsPerOpFile)
else:
    numOpFilesRequired = int( countDataLinesInInputFile / numRowsPerOpFile) + 1
print(f"\nNumber of output files required = {numOpFilesRequired}")
logging.warning(f"\nNumber of output files required = {numOpFilesRequired}")
#
## make list of output filenames -- filename, startRowPosition, endRowPosition
opFilenamesAndRowsList = []
for i in range(numOpFilesRequired):
    listValues = []
    startRowPos = int( i * numRowsPerOpFile + 1 )
    if i == numOpFilesRequired - 1:
        ## this is for the last file to be created
        endRowPos = countDataLinesInInputFile
    else:
        endRowPos = int( (i+1) * numRowsPerOpFile )
    listValues.append( inFilePath + inFilenameOnlyWithoutExt + '_' + str(startRowPos) + '_' + str(endRowPos) + InFileExt )
    listValues.append(startRowPos)
    listValues.append(endRowPos)
    opFilenamesAndRowsList.append(listValues)
#
## https://realpython.com/read-write-files-python/
with open(inFileWithPath, 'r') as inF:
    ## save the header if required
    if headerPresent:
        headerLineData = inF.readline()
    for currOpFile, startPos, endPos in opFilenamesAndRowsList:
        with open(currOpFile, 'w') as currOutF:
            if headerPresent:
                currOutF.write( headerLineData )
            for _ in range( endPos - startPos + 1 ):
                currOutF.write( inF.readline() )
        #
    #
#
# Print the summary info
#
myStr = f"\n\n" + f" ########## SUMMARY" * 3 + f" #########\n"
myStr += f"\nInput file  =\n\t{inFileWithPath}\n\nInput file treated as {'WITH HEADER' if headerPresent else 'WITHOUT HEADER'}."
myStr += f"\nNumber of lines in input file = {countDataLinesInInputFile}"
myStr += f"\nNo. of output files = {numOpFilesRequired}"
myStr += f"\n\nOutput Files are:::"
print(f"{myStr}")
logging.warning(f"{myStr}")
for i, (opFile, startPos, endPos) in enumerate(opFilenamesAndRowsList):
    myStr = f"\tFile {i+1} with {endPos - startPos + 1} data rows =  {opFile}"
    print(f"{myStr}")
    logging.warning(f"{myStr}")
#
print(f"\n\nNormal Exit")
logging.warning(f"\n\nNormal Exit")
exit(0)
### -------------------  MAIN LOGIC ENDS HERE   -------------- ###