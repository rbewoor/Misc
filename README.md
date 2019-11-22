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

6) 
