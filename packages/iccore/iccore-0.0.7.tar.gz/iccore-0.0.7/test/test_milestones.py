import json

from iccore.project import Milestone
from iccore.serialization import write_json, read_json

def test_milestone():

    milestone = Milestone()

    milestone.title = "My Milestone"
    milestone.description = "My Milestone description"
    milestone.start_date = "10-07-24"
    milestone.due_date = "12-07-24"

    milestone_serialized = str(milestone)
    milestone_json = json.loads(milestone_serialized)

    milestone_cpy = Milestone(milestone_json)

    assert milestone_cpy.title == milestone.title
    assert milestone_cpy.start_date == milestone.start_date
