import os

from glapi.epic import GitlabEpic
from utilities import synthetic_epics

GITLAB_EPIC_ID = os.environ["GITLAB_EPIC_ID"] if "GITLAB_EPIC_ID" in os.environ else None

def test():

    # initialize
    ge = GitlabEpic(id=GITLAB_EPIC_ID) if GITLAB_EPIC_ID else GitlabEpic(epic=synthetic_epics()[0])

    assert ge.epic is not None

    ##################
    # EXTRACT_ISSUES #
    ##################

    result = ge.extract_issues()

    assert True

    #################
    # EXTRACT_NOTES #
    #################

    result = ge.extract_notes()

    assert True
