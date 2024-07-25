import json


class Issue:

    def __init__(self):
        self.title = ""
        self.description = ""
        self.start_date = ""
        self.due_date = ""
        self.assignee = None


class Milestone:

    def __init__(self, json=None):
        self.title = ""
        self.description = ""
        self.start_date = None
        self.due_date = None
        self.issues = []
        self.raw = json

        if json:
            self.load(json)

    def load(self, json):
        self.raw = json

        self.title = json["title"]
        self.description = json["description"]
        self.start_date = json["start_date"]
        self.due_date = json["due_date"]

    def serialize(self):
        return {
            "title": self.title,
            "description": self.description,
            "start_date": self.start_date,
            "due_date": self.due_date,
        }

    def __str__(self):
        return json.dumps(self.serialize())
