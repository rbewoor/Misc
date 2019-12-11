import csv
import sys
import os

'''
Usage:
 $ python3 /script/folder/path/<programName.py> </input/vocab/file/with/path/vocabFilename.txt> </output/alpha/file/with/path/AlphaFilename.txt>

Expects exactly two Command line arguments (excluding the script name.)
First is the input vocabulary file with path.
Second is the the output alphabet file with path.
The script simply reads all the text from the input vocab the file, storing a set of unique characters that were seen along the way.
And the writes it to the output Alphabet file.
'''
if len(sys.argv) != 3:
    print(f"ERROR: number of command line arguments = {len(sys.argv)}")
    print(f"ERROR: Expected exactly three command line arguments expected in this format:")
    print(f"\t\t/script/folder/path/<programName.py> </input/vocab/file/with/path/vocabFilename.txt> </output/alpha/file/with/path/AlphaFilename.txt>")
    print(f"Exiting program with return code = 100")
    exit(100)

inFile = sys.argv[1]
alphabetDirFullPathWithFileName = sys.argv[2]

# check input vocab file exists
if os.path.isfile(inFile):
    print(f"Found vocab file....Loading from location: {inFile}")
else:
    print(f"ERROR: Vocab file not found here: {inFile}")
    print(f"Exiting program with return code = 200")
    exit(200)
#
allText = set()
with open(inFile, 'r') as inVocabFile:
    #reader = csv.reader(inVocabFile)
    for line in inVocabFile:
        allText |= set(str(line[0:-1]))
#
print("### The following unique characters were found in your transcripts: ###")
listAlphaChars = list(allText)
print(listAlphaChars)
print("### All these characters should be in your data/alphabet.txt file ###")
#
print(f"Making the alphabet file....")
listAlphaChars.sort()
#
# hardcoded text lines that are to be part of the alphabet file from explanation perspective
hcLine1 = "# Each line in this file represents the Unicode codepoint (UTF-8 encoded)\n"
hcLine2 = "# associated with a numeric label.\n"
hcLine3 = "# A line that starts with # is a comment. You can escape it with \\# if you wish\n"
hcLine4 = "# to use '#' as a label.\n"
hcLine2ndLastLine = "# The last (non-comment) line needs to end with a newline.\n"

content = [hcLine1, hcLine2, hcLine3, hcLine4] + list( (str(ele) + "\n") for ele in listAlphaChars) + [hcLine2ndLastLine]
content = "".join(content)

# show the contents tha will be written to the alphabet file
print(f"The content being written to the file is STARTS FROM THE NEXT LINE.")
print(f"{content}")
print(f"The content being written to the file ENDED ON THE ABOVE LINE.")

# create the alphabet file
with open(alphabetDirFullPathWithFileName, 'w') as alphaFile:
    alphaFile.write(content)
#
print(f"Alphabet file created at:\n{alphabetDirFullPathWithFileName}")
# convert any dos new line (CRLF) to unix new line (LF)
# https://stackoverflow.com/questions/36422107/how-to-convert-crlf-to-lf-on-a-windows-machine-in-python/43678795#43678795
#
print(f"\n\nNormal exit")
exit(0)