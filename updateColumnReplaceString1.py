'''
#######################################################################################
###  For the input CSV file, for the column name specified, update all entries in the
###      column by replacing an OLD-string with a NEW-string.
###  
###  To be used to change the file location for the wav files to be used for Deepspeech
###     training.
###
###  The output filename is the inputFileName followed by _new if the file has an extension.
###      If no extension, then blindly add _new at end of the file name.
###      E.g. inputFile = abc.csv     outputFile = abc_new.csv
###      E.g. inputFile = abc         outputFile = abc_new
###
###  NOTE: Expects 4 command line parameters (excluding the script name)
###
#######################################################################################
###
###  Usage example with position numbers indicated:
###                        0                                     1                           2            3           4
###  python </script/folder/path/programName.py> </input/file/with/path/filename.csv> <column-name> <OLD-string> <NEW-string>
###  
###  Expects exactly 5 Command line arguments (including the script name):
###  0)  ScriptName.py
###  1)  Absolute path and name of the input file
###  2)  Column name - in which the update should happen
###  3)  OLD string
###  4)  NEW string
###
#######################################################################################
'''
import numpy as np
import pandas as pd
import os, sys
#
### ----------------- FUNCTIONs AND CLASS DEFINITIONS START ------------- ###
####
### ----------------- FUNCTIONs AND CLASS DEFINITIONS  END  ------------- ###
###
### ------------------- MAIN LOGIC STARTS HERE  -------------- ###
#
## check all the command line arguments and assign variables, 5 expected including scriptname
print(f"\n\n")
if len(sys.argv) != 5:
    print(f"\n\nERROR: number of command line arguments entered = {len(sys.argv)}")
    print(f"ERROR: Including scriptname, expected exactly 5 command line arguments in this format:")
    print(f"\npython </script/folder/path/<programName.py> </input/file/with/path/filename.csv> <column-name> <OLD-string> <NEW-string>\n")
    print(f"\nExiting program with return code = 10\n")
    exit(10)
#
try:
    inPdFile       = sys.argv[1]
    colToBeUpdated = sys.argv[2]
    oldString      = sys.argv[3]
    newString      = sys.argv[4]
except:
    print(f"\n\nERROR: error assigning the arguments to variables.")
    print(f"Exiting program with return code = 11\n")
    exit(11)
#
# check input file exists
if os.path.isfile(inPdFile):
    print(f"Found input file.")
else:
    print(f"\n\nERROR: Input file not found here: {inPdFile}")
    print(f"Exiting program with return code = 12\n")
    exit(12)
#
print(f"\nThe command line arguments assigned to variables as follows:\n")
print(f"\t1) Input File: inPdFile = {inPdFile}")
print(f"\t2) Column to be updated: colToBeUpdated = {colToBeUpdated}")
print(f"\t3) Old string to be replaced: oldString = {oldString}")
print(f"\t4) New string for replacement: newString = {newString}")
#
print(f"\nProceeding to main logic.\n")
#
## now main logic starts
#
# set rowsToRead = -1 to read the whole dataframe in one shot, else specify the number accordingly
rowsToRead = -1
rowsToSkip = 0
if rowsToRead == -1:
    dfIn = pd.read_csv( inPdFile, sep=',', skiprows = range(1, rowsToSkip+1), header = 0, low_memory=False )
else:
    dfIn = pd.read_csv( inPdFile, sep=',', nrows = rowsToRead, skiprows = range(1, rowsToSkip+1), header = 0, low_memory=False )
#
print(f"\n\tRead the input file.\ndfIn.shape = {dfIn.shape}\n")
#
dfOut = dfIn.copy()
del(dfIn)
#
countBefore = dfOut[colToBeUpdated].str.count(newString).sum().item()
dfOut[colToBeUpdated] = dfOut[colToBeUpdated].str.replace(oldString, newString, case=True, regex=False)
countAfter = dfOut[colToBeUpdated].str.count(newString).sum().item()
#
## build the output filename by checking if there is any . in the filename already. Then accordingly build the output file name.
if inPdFile.find('.') == -1:
    ## blindly append _new at the end
    outPdFile = inPdFile + '_new'
else:
    ## blindly split on the last . and add _new before the .
    splitFile = inPdFile.rsplit('.', 1)
    outPdFile = splitFile[0] + '_new.' + splitFile[1]
#
try:
    dfOut.to_csv(outPdFile, index=False)
except:
    print(f"\n\nERROR: Problem creating the output file here: {inPdFile}")
    print(f"Exiting program with return code = 13\n")
    exit(13)
#
# Print the summary info
#
print(f"\n\n ########## SUMMARY ######### SUMMARY ######### SUMMARY #########\n")
print(f"Input File                        = {inPdFile}")
print(f"Output File                       = {outPdFile}")
print(f"Old String (that was replaced)    =\n{oldString}")
print(f"New String (used for replacement) =\n{newString}")
print(f"Number of replacements done       = {countAfter - countBefore}")
#
print(f"\n\nNormal Exit")
exit(0)
### -------------------  MAIN LOGIC ENDS HERE   -------------- ###