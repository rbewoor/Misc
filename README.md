# Misc
Various short scripts made

1) Script Name: concatCSVFiles1.py

Description: Script to concatenate CSV files with comamnd line parameters. Expects 5 command line args (including script name). Can be used in two ways. First is combine ALL the CSV files in the input folder. Second is combine specific CSV files. Logging implemented.

2) Script Name: updateColumnReplaceString1.py

Description: Script to update a CSV files particular columns cells, by replacing an 'old_string' with a 'new_string'. Uses command line args. No logging implemented.

3) Script Name: splitDeepspeechCsvIntoTrainDevTest1.py

Description: Script to split the Deepspeech CSV files into 3 files for TRAIN DEV and TEST.
Expects exactly 6 Command line arguments (including the script name). Specifiy using absolute numbers or percentages. Specify whether or not to shuffle before splitting. Will not work if the split ratio is such that any of the output files will have not data due to too litte data or split ratio too small. Logging implemented. Each output file has same name as input file appended by underscore and TRAIN or DEV or TEST.

4) Script Name: extractCharsFromCsvsMakeAlphabetFile3.py

NOTE: Adapted from the Deespeech repo scripts.

Description: From the Deepspeech CSV input file or files, create the alphabet file. As usual expected to have the three columns with the third column being the transcripts. Will process the contents of this third column. It reads the text in the data and stores a set of unique characters as the alphabet file. Expects 4 command line args (including script name). Input files can be specified in one of three ways. Logging implemented.

5) Script Name: extractTranscriptFromCsvsMakeVocabFileCSV3.py

NOTE: Adapted from the Deespeech repo scripts.

Description: From the CSV input file or files, create a the vocabulary file. As usual expected to have the three columns with the third column being the transcripts. Will process the contents of this third column. Removes any duplicates. Expects 4 command line args (including script name). Input files can be specified in one of three ways. Logging implemented.

6) Script Name: concatFilesRemoveDuplicates2.ipynb

Description: Takes list of files as input. Keeps removing duplicates in each file and appending into an output dataframe. Finally removes duplicates on this output dataframe and writes output file. Shows count of lines at each stage.

7) Script Name: testTTS11_with429503_parallelProc_charCountTrack-GITHUB.ipynb

NOTE: Works only for a PAID subscription for MS Azure - TTS service which allows up to 20 concurrent processes.

Description: Parallel processing to convert input sentences to wav files. Expects an input CSV file with the sentences in some row. Outputs set of files in the Deepspeech training CSV file format (path, wavFileSize, transcript). The converted wav files in required format of PCM 16kHz 16-bit Mono.

IMPORTANT INPUT VARIABLES TO EDIT BEFORE RUNNING:

logFilenameWithPath::: Location and name of the logging file.
inFilePath::: Location of the input file.
inFileName::: Input file name.
colsToReadIn::: Specify the column which contains the sentences. Only this column will be read in and the wav files created based on this.
rowsToRead::: Number of rows to process from input file.
rowsToSkip::: Number of rows to skip from input file.
outWavFilesPath::: Folder to save the output wav files.
outFilePath::: Folder to save the output CSV files.
outFileName4Deepspeech::: Filename for the Deespeech training file (without the .csv extension).
outFileNameFullData::: Filename for the output file which also has the voice type (without the .csv extension).
apiCallThrottleLimit::: Number of API calls by each worker after which to sleep for some time.
apiCallThrottleSleepTime::: Time in seconds for which to sleep to throttle speed.
accessTokenRecheckInSeconds::: Number of seconds after which each worker should regerenate its Access token automatically.
batchSizeForWorker::: Number of sentences from input file for each Task (note that each sentence is actually multiple API calls depending on the Voice Types specified).
statusRowPrintFreq::: How ofter to print the sentence being processed as status message. First sentence is always shown though.
voiceTypeShortNames::: List of the short name codes for the Voice Types to be used for conversion.
numConsumers::: Number of processes that will be started. Automatically set to the number of cores available (overwrite if required).

8) Script Name: deleteInvalidAlphaCharRows1.ipynb

Description: Check that only valid alphabet characters are present in the training sentences for Deepspeech. Any rows with sentences with invalid characters will be deleted. Output file will thus contain only rows with valid characters in sentences.

IMPORTANT INPUT VARIABLES TO EDIT BEFORE RUNNING:

validCharsString::: Strng containing all the valid characters for Deespeech training.
colToCheck::: The column which contains the sentences.

9) Script Name: testTTS13-GITHUB.ipynb

NOTE: Will work on Free version of Azure subscription key. No parallel processing as only 1 concurrent process allowed.

Description: NON-parallel processing to convert input sentences to wav files. Expects an input CSV file with the sentences in some row. Outputs two CSV files of which one is the Deepspeech training CSV file format (path, wavFileSize, transcript). The converted wav files in required format of PCM 16kHz 16-bit Mono.

IMPORTANT INPUT VARIABLES TO EDIT BEFORE RUNNING:

logFilenameWithPath::: Location and name of the logging file.
inFilePath::: Location of the input file.
inFileName::: Input file name.
colsToReadIn::: Specify the column which contains the sentences. Only this column will be read in and the wav files created based on this.
rowsToRead::: Number of rows to process from input file.
rowsToSkip::: Number of rows to skip from input file.
outWavFilesPath::: Folder to save the output wav files.
outFilePath::: Folder to save the output CSV files.
outFileName4Deepspeech::: Filename for the Deespeech training file (WITH the .csv extension).
outFileNameFullData::: Filename for the output file which also has the voice type (WITH the .csv extension).
apiCallThrottleLimit::: Number of API calls by each worker after which to sleep for some time -- set as 20.
apiCallThrottleSleepTime::: Time in seconds for which to sleep to throttle speed -- set as 60 seconds.
accessTokenRecheckInSeconds::: Number of seconds after which each worker should regerenate its Access token automatically.
statusRowPrintFreq::: How ofter to print the sentence being processed as status message. First sentence is always shown though.
voiceTypeShortNames::: List of the short name codes for the Voice Types to be used for conversion.

10) Script Name: testTTS13-GITHUB.PY

NOTE: Will work on Free version of Azure subscription key. No parallel processing as only 1 concurrent process allowed.

Description: NON-parallel processing to convert input sentences to wav files. Expects an input CSV file with the sentences in some row. Outputs two CSV files of which one is the Deepspeech training CSV file format (path, wavFileSize, transcript). The converted wav files in required format of PCM 16kHz 16-bit Mono.

COMMAND LINE VERSION OF THE JUPYTER NOTEBOOK.

Expects exactly 13 command line args (including script name) in this format:

python </script/folder/path/<programName.py> </input/file/with/path/filename.csv> <rowsToRead> <rowsToSkip> </output/file/path/wavsHere/> </output/file/path/csvs/> </outputFileNameForDeepspeech.csv> </outputFileNameNOTForDeepspeech.csv> <apiCallThrottleLimit> <apiCallThrottleSleepTime in Seconds> <statusRowPrintFreq> <fileNumber> </path/for/logFile/logFileName.log>
  
For example: to process 5 rows, skipping first 50 rows, API call limit=20, sleep for 60 seconds, print frequency=2, starting file number=51, one would run as below:
  
python testTTS13.py /home/rohit/dpspTraining/data/azure/pdfExtraction/System_800xA_Summary.pdf_extractedText_4.csv 5 50 /home/rohit/dpspTraining/data/azure/pdfExtraction/convertedWavs_13voice_51_55/ /home/rohit/dpspTraining/data/azure/pdfExtraction/convertedWavsCsvFile_13voice_51_55/ System_800xA_Summary.pdf_extractedText_4_forDS.csv System_800xA_Summary.pdf_extractedText_4_NOT_forDS.csv 20 60 2 51 /home/rohit/dpspTraining/data/azure/pdfExtraction/convertedWavsCsvFile_13voice_51_55/TestTTS13_13voice_51_55.log


11) Script Name: splitFileBlindlyMultiple1.py

Description: Script to split any input file into equal sized output files (except possibly last file).
Each output file has same name as input file appended by the starting+ending row numbers. Logging implemented. E.g. input file has 1001 rows with header, and the number of DATA rows required in output = 300; so here, 4 output files with names as: file_1_300, file_301_600, file_601_900, file_901_1000.

Expects exactly 5 Command line arguments (including the script name): python </script/path/programName.py> <path/with/inputFilename.csv> <rows per output file> <H or NH> </path/for/logFile/logFileName.log>

For above example one would run as: python </script/path/programName.py> <path/with/inputFilename.csv> 300 H </path/for/logFile/logFileName.log>
