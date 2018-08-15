import pdb

from data.models import Person, Email


def main():
    emails = Emails()

    for inmem_email in emails:

        if Person.objects.filter(email=inmem_email['From']).exists():
            # TODO: Everything

        db_email = Email()
        db_email.id = inmem_email['id']
        db_email.cc = inmem_email['CC']
        db_email.bcc = inmem_email['Bcc']
        db_email.to = inmem_email['To']
        db_email.authors = inmem_email['From']


    pdb.set_trace()

if __name__ == "__main__":
    main()