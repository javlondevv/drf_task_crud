from django.db.models import *


class Task(Model):
    title = CharField(max_length=255)
    description = TextField()
    completed = BooleanField(default=False)

    def __str__(self):
        return self.title
