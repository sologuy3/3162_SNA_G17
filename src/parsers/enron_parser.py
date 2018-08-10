"""
filename:enron_parser.py
author:mdfra8
Assumption - I'm assuming that the folder maildir is in the same directory as this script is being run in.
"""
import os
import sys
import re

class EnronParser:

    def __init__(self):
        """
        Initialises the Enron Parser Object.
        """
        file_finder = self.pathfinder()
        self.emp_count = 0
        self.progress = float(0)
        self.emails = []

        for each in file_finder:
            email = {}
            if each:
                # print(each)
                email_file = open(each)
                id = email_file.readline().replace('Message-ID: ','')
                datetime = email_file.readline().replace('Date: ','')
                from_addr = email_file.readline().replace('From: ','')
                prev = 'from'
                for line in email_file:
                    line = line.replace('\t','')

                    prev = self.classify_line(line, prev)
                    line = line.strip('\n')
                    if prev is not 'body':
                        line = line.replace(prev+':','')
                    if prev in email.keys():
                        email[prev] = email[prev] + [line]
                    else:
                        email[prev] = [line]
                email['id'] = id
                email['datetime'] = datetime
                if 'from' not in email.keys():
                    email['from'] = from_addr
                else:
                    raise("Multiple from addresss")

                self.emails.append(email)
                if 'id' in email.keys():
                    print(email['id'])
                if 'datetime' in email.keys():
                    print(email['datetime'])


                # to_addr can be multiline, it can also not be included. need to start identifying and seperating.
                # subject can also be multiline

    def pathfinder(self):
        """
        This is a generator that feeds the file path for each email file.
        :return:
        """
        path = '../../maildir/'                 # see assumption in docstring
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

    @staticmethod
    def classify_line(line, prev):
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
        return self.emails

emails = EnronParser()