'''
#######################################################################################
###  
###  From the Deepspeech CSV input file or files, create the alphabet file. As usual expected
###       to have the three columns with the third column being the transcripts.
###  Will process the contents of this third column.
###  
###  NOTE: Input files are assumed to be comma delimited, with the transcript being the third field.
###
###  It reads the text in the data and stores a set of unique characters as the alphabet file.
###  
###  Expects exactly 4 Command line arguments (including the script name):
###  0)  ScriptName.py
###  1)  Input files specified in one of the 3 ways shown below in double quotes
###  2)  Absolute path where to save the output alphabet file
###  3)  Log file name with path
###
###  Usage: There are three ways in which to specify the input files:
###   python /path/to/scriptName.py "/home/data/*.csv" /path/to/output/alphabetFilename.txt /path/for/logFile/logFileName.log
###                         OR
###   python /path/to/scriptName.py "/home/data/file1.csv" /path/to/output/alphabetFilename.txt /path/for/logFile/logFileName.log
###                         OR
###   python /path/to/scriptName.py "train.csv test.csv" /path/to/output/alphabetFilename.txt /path/for/logFile/logFileName.log
###
#######################################################################################
'''
#
import logging
import csv
import sys
import glob
#
### ----------------- FUNCTION DEFINITIONS START ------------- ###
####
### ----------------- FUNCTION DEFINITIONS  END  ------------- ###
#
### ------------------- MAIN LOGIC STARTS HERE  -------------- ###
#
print(f"\n\n")
#
## check all the command line arguments and assign variables, 5 expected including scriptname
if len(sys.argv) != 4:
    print(f"\n\nERROR: number of command line arguments entered = {len(sys.argv)}")
    print(f"ERROR: Including scriptname, expected exactly 4 command line arguments in one of these formats:")
    print(f'\npython /path/to/scriptName.py "/home/data/*.csv" /path/to/output/alphabetFilename.txt /path/for/logFile/logFileName.log\n')
    print(f'        OR')
    print(f'\npython /path/to/scriptName.py "/home/data/file1.csv" /path/to/output/alphabetFilename.txt /path/for/logFile/logFileName.log\n')
    print(f'        OR')
    print(f'\npython /path/to/scriptName.py "train.csv test.csv" /path/to/output/alphabetFilename.txt /path/for/logFile/logFileName.log\n')
    print(f"\nExiting program with return code = 10\n")
    exit(10)
#
#
try:
    inFiles                         = sys.argv[1]
    alphabetDirFullPathWithFileName = sys.argv[2]
    logFilePathAndName              = sys.argv[3]
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
print(f"\t2) Output alphabet file: alphabetDirFullPathWithFileName = {alphabetDirFullPathWithFileName}")
print(f"\t3) Log file: logFilePathAndName = {logFilePathAndName}")
if "*" in inFiles:
    print(f"\tNOTE: ALL CSV files present in input file folder will be treated as input files.")
#
logging.warning(f"\nThe command line arguments assigned to variables as follows:\n")
logging.warning(f"\t1) Input File or Files: inFiles = {inFiles}")
logging.warning(f"\t2) Output alphabet file: alphabetDirFullPathWithFileName = {alphabetDirFullPathWithFileName}")
logging.warning(f"\t3) Log file: logFilePathAndName = {logFilePathAndName}")
if "*" in inFiles:
    logging.warning(f"\tNOTE: ALL CSV files present in input file folder will be treated as input files.")
#
print(f"\n\nProceeding to main logic.\n")
logging.warning(f"\n\nProceeding to main logic.\n")
#
#alphabetDir = '/home/rohit/dpspTraining/commVoiceSet2-FullValidated/alphabetDir/'
#alphabetFileName = 'alphabet-allValidated.txt'
#alphabetDirFullPathWithFileName = alphabetDir + alphabetFileName
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
#inFiles = ['/home/rohit/dpspTraining/data/wavFiles/wav33/csvFiles/train33.csv',
#    '/home/rohit/dpspTraining/data/wavFiles/wav33/csvFiles/dev33.csv',
#    '/home/rohit/dpspTraining/data/wavFiles/wav33/csvFiles/test33.csv']
######### TEMP CODE for testing   --- END
#
print("\n### Processing the following CSV files: ###")
for file in inFiles:
    print(f"\t{file}")
logging.warning("\n### Processing the following CSV files: ###")
for file in inFiles:
    logging.warning(f"\t{file}")
#
print(f"\n\n")
logging.warning(f"\n\n")
#
allText = set()
for inFile in (inFiles):
    with open(inFile, 'r') as csvFile:
        reader = csv.reader(csvFile)
        try:
            for row in reader:
                allText |= set(str(row[2]))
        except IndexError as ie:
            print("\n\nERROR: Input file not formatted properly. Check there are 3 columns with the 3rd containing the transcript.")
            print(f"Input file =\n{inFile}")
            print(f"Exiting program with return code = 30.\n")
            logging.warning("\n\nERROR: Input file not formatted properly. Check there are 3 columns with the 3rd containing the transcript.")
            logging.warning(f"Input file =\n{inFile}")
            logging.warning(f"Exiting program with return code = 30.\n")
            sys.exit(30)
        finally:
            csvFile.close()
#
print("\n\n### The following unique characters were found in the transcripts: ###")
logging.warning(f"\n\n### The following unique characters were found in the transcripts: ###")
listAlphaChars = list(allText)
print(f"{listAlphaChars}")
logging.warning(f"{listAlphaChars}")
print("\n### All these characters should be in the alphabet file ###")
logging.warning(f"\n### All these characters should be in the alphabet file ###")
#
listAlphaChars.sort()
#
## hardcoded text that are to be part of the alphabet file from explanation perspective.
hcLine1 = "# Each line in this file represents the Unicode codepoint (UTF-8 encoded)\n"
hcLine2 = "# associated with a numeric label.\n"
hcLine3 = "# A line that starts with # is a comment. You can escape it with \\# if you wish\n"
hcLine4 = "# to use '#' as a label.\n"
hcLine2ndLastLine = "# The last (non-comment) line needs to end with a newline.\n"
#
content = [hcLine1, hcLine2, hcLine3, hcLine4] + list( (str(ele) + "\n") for ele in listAlphaChars) + [hcLine2ndLastLine]
content = "".join(content)
#
## show the contents tha will be written to the alphabet file
print(f"\n\nThe content being written to the file is STARTS FROM THE NEXT LINE.")
print(f"{content}")
print(f"The content being written to the file ENDED ON THE ABOVE LINE.")
logging.warning(f"\n\nThe content being written to the file is STARTS FROM THE NEXT LINE..............")
logging.warning(f"\n{content}")
logging.warning(f"The content being written to the file ENDED ON THE ABOVE LINE...................")
#
## create the alphabet file
with open(alphabetDirFullPathWithFileName, 'w') as alphaFile:
    alphaFile.write(content)
#
print(f"\n\nAlphabet file created here = {alphabetDirFullPathWithFileName}")
logging.warning(f"\n\nAlphabet file created here = {alphabetDirFullPathWithFileName}")
# convert any dos new line (CRLF) to unix new line (LF)
# https://stackoverflow.com/questions/36422107/how-to-convert-crlf-to-lf-on-a-windows-machine-in-python/43678795#43678795
#
print(f"\n\nNormal exit\n\n")
logging.warning(f"\n\nNormal exit\n\n")
exit(0)