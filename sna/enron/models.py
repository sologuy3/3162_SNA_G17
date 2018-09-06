import sys
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()


class Person(models.Model):
    name = models.CharField(max_length=100)
    email_address = models.EmailField(null=False)

    @property
    def organisation(self):
        return self.email_address.split("@")[1].split(".")[0]

    def __str__(self):
        return self.email_address

class Email(models.Model):
    id = models.CharField(max_length=100, primary_key=True)

    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Person, related_name="recipients")
    # ccs = models.ManyToManyField(Person, related_name="ccs")
    # bccs = models.ManyToManyField(Person, related_name="bccs")

    subject = models.CharField(max_length=200)
    body = models.TextField()

    time_sent = models.DateField()
