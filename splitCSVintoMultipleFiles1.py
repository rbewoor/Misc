##############
# Usage:
#   1) run either with no command line arguments CLA's (will use hardcoded values) , OR
#   2) with only 1 argument for NumberOfEntriesPerFile,     OR
#       python <programname> <#NumberOfEntriesPerFile>
#   2a)     NumberOfEntriesPerFile = <some integer> is a valid input , OR
#           NumberOfEntriesPerFile = 0   is treated as read the whole CSV and no splitting is needed
#               The flag doNOTSplitOutputFlag = FALSE by default.
#                   ONLY if the NumberOfEntriesPerFile is passed as 0 in CLA, then doNOTSplitOutputFlag = TRUE.
#   3) with exactly ALL 4 argements given below
#       python <programname> <#NumberOfEntriesPerFile> <fileInputCsvPathFilename> <folderOutputFilesPathHiLevel> <folderSourceWavFilesPath>
# 
# Read the csv file and split the information into sets of files of NumberOfEntriesPerFile variable.
#   The CSV file has header row with following 3 columns:
#       wav_filename,wav_filesize,transcript
# Specify the output folder and the prefix for the output files.
# Important points:
#   1) if not using CLA and with hardcoding, make sure the folderSourceWavFilesPath string includes the / at end of the string. Otherwise
#       the wav filename will be concatenated without the forward slash and the file will not be found and entry not picked up into array
#       for processing.
#       1a) However, if using CLA then the code will automatically add the forward slash at end of all folder arguments.
#   2) change NumberOfEntriesPerFile value to specify how many wav files to be placed in individual output directory. The entries will be
#       made into the output TXT file (containing filename and the transcript separated by TAB).
#   3) If using CLA version, the output file name will start with exactly the input file name, followed by the middle changing part digit and
#       and have the .txt extension.
#
#############
import pandas as pd
import os
import sys
from os import path
from shutil import copyfile
import csv
import codecs

import logging

logging.basicConfig(level=logging.WARNING, filename='LOG_splitCSVintoMultipleFiles1.log',                                                       \
    filemode='w', format='%(asctime)s %(levelname)s:%(message)s')

global fileInputCsvPathFilename
global folderSourceWavFilesPath
global folderOutputFilesPathHiLevel
global folderOutputFilesPathLowLevel
global outputFilenamesStarting
global outputFilenamesEnding
global outputFilenamesMiddleChanging
global NumberOfEntriesPerFile
global doNOTSplitOutputFlag

NumberOfEntriesPerFile = 5
doNOTSplitOutputFlag = False

fileInputCsvPathFilename = "xxx"
#fileInputCsvPathFilename = "/home/rohit/dpspTraining/data/wavFiles/azure1/allValidatedSet-validedFilesOnly-first23.csv"

folderSourceWavFilesPath = "/home/rohit/dpspTraining/data/wavFiles/commVoiceSet2-FullValidated/convertedWavs/"

folderOutputFilesPathHiLevel = "/home/rohit/dpspTraining/data/wavFiles/azure1/outputFilesDir/"

outputFilenamesStarting = 'allValidatedSet-validedFilesOnly-first23'
outputFilenamesEnding = '.txt'
#outputFilenamesMiddleChanging = 0  # specified as value 0 later in code just before usage

global counters
counters =                                                                                                                                  \
    {"countRowsReadFromInputCsvFile": 0, "countFileFoundInWavFolder": 0, "countFileNOTFoundInWavFolder": 0, "countOutputTxtFilesCreated": 0,   \
    "countTotalWritesToAllTxts": 0, "countWritesToLatestTxt": 0, "countWavFileCopySuccess": 0, "countWavFileCopyFailed": 0, "countOutputDirsCreated": 0 }
    

### ----------------- FUNCTION DEFINITIONS START ------------- ###
####
def initialSetup():
    global NumberOfEntriesPerFile
    global fileInputCsvPathFilename
    global folderOutputFilesPathHiLevel
    global folderSourceWavFilesPath
    global outputFilenamesStarting

    print(f"#CLI arguments provided = {len(sys.argv)}")
    logging.warning(f"#CLI arguments provided = {len(sys.argv)}")

    if len(sys.argv) == 1: # running with no CLI, allowed
        return(0)
    elif len(sys.argv) == 2: # running with only one CLI, allowed
        # assign the NumberOfEntriesPerFile
        if sys.argv[1].isdigit():
            NumberOfEntriesPerFile = int(sys.argv[1])
            return(0)
        else:
            print(f"ERROR: Problem with Argument 1 for NumberOfEntriesPerFile")
            logging.critical(f"ERROR: Problem with Argument 1 for NumberOfEntriesPerFile")
            return(12)
    elif len(sys.argv) == 5: # running with ALL 4 parameters, allowed
        # assign the NumberOfEntriesPerFile
        if sys.argv[1].isdigit():
            NumberOfEntriesPerFile = int(sys.argv[1])
        else:
            print(f"ERROR: Problem with Argument 1 for NumberOfEntriesPerFile")
            logging.critical(f"ERROR: Problem with Argument 1 for NumberOfEntriesPerFile")
            return(12)
        # assign the input CSV filename
        fileInputCsvPathFilename = sys.argv[2]
        # assign the output files high level path
        if sys.argv[3][-1:] == "/":
            folderOutputFilesPathHiLevel = sys.argv[3]
        else:
            folderOutputFilesPathHiLevel = sys.argv[3] + "/"
        # assign the wav files path
        if sys.argv[4][-1:] == "/":
            folderSourceWavFilesPath = sys.argv[4]
        else:
            folderSourceWavFilesPath = sys.argv[4] + "/"
        # extract input CSV filename and assign to output filename
        if fileInputCsvPathFilename.rfind('/') == -1:
            print(f"ERROR: Unable to identify the input CSV filename")
            logging.critical(f"ERROR: Unable to identify the input CSV filename")
            return(13)
        elif fileInputCsvPathFilename.rfind('.') == -1:
            outputFilenamesStarting = fileInputCsvPathFilename[ fileInputCsvPathFilename.rfind('/') + 1 : ]
            return(0)
        elif fileInputCsvPathFilename.rfind('/') >= fileInputCsvPathFilename.rfind('.') :
            print(f"ERROR: input CSV file, expected last . to be to right of the last /")
            logging.critical(f"ERROR: input CSV file, expected last . to be to right of the last /")
            return(14)
        else:
            outputFilenamesStarting = fileInputCsvPathFilename[ fileInputCsvPathFilename.rfind('/') + 1 : fileInputCsvPathFilename.rfind('.')]
    else:
        print(f"Error: Check number of CLI, expected none, 1 or exactly 4.")
        logging.critical(f"Error: Check number of CLI, expected none, 1 or exactly 4.")
        return(11)
    
    return(0)
####
def readCSVFileIntoProcessingArray(procArray, inFileCsv, nRowsSkip, nRowsRead):
    '''
    Read in required lines from the csv file and pick up only the "path" and "sentence" columns.
    For each row of data, create a tuple (path, sentence) and append into the samples[] array and return this array
    '''
    #
    # https://honingds.com/blog/pandas-read_csv/
    # https://towardsdatascience.com/why-and-how-to-use-pandas-with-large-data-9594dda2ea4c
    # https://cmdlinetips.com/2018/01/how-to-load-a-massive-file-as-small-chunks-in-pandas
    
    print(f"\nValue of nRowsRead = {nRowsRead}")
    if nRowsRead == -1:
        # more basic version WITHOUT nrows and skiprows parameters
        print(f"Reading the ENTIRE CSV file into memory.")
        logging.warning(f"Reading the ENTIRE CSV file into memory.")
        df = pd.read_csv( inFileCsv, delimiter=',',                                                                                         \
        encoding='utf-8', header=0, usecols = ["wav_filename", "transcript"] )
    else:
        # version which has the nrows and skiprows parameters being used
        print(f"Reading {nRowsRead} rows from CSV file into memory.")
        logging.warning(f"Reading {nRowsRead} rows from CSV file into memory.")
        df = pd.read_csv( inFileCsv, delimiter=',', nrows=nRowsRead, skiprows = nRowsSkip,                                                 \
            encoding='utf-8', header=0, usecols = ["wav_filename", "transcript"] )

    df = df.fillna('   ')
    
    # Get audiofile wav filename and transcript and save as tuple into the processing array
    for rowIdx, rowData in df.iterrows():
        counters['countRowsReadFromInputCsvFile'] += 1
        if os.path.isfile( folderSourceWavFilesPath + rowData['wav_filename'] ):
            procArray.append( (rowData['wav_filename'], rowData['transcript']) )
            counters['countFileFoundInWavFolder'] += 1
        else:
            counters['countFileNOTFoundInWavFolder'] += 1
    
    #return(df)
####
def summaryPrint():
    print(f"#Rows read from input CSV file = {counters['countRowsReadFromInputCsvFile']}")
    logging.warning(f"#Rows read from input CSV file = {counters['countRowsReadFromInputCsvFile']}")

    print(f"#Wav files FOUND in wav folder = {counters['countFileFoundInWavFolder']}")
    print(f"#Wav files NOT FOUND in wav folder = {counters['countFileNOTFoundInWavFolder']}")
    logging.warning(f"#Wav files FOUND in wav folder = {counters['countFileFoundInWavFolder']}")
    logging.warning(f"#Wav files NOT FOUND in wav folder = {counters['countFileNOTFoundInWavFolder']}")

    print(f"#doNOTSplitOutputFlag = {doNOTSplitOutputFlag}")
    print(f"#value used for NumberOfEntriesPerFile = {NumberOfEntriesPerFile}")
    print(f"#Output directories created = {counters['countOutputDirsCreated']}")
    print(f"#Output files created = {counters['countOutputTxtFilesCreated']}")
    print(f"#Total writes to all output files = {counters['countTotalWritesToAllTxts']}")
    logging.warning(f"#doNOTSplitOutputFlag = {doNOTSplitOutputFlag}")
    logging.warning(f"#value used for NumberOfEntriesPerFile = {NumberOfEntriesPerFile}")
    logging.warning(f"#Output directories created = {counters['countOutputDirsCreated']}")
    logging.warning(f"#Output files created = {counters['countOutputTxtFilesCreated']}")
    logging.warning(f"#Total writes to all output files = {counters['countTotalWritesToAllTxts']}")

    return
####
def writeDataToOutputFileAndCopyWav(writer, processingArray, folderSourceWavFilesPath, folderOutputFilesPathLowLevel):

    try:
        writer.writerow({'azureWavFilename': procArrayEntry[0], 'azureTranscript': procArrayEntry[1] })
        counters['countWritesToLatestTxt'] += 1
        counters['countTotalWritesToAllTxts'] += 1
    except:
        print(f"ERROR: problem writing data to output file...")
        print(f"\tFilename = {procArrayEntry[0]}\n\tTranscript = {procArrayEntry[1]}")
        print("Exiting program with return code = 201")
        logging.warning(f"ERROR: problem writing data to output file...")
        logging.warning(f"\n\tFilename = {procArrayEntry[0]}\n\tTranscript = {procArrayEntry[1]}")
        logging.warning("Exiting program with return code = 201")
        exit(201)
    
    # now copy the wav file from source to target folder and abort if there is any problem
    try:
        sourceFile = folderSourceWavFilesPath + procArrayEntry[0]
        targetFile = folderOutputFilesPathLowLevel + procArrayEntry[0]
        copyfile(sourceFile, targetFile)
        logging.warning(f"wavfile copy SUCCESS. Filename -- {procArrayEntry[0]}")
    except IOError as e:
        print(f"Unable to copy file -- {sourceFile}. Error -- {e}")
        logging.critical(f"Unable to copy file -- {sourceFile}. Error -- {e}")
        print(f"Exiting program with return code = 202")
        logging.critical(f"Exiting program with return code = 202")
        exit(201)
    except:
        print(f"UNEXPECTED error while copying -- {sys.exc_info()}")
        logging.critical(f"UNEXPECTED error while copying -- {sys.exc_info()}")
        print(f"Exiting program with return code = 203")
        logging.critical(f"Exiting program with return code = 203")
        exit(202)
    return
####
### ----------------- FUNCTION DEFINITIONS  END  ------------- ###

### ------------------- MAIN LOGIC STARTS HERE  -------------- ###

logging.warning(f"\n")
logging.warning(f"Started the program\n")

rc4mInitialSetupRoutine = initialSetup()
if ( rc4mInitialSetupRoutine == 0 ):
    print(f"Initial Setup fine.")
    logging.warning(f"Initial Setup fine.")
    print(f"\n\nWill use following parameters...\n")
    if NumberOfEntriesPerFile == 0:
        doNOTSplitOutputFlag = True
    print(f"\t\tdoNOTSplitOutputFlag = {doNOTSplitOutputFlag}")
    print(f"\t\tNumberOfEntriesPerFile = {NumberOfEntriesPerFile}")
    print(f"\t\tinput CSV fileInputCsvPathFilename = {fileInputCsvPathFilename}")
    print(f"\t\toutput folder folderOutputFilesPathHiLevel = {folderOutputFilesPathHiLevel}")
    print(f"\t\twav files folder folderSourceWavFilesPath = {folderSourceWavFilesPath}")
    print(f"\t\toutput file name will be like this = {outputFilenamesStarting + '--1' + '.txt'}")
    logging.warning(f"\n\nWill use following parameters...\n")
    logging.warning(f"\n\t\tdoNOTSplitOutputFlag = {doNOTSplitOutputFlag}")
    logging.warning(f"\n\t\tNumberOfEntriesPerFile = {NumberOfEntriesPerFile}")
    logging.warning(f"\n\t\tinput CSV fileInputCsvPathFilename = {fileInputCsvPathFilename}")
    logging.warning(f"\n\t\toutput folder folderOutputFilesPathHiLevel = {folderOutputFilesPathHiLevel}")
    logging.warning(f"\n\t\twav files folder folderSourceWavFilesPath = {folderSourceWavFilesPath}")
    logging.warning(f"\n\t\toutput file name will be like this = {outputFilenamesStarting + '--1' + '.txt'}")
else:
    print(f"ERROR: Initial setup problem. Function return code = {rc4mInitialSetupRoutine}")
    print(f"Exiting program with return code = 50")
    logging.critical(f"ERROR: Initial setup problem. Function return code = {rc4mInitialSetupRoutine}")
    logging.critical(f"Exiting program with return code = 50")
    exit(50)

## temp code start
#exit(0)
## temp code ends
# load the CSV file
if os.path.isfile(fileInputCsvPathFilename):
    print(f"Found CSV file....Loading from location: {fileInputCsvPathFilename}")
    logging.warning(f"Found CSV file and Loading from location:\n           {fileInputCsvPathFilename}")
else:
    print(f"ERROR: input CSV file not found here: {fileInputCsvPathFilename}")
    print(f"Exiting program with return code = 100")
    logging.critical(f"ERROR: input CSV file not found here::\n           {fileInputCsvPathFilename}")
    logging.critical(f"Exiting program with return code = 100")
    exit(100)

# read the CSV and extract the wav file name and the transcript text
#     and put them into the samples array
# set numRowsRead = -1  to read the entire file
numRowsSkip = 0
numRowsRead = -1
logging.warning(f"\nDataframe loading parameters:\t\tnumRowsSkip = {numRowsSkip}\t\tnumRowsRead = {numRowsRead}")

# array to hold filenames and their transcripts.
processingArray = []
readCSVFileIntoProcessingArray(processingArray, fileInputCsvPathFilename, numRowsSkip, numRowsRead)
lenProcessingArray = len(processingArray)

print(f"\n   Finished loading the dataframe")
print(f"        counters['countRowsReadFromInputCsvFile'] =   {counters['countRowsReadFromInputCsvFile']}")
print(f"        length of processing array =   {lenProcessingArray}")
print(f"        #Wav files NOT FOUND in wav folder = {counters['countFileNOTFoundInWavFolder']}")
print(f"        Above two values should match if all wav files were found.")
logging.warning(f"\n   Finished loading the dataframe")
logging.warning(f"        counters['countRowsReadFromInputCsvFile'] =   {counters['countRowsReadFromInputCsvFile']}")
logging.warning(f"        length of processing array =   {len(processingArray)}")
logging.warning(f"        #Wav files NOT FOUND in wav folder = {counters['countFileNOTFoundInWavFolder']}")
logging.warning(f"        Above two values should match if all wav files were found.")

# start creating the output files until all entries in the processing array are finished
outputFilenamesMiddleChanging = 0

if doNOTSplitOutputFlag:
    NumberOfEntriesPerFile = lenProcessingArray
blockStartIndex = 0
while (blockStartIndex < lenProcessingArray ):
    counters['countWritesToLatestTxt'] = 0
    outputFilenamesMiddleChanging += 1

    folderOutputFilesPathLowLevel = folderOutputFilesPathHiLevel + str(outputFilenamesMiddleChanging) + '/'
    currentOutputFilename = outputFilenamesStarting + '--' + str(outputFilenamesMiddleChanging) + outputFilenamesEnding

    # make the directory first and if this fails then exit as fatal error code 200
    try:
        if os.path.exists(folderOutputFilesPathLowLevel):
            print(f"ERROR: output directory already exists.")
            print(f"Exiting program with return code = 201")
            logging.critical(f"ERROR: output directory already exists.")
            logging.critical(f"Exiting program with return code = 201")
            exit(201)
        else:
            os.mkdir(folderOutputFilesPathLowLevel)
            print(f"\n\nmkdir SUCCESS -- {folderOutputFilesPathLowLevel}\t\t...continuing to copy wav files and make txt")
            logging.warning(f"\n\nmkdir SUCCESS -- {folderOutputFilesPathLowLevel}\t\t...continuing to copy wav files and make txt")
            counters['countOutputDirsCreated'] += 1
    except:
        print(f"UNEXPECTED error while creating folder -- {sys.exc_info()}")
        print(f"Exiting program with return code = 200")
        logging.critical(f"UNEXPECTED error while creating folder -- {sys.exc_info()}")
        logging.critical(f"Exiting program with return code = 200")
        exit(200)
    
    print(f"\n\t\tCreating output file to\n\t\t-- path = {folderOutputFilesPathLowLevel} -- filename = {currentOutputFilename}")
    print(f"\nblockStartIndex = {blockStartIndex},\t\tblockStartIndex + NumberOfEntriesPerFile = {blockStartIndex + NumberOfEntriesPerFile}")
    logging.warning(f"\n\t\tCreating output file to\n\t\t-- path = {folderOutputFilesPathLowLevel} -- filename = {currentOutputFilename}")
    logging.warning(f"\nblockStartIndex = {blockStartIndex},\t\tblockStartIndex + NumberOfEntriesPerFile = {blockStartIndex + NumberOfEntriesPerFile}")
    
    # create the output file  with the BOM at start of file    for UTF-8   the byte sequence is 0xEF 0xBB 0xBF
    with open( (folderOutputFilesPathLowLevel + currentOutputFilename ), 'wb') as currentOutputTxt4BOM:
        currentOutputTxt4BOM.write(codecs.BOM_UTF8)
    print(f"\nBOM inserted into file")
    logging.warning(f"\nBOM inserted into file")
    # now write the data
    with open( (folderOutputFilesPathLowLevel + currentOutputFilename ), 'a', newline='', encoding='utf-8') as currentOutputTxt:
        writer = csv.DictWriter(currentOutputTxt, delimiter='\t', lineterminator="\n", fieldnames= ['azureWavFilename', 'azureTranscript'] )
        # header data is not needed for the azure training data
        #writer.writeheader()
        if (blockStartIndex + NumberOfEntriesPerFile ) < lenProcessingArray :
            for procArrayEntry in processingArray[blockStartIndex : blockStartIndex + NumberOfEntriesPerFile ] :
                writeDataToOutputFileAndCopyWav(writer, processingArray, folderSourceWavFilesPath, folderOutputFilesPathLowLevel)
            
            # for procArrayEntry in processingArray[blockStartIndex : blockStartIndex + NumberOfEntriesPerFile ] :
            #     writer.writerow({'azureWavFilename': procArrayEntry[0], 'azureTranscript': procArrayEntry[1] })
            #     counters['countWritesToLatestTxt'] += 1
            #     counters['countTotalWritesToAllTxts'] += 1
                
            #     # now copy the wav file from source to target folder and abort if there is any problem
            #     try:
            #         sourceFile = folderSourceWavFilesPath + procArrayEntry[0]
            #         targetFile = folderOutputFilesPathLowLevel + procArrayEntry[0]
            #         copyfile(sourceFile, targetFile)
            #         logging.warning(f"wavfile copy SUCCESS. Filename -- {procArrayEntry[0]}")
            #     except IOError as e:
            #         print(f"Unable to copy file -- {sourceFile}. Error -- {e}")
            #         logging.critical(f"Unable to copy file -- {sourceFile}. Error -- {e}")
            #         print(f"Exiting program with return code = 201")
            #         logging.critical(f"Exiting program with return code = 201")
            #         exit(201)
            #     except:
            #         print(f"UNEXPECTED error while copying -- {sys.exc_info()}")
            #         logging.critical(f"UNEXPECTED error while copying -- {sys.exc_info()}")
            #         print(f"Exiting program with return code = 202")
            #         logging.critical(f"Exiting program with return code = 202")
            #         exit(202)
        else:
            for procArrayEntry in processingArray[blockStartIndex :  ] :
                writeDataToOutputFileAndCopyWav(writer, processingArray, folderSourceWavFilesPath, folderOutputFilesPathLowLevel)
            
            # for procArrayEntry in processingArray[blockStartIndex :  ] :
            #     writer.writerow({'azureWavFilename': procArrayEntry[0], 'azureTranscript': procArrayEntry[1] })
            #     counters['countWritesToLatestTxt'] += 1
            #     counters['countTotalWritesToAllTxts'] += 1
                
            #     # now copy the wav file from source to target folder and abort if there is any problem
            #     try:
            #         sourceFile = folderSourceWavFilesPath + procArrayEntry[0]
            #         targetFile = folderOutputFilesPathLowLevel + procArrayEntry[0]
            #         copyfile(sourceFile, targetFile)
            #         logging.warning(f"wavfile copy SUCCESS. Filename -- {procArrayEntry[0]}")
            #     except IOError as e:
            #         print(f"Unable to copy file -- {sourceFile}. Error -- {e}")
            #         logging.critical(f"Unable to copy file -- {sourceFile}. Error -- {e}")
            #         print(f"Exiting program with return code = 201")
            #         logging.critical(f"Exiting program with return code = 201")
            #         exit(201)
            #     except:
            #         print(f"UNEXPECTED error while copying -- {sys.exc_info()}")
            #         logging.critical(f"UNEXPECTED error while copying -- {sys.exc_info()}")
            #         print(f"Exiting program with return code = 202")
            #         logging.critical(f"Exiting program with return code = 202")
            #         exit(202)
    
    print(f"\nWrote counters['countWritesToLatestTxt'] = {counters['countWritesToLatestTxt']} entries to file number {outputFilenamesMiddleChanging}")
    logging.warning(f"\nWrote counters['countWritesToLatestTxt'] = {counters['countWritesToLatestTxt']} entries to file number {outputFilenamesMiddleChanging}")
    print(f"\nTotal writes to ALL Csv's so far\tcounters['countTotalWritesToAllTxts'] = {counters['countTotalWritesToAllTxts']}")
    logging.warning(f"\nTotal writes to ALL Csv's so far\tcounters['countTotalWritesToAllTxts'] = {counters['countTotalWritesToAllTxts']}")
    
    blockStartIndex += NumberOfEntriesPerFile
    counters['countOutputTxtFilesCreated'] += 1

print(f"\n\nAll output files created\n\nSUMMARY INFO.....\n\n")
logging.warning(f"\n\nAll output files created\n\nSUMMARY INFO.....\n\n")

summaryPrint()
#
print(f"\n\nNormal exit")
logging.warning(f"\n\n")
logging.warning(f"Normal exit")
exit(0)