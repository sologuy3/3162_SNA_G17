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
import pdb
import sys

import re

from graph_sna.graph.graph import Graph
from graph_sna.graph.node import Node


class EnronParser:

    def __init__(self, loadfromdump=False):
        """
        Initialises the Enron Parser Object.
        """

        if loadfromdump:
            self.emails = json.loads(open('enrondump').read())
            return
        file_finder = self.pathfinder()         # initialise this generator
        self.emp_count = 0                      # how many folders exist in the root directory
        self.progress = float(0)                # keep track of progress through the folders
        self.emails = []                        # all the parsed emails are stored here

        path = '../maildir/'  # see assumption in docstring
        employee_folders = os.listdir(path)  # grab a list of folders in the current directory


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
                email = self.clean(email)
                self.emails.append(email)       # add the current email to the list of emails.
        maildir = path
        folders = os.listdir(path=maildir)
        staff_emails = set("steven.harris@enron.com")  # Add the one annoying edge case by hand...
        to_regex = re.compile("From: ([a-zA-Z]*.[a-zA-Z]*@enron.com)")
        for folder in folders:

            path = maildir + folder
            categories = os.listdir(path)
            sent_folders = [category for category in categories if "sent" in category]
            if len(sent_folders) == 0:
                continue

            # Go through sent folders / sent items and try find a source email address that matches the format
            # john.smith@enron.com
            found_email = False
            for sent_folder in sent_folders:
                for file in os.listdir(path + "/" + sent_folder):
                    infile = open(path + "/" + sent_folder + "/" + file).read()
                    match = to_regex.search(infile)
                    if hasattr(match, "group"):
                        staff_emails.add(match.group(1))
                        found_email = True
                        break
                if found_email:
                    break


        good_emails = []

        for i, inmem_email in enumerate(self.emails):

            if i % 5000 == 0:
                print(str(round(100 * i / len(self.emails), 2)) + "% done")

            inmem_email = self.clean(inmem_email)
            from_email = inmem_email['from']
            if from_email not in staff_emails:
                continue

            if "To" not in inmem_email:
                continue  # Some emails don't have a `To` key?

            to_emails = inmem_email['To']
            valid_to_emails = [addr for addr in to_emails if addr in staff_emails and addr != '']

            if len(valid_to_emails) == 0:
                continue
            else:
                # print("{} -> {}".format(from_email, valid_to_emails))
                inmem_email['To'] = json.dumps(valid_to_emails)

            good_emails.append(inmem_email)

        print("Out of {} emails, {} were originating from and sent towards {} dataset staff".format(len(self.emails),
                                                                                                 len(good_emails),
                                                                                                    len(staff_emails)))
        self.emails = good_emails
        with open("enrondump", "w") as out:
            out.write(json.dumps(good_emails))

    def generate_graph(self):
        """
        To be used after the data has been saved to an enrondump file by the parser
        :return:
        """

        graph = Graph('Enron')
        emails = json.loads(open('enrondump').read())
        for email in emails:
            sender_email = email['from']
            if graph.has_node_by_label(sender_email):
                sender = graph.get_node_from_label(label=sender_email)
            else:
                sender = Node(label=sender_email)
                graph.add_node(sender)
            recipients = json.loads(email['To'])

            for recipient_email in recipients:
                if graph.has_node_by_label(recipient_email):
                    recipient = graph.get_node_from_label(recipient_email)
                else:
                    recipient = Node(label=recipient_email)
                    graph.add_node(recipient)

                if not graph.has_edge(sender, recipient):
                    graph.add_edge(sender, recipient, 1)
                else:
                    # Increment the weight by 1
                    graph.update_edge(sender, recipient,
                                      graph.get_weight(sender, recipient,) + 1)

        return graph

    @staticmethod
    def clean(email):
        d = {}

        if 'To' in email:
            d['To'] = [to.replace(" ", "") for to in email['To']]

        for k, v in email.items():
            if k == "To":
                continue
            try:
                if isinstance(v, list):
                    d[k] = v[0].replace("\n", "")  # 0th index for first subject line?
                else:
                    d[k] = v.replace("\n", "")
            except Exception as e:
                print(e)

        return d

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

if __name__ == "__main__":
    ep = EnronParser(True)
    emails = ep.get_email_json()
    enron_graph = ep.generate_graph()
    print(len(enron_graph.get_all_nodes()))
    with open('enronsave','w+') as enronsave:
        enronsave.write(enron_graph.get_save())