"""
filename:enron_parser.py
author:mdfra8

This file contains the EnronParser object. It iterates through the maildir folder and parses the emails.
It then holds the emails in a dictionary, with key:value pairs for the fields that the parser has been able to identify.

Assumption - I'm assuming that the folder maildir is in the same directory as this script is being run in.
todo - Improve to allow object to be initialised with a dynamic root directory
todo - Imrpove to not hold ALL the emails in memory, i.e. turn into generator
"""
import json
import os
import sys

class EnronParser:

    def __init__(self):
        """
        Initialises the Enron Parser Object.
        """
        file_finder = self.pathfinder()         # initialise this generator
        self.emp_count = 0                      # how many folders exist in the root directory
        self.progress = float(0)                # keep track of progress through the folders
        self.emails = []                        # all the parsed emails are stored here

        for each in file_finder:                # iterate through each email
            email = {}                          # this is a dictionary that will contain the parsed email

            if each:
                email_file = open(each, encoding="latin-1")         # open the file
                id = email_file.readline().replace('Message-ID: ','')   # first line is always an ID
                datetime = email_file.readline().replace('Date: ','')   # second line is always a timestamp
                from_addr = email_file.readline().replace('From: ','')  # third line is the From address

                # Add the header fields that we just read
                email['id'] = id
                email['datetime'] = datetime
                if 'from' not in email.keys():
                    email['from'] = from_addr
                else:
                    raise("Multiple from addresss")

                prev = 'from'                   # just in case there are multiple From Addresses

                for line in email_file:         # iterate through lines in the email
                    line = line.replace('\t','')        # strip out \t as part of data cleaning
                    prev = self.classify_line(line, prev)      # this function classifies where this line should go
                    line = line.replace('\n','')     # data cleaning
                    line = line.replace('\r','')     # data cleaning
                    if len(line) > 0 and line[0] == " ":               # data cleaning
                        line = line[1:]

                    if prev is not 'body':      # If there is a label (like From:), remove it
                        line = line.replace(prev+':','')

                    # adds the line to the correct key:value pair in the email dictionary
                    if prev in email.keys():
                        email[prev] = email[prev] + [line]
                    else:
                        email[prev] = [line]

                email['body'] = ''              # don't save the body - not needed
                self.emails.append(email)       # add the current email to the list of emails.


    def pathfinder(self):
        """
        This is a generator that feeds the file path for each email file.
        :return:
        """
        path = '../maildir/'                 # see assumption in docstring
        employee_folders = os.listdir(path)     # grab a list of folders in the current directory
        self.emp_count = len(employee_folders)          # sanity check
        for emp_folder in employee_folders:     # go through each folder (employee folders)
            self.progress += 1
            crnt_emp_path = path + emp_folder   # path of the current employee's folder
            email_folders = os.listdir(crnt_emp_path)
            for email_folder in email_folders:
                crnt_emp_folder = crnt_emp_path +'/' + email_folder
                progress = "\rCurrently parsing {} of {} employees: {}/{}".format(int(self.progress), self.emp_count,str(emp_folder),email_folder)
                sys.stdout.write(progress)
                sys.stdout.flush()
                if os.path.isdir(crnt_emp_folder):
                    try:
                        crnt_emp_emails = os.listdir(crnt_emp_folder)    # grab all the filenames in the inbox
                        # starting to go each email in the directory 'inbox'

                        for email in crnt_emp_emails:
                            email_path = crnt_emp_folder + '/' + email
                            if not os.path.isdir(email_path):  # make sure we're not trying to open a folder
                                # email_file = open(email_path)
                                yield email_path

                    except FileNotFoundError as err:
                        print(err)
                        yield False
                else:
                    yield crnt_emp_folder

    @staticmethod
    def classify_line(line, prev):
        """
        Line classifier. This looks for key field identifiers that we know about, and if the field is identified,
        returns that field name. If not, it assumes that the line is a continuation of the previous field,
        or it is a part of the body of the email.
        :param line:
        :param prev:
        :return:
        """
        check_one = line.split(':')
        key_check = check_one[0].capitalize()
        ez_keys = ['To', 'Subject', 'Cc', 'Mime-Version', 'Content-Type', 'Content-Transfer-Encoding', 'Bcc',
                   'X-From','X-To', 'X-cc', 'X-bcc', 'X-Folder', 'X-Origin', 'X-FileName']
        if key_check in ez_keys:
            return key_check

        elif key_check == '\n':
            return prev

        elif prev == 'X-FileName':
            return 'body'

        elif prev == 'body':
            return 'body'

        else:
            return 'body'

    def get_emails(self):
        """
        returns the Emails that have been parsed.
        :return:
        """
        return self.emails


    def get_email_json(self):
        return json.dumps(self.emails)
