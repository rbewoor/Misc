## https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/Samples-Http/Python/TTSSample.py
import os, requests, time, sys
import pandas as pd
from xml.etree import ElementTree
from datetime import datetime
from random import randint
import logging
'''
#######################################################################################
###  Take the cleaned up extracted PDF contents CSV file as input data.
###  Convert the sentence to wav audio  in 16kHz, mono, PCM coding.
###  Save the audio files.
###  Create the CSV file required by Deepspeech training.
###  Create additional CSV file which also includes the short name of the voice type
###         -- note this file is not used for for Deepspeech and only for reference.
###
###  NOTES: Expects 13 command line parameters (including the script name)
###         Handles 503 error by making up to 3 API calls for the same conversion.
###         Handles 429 error by exiting prematurely and sets a flag to indicate problem occurred.
#######################################################################################
#
Usage example with position numbers indicated:
                    0                                       1                          2           3                    4
python </script/folder/path/programName.py> </input/file/with/path/filename.csv> <rowsToRead> <rowsToSkip> </output/file/path/wavsHere/>
            5                        6                                       7
</output/file/path/csvs/> </outputFileNameForDeepspeech.csv> </outputFileNameNOTForDeepspeech.csv>
         8                                9                           10               11                     12
<apiCallThrottleLimit> <apiCallThrottleSleepTime in Seconds> <statusRowPrintFreq> <fileNumber> </path/for/logFile/logFileName.log>

Expects exactly 12 Command line arguments (excluding the script name):
0)  ScriptName.py
1)  Absolute path and name of the input file
2)  Number of rows to read from input file (put -1 to all the rows)
3)  Number of rows to skip from input file
4)  Absolute path where to save the output wav files
5)  Absolute path where to save the output csv files
6)  Output csv file name for Deepspeech
7)  Output csv file name for non-Deepspeech (which includes the short name for voice type)
8)  Number of API calls to make before throttling
9)  Time to sleep (in seconds) during throttling
10) Status Print frequency: every now many rows to print to console
11) Filenumber from which to start
12) Log file name
'''
### ----------------- FUNCTIONs AND CLASS DEFINITIONS START ------------- ###
####
## https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/Samples-Http/Python/TTSSample.py
class TextToSpeech(object):
    #
    def __init__(self, subscription_key):
        self.subscription_key = subscription_key
        self.tts = None   ##  the text to be converted to audio -- defaulting the value to None
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        self.access_token = None
        self.access_token_startTime = None
    #
    #The TTS endpoint requires an access token. This method exchanges your
    #subscription key for an access token that is valid for ten minutes.
    #
    def get_token(self):
        #fetch_token_url = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        fetch_token_url = "https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)
        self.access_token_startTime = time.strftime("%Y%m%d-%H%M%S")
    #
    def check_tokenGenerationTime_and_regenerateIfRequired(self, thresholdInSecs = 540):
        timeNow = time.strftime("%Y%m%d-%H%M%S")
        s_tg = time.strptime(self.access_token_startTime, "%Y%m%d-%H%M%S")  # struct_time of token generation time
        s_now = time.strptime(timeNow, "%Y%m%d-%H%M%S")  # struct_time of now time
        timeDiff = time.mktime(s_now) - time.mktime(s_tg) ## time since token generation in seconds
        if timeDiff > thresholdInSecs: # azure documentation states token valid for 10 mins, so setting 9*60 = 540 secs
            logging.warning(f"\nRequesting new access token automatically.")
            logging.warning(f"Old token: Start time = {self.access_token_startTime}\nTime now = {timeNow}")
            logging.warning(f"Time Difference (secs) since last generation= {timeDiff}")
            #print(f"\nOld access_token = \n{self.access_token}\n")
            logging.warning(f"\nOld access_token = \n{self.access_token}\n")
            self.get_token()
            #print(f"\nNew Access Token received = \n{self.access_token}")
            logging.warning(f"\nNew Access Token received = \n{self.access_token}")
            #print(f"\nNew Access Token Start Time = \n{self.access_token_startTime}\n")
            logging.warning(f"\nNew Access Token Start Time = \n{self.access_token_startTime}\n")
    #
    def save_audio(self, inVoiceTypeShortName = '', fileNumber = 1, wavFilePath = ''):
        #### Inputs:
        ####       the ShortName of the voice type to be used.
        ####       the file number to include in the filename.
        ####       the absolute path where to save the audio file.
        #### Returns:
        ####       the status code (should be 200 if all good).
        ####       the audio file name created.
        #
        base_url = 'https://westeurope.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            #'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'X-Microsoft-OutputFormat': 'riff-16khz-16bit-mono-pcm', # Deepspeech needs 16kHz, mono, PCM encoded wav files
            'User-Agent': 'YOUR_RESOURCE_NAME'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        #voice.set('name', 'en-US-Guy24kRUS') # Short name for 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
        voice.set('name', inVoiceTypeShortName) # Short name for 'Microsoft Server Speech Text to Speech Voice
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)
        #
        ## sometimes azure response = 503
        ##    https://docs.microsoft.com/en-us/rest/api/searchservice/http-status-codes
        ##    Solution: make API call up to 3 times with random delay
        for _ in range(3):
            counters['countApiCallsMade'] += 1
            response = requests.post(constructed_url, headers=headers, data=body)
            if response.status_code != 503:
                break
            sleep503Time = randint(3, 10)
            #print(f"\nAure response = 503, so sleeping for {sleep503Time} seconds.\n")
            logging.warning(f"\nAure response = 503, so sleeping for {sleep503Time} seconds.\n")
            time.sleep(sleep503Time)
            #
        #
        #If a success response is returned, then the binary audio is written to the file.
        #
        outWavFile = '' # if conversion failed then this will remain empty string
        # if the conversion is successful then status code will be 200.
        if response.status_code == 200:
            ## the wav file is created at the location sent during function call via wavFilePath variable
            ##     example of how filename will look: azureSTT_7_en-CA-HeatherRUS_20191119-121233.wav
            outWavFile = 'azureSTT_' + str(fileNumber) + '_' + inVoiceTypeShortName + '_' + time.strftime("%Y%m%d-%H%M%S") + '.wav'
            with open(wavFilePath + outWavFile, 'wb') as audio:
                audio.write(response.content)
                #print(f"\nSuccess -- file number = {fileNumber}\nfile created: {outWavFile}")
                logging.warning(f"\nSuccess -- file number = {fileNumber}\nfile created: {outWavFile}")
                counters['countAudioConversionSuccess'] += 1
        else:
            #print(f"\nFAILED -- file number = {fileNumber}\nresponse.status_code: {str(response.status_code)}\nsentence=\n{self.tts}")
            logging.warning(f"\nFAILED -- file number = {fileNumber}\nresponse.status_code: {str(response.status_code)}\nsentence=\n{self.tts}")
            counters['countAudioConversionFailed'] += 1
        #
        return response.status_code, outWavFile
    #
    def get_voices_list(self):
        #base_url = 'https://westus.tts.speech.microsoft.com/'
        base_url = 'https://westeurope.tts.speech.microsoft.com/'
        path = 'cognitiveservices/voices/list'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
        }
        response = requests.get(constructed_url, headers=headers)
        if response.status_code == 200:
            print("\nAvailable voices: \n" + response.text)
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
    #
    def set_text_to_convert(self, inText):
        if isinstance(inText, str):
            self.tts = inText
            return True
        else:
            return False
    #
####
### ----------------- FUNCTIONs AND CLASS DEFINITIONS  END  ------------- ###
###
### ------------------- MAIN LOGIC STARTS HERE  -------------- ###
#
## check all the command line arguments and assign variables, 13 expected including scriptname
print(f"\n\n")
if len(sys.argv) != 13:
    print(f"ERROR: number of command line arguments entered = {len(sys.argv)}")
    print(f"ERROR: Including scriptname, expected exactly 13 command line arguments in this format:")
    print(f"\npython </script/folder/path/<programName.py> </input/file/with/path/filename.csv> <rowsToRead> <rowsToSkip> </output/file/path/wavsHere/> </output/file/path/csvs/> </outputFileNameForDeepspeech.csv> </outputFileNameNOTForDeepspeech.csv> <apiCallThrottleLimit> <apiCallThrottleSleepTime in Seconds> <statusRowPrintFreq> <fileNumber> </path/for/logFile/logFileName.log>\n")
    print(f"\nExiting program with return code = 10\n")
    exit(10)
#
try:
    inPdFile                 = sys.argv[1]
    rowsToRead               = int(sys.argv[2])
    rowsToSkip               = int(sys.argv[3])
    outWavFilesPath          = sys.argv[4]
    outFilePath              = sys.argv[5]
    outFileName4Deepspeech   = sys.argv[6]
    outFileNameFullData      = sys.argv[7]
    apiCallThrottleLimit     = int(sys.argv[8])
    apiCallThrottleSleepTime = int(sys.argv[9])
    statusRowPrintFreq       = int(sys.argv[10])
    fileNumber               = int(sys.argv[11])
    logFilenameWithPath      = sys.argv[12]
except:
    print(f"ERROR: error assigning the arguments to variables.")
    print(f"Exiting program with return code = 11\n")
    exit(11)
#
# check input file exists
if os.path.isfile(inPdFile):
    print(f"Found input file.")
else:
    print(f"ERROR: Input file not found here: {inPdFile}")
    print(f"Exiting program with return code = 12\n")
    exit(12)
#
print(f"\nThe command line arguments assigned to variables as follows:\n")
print(f"\t1) Input File: inPdFile = {inPdFile}")
print(f"\t2) Number of rows to read: rowsToRead = {rowsToRead}")
print(f"\t3) Number of rows to skip: rowsToSkip = {rowsToSkip}")
print(f"\t4) Wav files to be saved here: outWavFilesPath = {outWavFilesPath}")
print(f"\t5) Ouput files to be saved here: outFilePath = {outFilePath}")
print(f"\t6) Output file for Deepspeech: outFileName4Deepspeech = {outFileName4Deepspeech}")
print(f"\t7) Output file NOT for Deepspeech: outFileNameFullData = {outFileNameFullData}")
print(f"\t8) Number of API calls before throttling: apiCallThrottleLimit = {apiCallThrottleLimit}")
print(f"\t9) Throttle sleep time: apiCallThrottleSleepTime = {apiCallThrottleSleepTime}")
print(f"\t10)Print Frequency for status tracking: statusRowPrintFreq = {statusRowPrintFreq}")
print(f"\t11)Filenumber to begin output file tags: fileNumber = {fileNumber}")
print(f"\t12)Logfile will be here: logFilenameWithPath = {logFilenameWithPath}")
#
print(f"\nProceeding to main logic.\n")
#
## now main logic starts
#
## https://www.patricksoftwareblog.com/python-logging-tutorial/
logging.basicConfig(level=logging.WARNING, filename=logFilenameWithPath,                      \
    filemode='w', format='%(asctime)s : %(message)s')
#
logging.warning(f"\nThe command line arguments assigned to variables as follows:\n")
logging.warning(f"\t1) Input File: inPdFile = {inPdFile}")
logging.warning(f"\t2) Number of rows to read: rowsToRead = {rowsToRead}")
logging.warning(f"\t3) Number of rows to skip: rowsToSkip = {rowsToSkip}")
logging.warning(f"\t4) Wav files to be saved here: outWavFilesPath = {outWavFilesPath}")
logging.warning(f"\t5) Ouput files to be saved here: outFilePath = {outFilePath}")
logging.warning(f"\t6) Output file for Deepspeech: outFileName4Deepspeech = {outFileName4Deepspeech}")
logging.warning(f"\t7) Output file NOT for Deepspeech: outFileNameFullData = {outFileNameFullData}")
logging.warning(f"\t8) Number of API calls before throttling: apiCallThrottleLimit = {apiCallThrottleLimit}")
logging.warning(f"\t9) Throttle sleep time: apiCallThrottleSleepTime = {apiCallThrottleSleepTime}")
logging.warning(f"\t10)Print Frequency for status tracking: statusRowPrintFreq = {statusRowPrintFreq}")
logging.warning(f"\t11)Filenumber to begin output file tags: fileNumber = {fileNumber}")
logging.warning(f"\t12)Logfile will be here: logFilenameWithPath = {logFilenameWithPath}")
#
logging.warning(f"\nProceeding to main logic.\n")
#
## track how many characters were sent to Azure TTS
## Paid version allows 20 concurrent requests  (free allows only 1)
## https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/
## Costs for Standard TTS:
## Paid version - 4$ per 1 million characters
overallCharCountTrack = 0
#
## Read the input file.
#
# The file has these three columns in a csv format:
#             sentence,pageNum,sentenceLen
#
#inFilePath = '/home/rohit/dpspTraining/data/wavFiles/azure1/pdfExtraction/'
#inFileName = 'System_800xA_Summary.pdf_extractedText_4.csv'
#inPdFile = inFilePath + inFileName
#
## The output file expected for the Deepspeech training has three columns:
#             wav_filename,wav_filesize,transcript
#
print(f"\n\n")
logging.warning(f"\n\n")
myStr = f"\n    *************************************************************** " + \
      f"\n    Input file =\n{inPdFile}" + \
      f"\n    *************************************************************** " + \
      f"\n\n"
print(f"{myStr}")
logging.warning(f"{myStr}")
#
colsToReadIn = ['sentence']
#
# set rowsToRead = -1 to read the whole dataframe in one shot, else specify the number accordingly
#rowsToRead = -1
#rowsToRead = 2
#rowsToSkip = 5
if rowsToRead == -1:
    dfIn = pd.read_csv( inPdFile, sep=',', usecols = colsToReadIn, skiprows = range(1, rowsToSkip+1), header = 0, low_memory=False )
else:
    dfIn = pd.read_csv( inPdFile, sep=',', nrows = rowsToRead, usecols = colsToReadIn, skiprows = range(1, rowsToSkip+1), header = 0, low_memory=False )
#
myStr = f'\n\t# Rows read into dataframe = {rowsToRead if rowsToRead != -1 else "all the rows"}' + \
      f"\n\t# Rows Skipped = {rowsToSkip}" + \
      f"\n\tdfIn.shape = {dfIn.shape}"
print(f"{myStr}")
logging.warning(f"{myStr}")
#
## The output file expected for the Deepspeech training has three columns:
#             wav_filename,wav_filesize,transcript
#
#outWavFilesPath = '/home/rohit/dpspTraining/data/wavFiles/azure1/pdfExtraction/convertedWavs/'
#
#outFilePath = '/home/rohit/dpspTraining/data/wavFiles/azure1/pdfExtraction/convertedWavsCsvFile/'
#
# file for Deepspeech -- only 3 columns
#outFileName4Deepspeech = 'System_800xA_Summary.pdf_extractedText_4_forDS.csv'
# file for full data -- all 4 columns -- including the Short Name of Voice Type
#outFileNameFullData = 'System_800xA_Summary.pdf_extractedText_4_NOT_forDS.csv'
#
## amount of time after which to request a new token
accessTokenRecheckInSeconds = 300
## number of api calls after which to sleep
#apiCallThrottleLimit = 20
## time in seconds to sleep during throttling
#apiCallThrottleSleepTime = 60
#
## how frequently should it print status to console -- based on row read in from input file
#statusRowPrintFreq = 50
#
counters = { 'countRowsReadIn': 0 , 'countRowsWrittenToDfOut': 0 , 'countAudioConversionSuccess': 0 , \
            'countAudioConversionFailed': 0 , 'countInvalidSentences': 0, 'countApiCallsMade': 0}
#
## When the final output CSV file is written for Deepspeech, then the voiceShortName will not be included.
#
dfOutColumns = [ 'voiceShortName' , 'wav_filename' , 'wav_filesize' , 'transcript']
#
dfOutColumnsDtypes = [str, str, int, str]
dfOut = pd.DataFrame(columns = dfOutColumns)
#dfOut = dfOut.astype({"wav_filename": str, "wav_filesize": int, 'transcript': str})
dfOut = dfOut.astype(dict(zip(dfOutColumns, dfOutColumnsDtypes)))
#
## add slash at end if not there already
if outFilePath[-1] != '/':
    outFilePath = outFilePath + '/'
if outWavFilesPath[-1] != '/':
    outWavFilesPath = outWavFilesPath + '/'
#
myStr = f'\nWav files will be saved here:\n{outWavFilesPath}' + \
      f'\nOutput CSV files will be saved here:\n{outFilePath}'
print(f"{myStr}")
logging.warning(f"{myStr}")
#
## create the object for the TTS processing
app = TextToSpeech('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
app.get_token()
#
myStr = f"\nFirst time Access Token = \n{app.access_token}" + \
    f"\nFirst time Access Token Start Time = \n{app.access_token_startTime}\n"
print(f"{myStr}")
logging.warning(f"{myStr}")
#
#voiceTypeShortName = 'en-US-BenjaminRUS'
voiceTypeShortNameList = [ 'en-AU-Catherine', 'en-AU-HayleyRUS', 'en-CA-HeatherRUS', 'en-CA-Linda', \
                          'en-GB-George-Apollo', 'en-GB-HazelRUS', 'en-GB-Susan-Apollo', \
                          'en-IN-Heera-Apollo', 'en-IN-PriyaRUS', 'en-IN-Ravi-Apollo', \
                          'en-US-BenjaminRUS', 'en-US-JessaRUS', 'en-US-ZiraRUS' ]
print(f"\n# Voice Short Names input = {len(voiceTypeShortNameList)}.\n\nThe names of the voices are:")
logging.warning(f"\n# Voice Short Names input = {len(voiceTypeShortNameList)}.\n\nThe names of the voices are:")
for voiceType in voiceTypeShortNameList:
    print(f"\t{voiceType}")
    logging.warning(f"\t{voiceType}")
print(f"\n\n")
logging.warning(f"\n\n")
#
myStr = f'\n' + \
    f'\n    ***************************************************************' * 2 + \
    f'\n\tProcessing input data....\n\n' + \
    f'\n    ***************************************************************' * 2 + \
    f'\n\n'
print(f"{myStr}")
logging.warning(f"{myStr}")
#
## fileNumber set to rowsToSkip. It is increased in loop immediately and we want numbering to start
##         from the corresponding first row position being processed which is = rowsToSkip + 1
#fileNumber = rowsToSkip
## NOTE: for command line version, expect user to input exactly the number to start with, so decrementing by one first
fileNumber -= 1
#
## this should be remain 0 ideally, the flag for 429 will tell if 429 error occurred
processingReturnCode = 0
#
## ideally this should never have been set to True
flagRc429Encountered = False  ## check any Azure call had 429 response code
#
## start processing the sentences from dfin for each voice type required
for row in dfIn.itertuples():
    #
    if processingReturnCode != 0 or flagRc429Encountered == True:
        break
    #
    counters['countRowsReadIn'] += 1
    fileNumber += 1  ## same file number should remain for a particular sentence
    #
    ## Convert named tuple to dictionary
    ## using as per this link: https://thispointer.com/pandas-6-different-ways-to-iterate-over-rows-in-a-dataframe-update-while-iterating-row-by-row/
    dictRow = row._asdict()
    #
    textToConvert = dictRow['sentence']
    #
    ## log each sentence , but print a status only as per input frequency
    myStr = f"\n ----------------------- **** Processing sentence # {counters['countRowsReadIn']} *** -----------------------" + \
            f"\nSentence =\n{textToConvert}"
    logging.warning(f"{myStr}")
    ## print which row is being processed every so long
    if counters['countRowsReadIn'] % statusRowPrintFreq == 0 or counters['countRowsReadIn'] == 1:
        print(f"{myStr}")
    #
    if textToConvert is not None and textToConvert != '':
        if app.set_text_to_convert(textToConvert) == False:
            print(f"\n\nFatal Error: Problem setting text in the app object.\n\n")
            logging.warning(f"\n\nFatal Error: Problem setting text in the app object.\n\n")
            processingReturnCode = 100
            break
    else:
        logging.warning(f"\nSentence was None or empty string. Continuing to next sentence.\n")
        counters['countInvalidSentences'] += 1
        continue ## move to the next sentence
    #
    ## sentence is fine and set in the app object, so now convert for each type of voice
    #
    for idxVoiceType, voiceTypeShortName in enumerate(voiceTypeShortNameList):
        #print(f"\n **** Voice = {idxVoiceType + 1} *** \t\tvoice Short Name = {voiceTypeShortName}")
        logging.warning(f"\n **** Voice = {idxVoiceType + 1} *** \t\tvoice Short Name = {voiceTypeShortName}")
        #
        ## throttling to avoid response 429 from Azure
        ## https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/faq-text-to-speech
        if counters['countApiCallsMade'] != 0 and counters['countApiCallsMade'] % apiCallThrottleLimit == 0:
            #print(f"\nSleeping for {apiCallThrottleSleepTime} seconds, api calls made so far = {counters['countApiCallsMade']}")
            logging.warning(f"\nSleeping for {apiCallThrottleSleepTime} seconds, api calls made so far = {counters['countApiCallsMade']}")
            time.sleep(apiCallThrottleSleepTime)
            #print(f"\nFinished sleep, continuing....\n")
            logging.warning(f"\nFinished sleep, continuing....\n")
        #
        ## check the current token issue time. If more than threshold time has passed, then get new token again.
        app.check_tokenGenerationTime_and_regenerateIfRequired(accessTokenRecheckInSeconds)
        #
        ## make api call to convert audio. also increments the counters for audio conversion
        ##      success, failed, api calls made.
        overallCharCountTrack += len(textToConvert)
        try:
            appSaveAudioRespCode, savedWavFilename = app.save_audio( voiceTypeShortName, fileNumber, outWavFilesPath )
        except:
            ## unexpected issue (e.g. had a OSError: Tunnel connection failed: 502 Could not relay message upstream)
            ##     this killed process midway -> no output CSV file and NO REJOIN with main process.
            ##     so main process did not proceed and waits infinitely.
            ## if there are already any entries in dfOut then write to CSV file and rejoin the main process
            processingReturnCode = 11000 ## using huge value
            myStr = f"\n" + \
                    "\n ------ Unhandled exception occurred during save_audio call ------ " * 2 + \
                    "\n"
            print(f"{myStr}")
            logging.warning(f"{myStr}")
            break
            #
        ## azure api call returns with response code 200 if all is ok.
        ##       overwriting processingReturnCode only if it is serious.
        if appSaveAudioRespCode != 200:
            if appSaveAudioRespCode == 429:
                flagRc429Encountered = True
                break
            #
            ## its not 429, something serious
            print(f"\n\nProblem with audio conversion. Azure response Status Code = {appSaveAudioRespCode}\n\n")
            logging.warning(f"\n\nProblem with audio conversion. Azure response Status Code = {appSaveAudioRespCode}\n\n")
            processingReturnCode = appSaveAudioRespCode
            break
        #
        ## no major problems encountered so far, get the filesize
        try:
            ## get the filesize and make entry in dataframe for output file
            fullPathWavFile = outWavFilesPath + savedWavFilename
            wavFileSize = os.path.getsize(fullPathWavFile)
            dfOutColumnsData = [ voiceTypeShortName, fullPathWavFile , wavFileSize , textToConvert ]
            dfOut = dfOut.append( dict(zip(dfOutColumns, dfOutColumnsData)) , ignore_index = True)
            counters['countRowsWrittenToDfOut'] += 1
        except:
            print(f"\n\nFatal Error: Problem getting the wav file size or making entry for output dataframe.\n\n")
            logging.warning(f"\n\nFatal Error: Problem getting the wav file size or making entry for output dataframe.\n\n")
            processingReturnCode = 300
            break
        #
    #
#
if processingReturnCode != 0:
    myStr = f"\n" + \
        f"\nFatal Error: " + \
            f"### PROBLEM " * 4 + \
            f"\nFatal Error: " + \
            f"### PROBLEM " * 4
    print(f"{myStr}")
    logging.warning(f"{myStr}")
    #
myStr = f"\n\nSentence+voiceType processing done." + \
    f"\nprocessingReturnCode = {processingReturnCode}\n" + \
    f"\n\nCreating output files...\n"
print(f"{myStr}")
logging.warning(f"{myStr}")
#
# Write full output file including voice type short name
dfOut.to_csv(outFilePath + outFileNameFullData, index = False)
#
# Write output file for Deepspeech training -- only the three required columns
dfOutForFile = dfOut[['wav_filename' , 'wav_filesize' , 'transcript']]
dfOutForFile.to_csv(outFilePath + outFileName4Deepspeech, index = False)
#
# Print the summary info
#
print(f"\n\nFull Data CSV file created here:\n{outFilePath + outFileNameFullData}")
print(f"\nDeepspeech training CSV file created here:\n{outFilePath + outFileName4Deepspeech}")
print(f"\nWAV files location:\n{outWavFilesPath}")
#
print(f"\n\n ########## SUMMARY ######### SUMMARY ######### SUMMARY #########\n")
print(f"\n# Rows Read = {rowsToRead}\t\t# Rows Skipped = {rowsToSkip}")
print(f"\n# Sentences in input file                    = {len(dfIn)}")
print(f"\n# Voices types input                         = {len(voiceTypeShortNameList)}")
print(f"\n# Sentences read in                          = {counters['countRowsReadIn']}")
print(f"\n# Invalid Sentences                          = {counters['countInvalidSentences']}")
print(f"\n  There should be these number of rows in the output file, if all went well:")
print(f"    numSentences * numVoiceTypes               = {len(dfIn) * len(voiceTypeShortNameList)}")
print(f"\n  counters['countRowsWrittenToDfOut']        = {counters['countRowsWrittenToDfOut']}")
print(f"\n# rows in dfOut                              = {len(dfOut)}")
print(f"\n# Successful audio conversion                = {counters['countAudioConversionSuccess']}")
print(f"\n# Failed audio conversion                    = {counters['countAudioConversionFailed']}")
print(f"\n# API calls made to Azure                    = {counters['countApiCallsMade']}")
print(f"\n# Characters processed                       = {overallCharCountTrack}")
print(f"\nProcessing return code                       = {processingReturnCode}")
print(f"\n  Status flag for 429 error                  = {flagRc429Encountered}")
#
logging.warning(f"\n\nFull Data CSV file created here:\n{outFilePath + outFileNameFullData}")
logging.warning(f"\nDeepspeech training CSV file created here:\n{outFilePath + outFileName4Deepspeech}")
logging.warning(f"\nWAV files location:\n{outWavFilesPath}")
#
logging.warning(f"\n\n ########## SUMMARY ######### SUMMARY ######### SUMMARY #########\n")
logging.warning(f"\n# Rows Read = {rowsToRead}\t\t# Rows Skipped = {rowsToSkip}")
logging.warning(f"\n# Sentences in input file                    = {len(dfIn)}")
logging.warning(f"\n# Voices types input                         = {len(voiceTypeShortNameList)}")
logging.warning(f"\n# Sentences read in                          = {counters['countRowsReadIn']}")
logging.warning(f"\n# Invalid Sentences                          = {counters['countInvalidSentences']}")
logging.warning(f"\n  There should be these number of rows in the output file, if all went well:")
logging.warning(f"    numSentences * numVoiceTypes               = {len(dfIn) * len(voiceTypeShortNameList)}")
logging.warning(f"\n  counters['countRowsWrittenToDfOut']        = {counters['countRowsWrittenToDfOut']}")
logging.warning(f"\n# rows in dfOut                              = {len(dfOut)}")
logging.warning(f"\n# Successful audio conversion                = {counters['countAudioConversionSuccess']}")
logging.warning(f"\n# Failed audio conversion                    = {counters['countAudioConversionFailed']}")
logging.warning(f"\n# API calls made to Azure                    = {counters['countApiCallsMade']}")
logging.warning(f"\n# Characters processed                       = {overallCharCountTrack}")
logging.warning(f"\nProcessing return code                       = {processingReturnCode}")
logging.warning(f"\n  Status flag for 429 error                  = {flagRc429Encountered}")
#
print(f"\n\n\nNormal exit\n")
logging.warning(f"\n\n\nNormal exit\n")
exit(0)
### -------------------  MAIN LOGIC ENDS HERE   -------------- ###