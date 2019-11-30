# Misc
Various short scripts made

1) Script Name: concatCSVFiles1.py
Description: Script to concatenate CSV files with comamnd line parameters. Expects 5 command line args (including script name). Can be used in two ways. First is combine ALL the CSV files in the input folder. Second is combine specific CSV files. Logging implemented.

2) Script Name: updateColumnReplaceString1.py
Description: Script to update a CSV files particular columns cells, by replacing an 'old_string' with a 'new_string'. Uses command line args. No logging implemented.

3) Script Name: splitDeepspeechCsvIntoTrainDevTest1.py
Description: Script to split the Deepspeech CSV files into 3 files for TRAIN DEV and TEST.
Expects exactly 6 Command line arguments (including the script name). Specifiy using absolute numbers or percentages. Specify whether or not to shuffle before splitting. Will not work if the split ratio is such that any of the output files will have not data due to too litte data or split ratio too small. Logging implemented.

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
Important inputs to edit before running:
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
Important inputs to edit before running:
validCharsString::: Strng containing all the valid characters for Deespeech training.
colToCheck::: The column which contains the sentences.
