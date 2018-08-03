"""
filename:restruct_data.py
author:mdfra8
Assumption - I'm assuming that the folder maildir is in the same directory as this script is being run in.
"""
import os, sys


class Emails:

    def __init__(self):
        file_finder = self.pathfinder()
        self.emp_count = 0
        self.progress = float(0)
        self.emails = []

        for each in file_finder:
            email = {}
            if each:
                # print(each)
                email_file = open(each)
                id = email_file.readline()
                datetime = email_file.readline()
                from_addr = email_file.readline()
                prev = 'from'
                for line in email_file:
                    # line = email_file.readline()

                    prev = self.classify_line(line, prev)
                    line = line.strip('\n')
                    if prev in email.keys():
                        email[prev] = email[prev] + line
                    else:
                        email[prev] = line

                self.emails.append(email)
                # to_addr can be multiline, it can also not be included. need to start identifying and seperating.
                # subject can also be multiline

    def pathfinder(self):
        path = "./maildir/"  # see assumption in docstring
        employee_folders = os.listdir(path)  # grab a list of folders in the current directory
        self.emp_count = len(employee_folders)          # sanity check
        for emp_folder in employee_folders:  # go through each folder (employee folders)
            self.progress += 1
            progress = "\rCurrently parsing {} of {} employees".format(int(self.progress),self.emp_count)
            sys.stdout.write(progress)
            sys.stdout.flush()

            crnt_emp_inbox = path + emp_folder + '/inbox'  # append /inbox to the path
            try:
                crnt_emp_emails = os.listdir(crnt_emp_inbox)  # grab all the filenames in the inbox
                # print(crnt_emp_inbox)
                # starting to go each email in the directory 'inbox'

                for email in crnt_emp_emails:
                    email_path = crnt_emp_inbox + '/' + email
                    if not os.path.isdir(email_path):  # make sure we're not trying to open a folder
                        # email_file = open(email_path)
                        yield email_path

            except FileNotFoundError:
                yield False


    def classify_line(self,line, prev):
        check_one = line.split(':')
        key_check = check_one[0]
        ez_keys = ['To', 'Subject', 'Cc', 'Mime-Version', 'Content-Type', 'Content-Transfer-Encoding', 'Bcc',
                   'X-From'
                   'X-To', 'X-cc', 'X-bcc', 'X-Folder', 'X-Origin', 'X-FileName']
        if key_check in ez_keys:
            return key_check

        elif key_check == '\n':
            return prev

        elif prev == 'X-FileName':
            return 'body'

        elif prev == 'body':
            return 'body'

        else:
            pass
            # print(key_check)

    def get_emails(self):
        return self.emails


emails = Emails()
