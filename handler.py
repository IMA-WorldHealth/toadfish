#!/usr/bin/env python3

import sys
import requests
import logging
import os

logging.basicConfig(filename='sms.log',level=logging.INFO)

from dotenv import load_dotenv
load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")

PATH = "/sms"
DESTINATION = SERVER_URL + PATH
DELIMITER = "+"


method = sys.argv[1]
message = sys.argv[2]

def main():
    """
    Handles the text messages received from smstools, parses them, and
    forwards them on to the online ima-data server.
    """

    # only operate on recieved messages, not sent messages.
    if method != "RECEIVED":
        logging.info('Called with invalid path %s' % method);
        return

    logging.info('Opening file %s for reading' % message);
    with open(message, 'r') as sms:
        contents = sms.read()
        parseSMSMessage(contents)



def parseSMSMessage(sms):
    lines = [txt for txt in sms.split('\n') if txt != '']
    submission = lines.pop()

    logging.info('Extracted submission %s' % submission);

    elements = submission.split(DELIMITER)
    form = elements[0]

    logging.info('Detected for name %s' % submission);

    #generate the kv_map
    kv_map = dict(zip(elements[1::2], elements[2::2]))

    logging.info('Submitting form to server.');

    # send the JSON object to the server
    sendSMSToODKServer(form, kv_map)

    # write to a database the parsed values
    saveSMSMessageInDB(form, sms, kv_map)

    return

def saveSMSMessageInDB(form, sms, kv_map):
    """
    Saves into database the raw message and the interpreted form
    """
    logging.info('TODO - writing values to database.')
    return

def sendSMSToODKServer(form, kv_map):
    """
    Sends the SMS to the ODK server online
    """
    url = DESTINATION + '/' + form

    logging.info('Submitting parsed JSON object %s ' % url)

    response = requests.post(url, data=kv_map)

main()
