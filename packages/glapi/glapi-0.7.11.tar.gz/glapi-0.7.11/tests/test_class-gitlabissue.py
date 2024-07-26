import os

from glapi.issue import GitlabIssue
from utilities import synthetic_epics

GITLAB_ISSUE_ID = os.environ["GITLAB_ISSUE_ID"]

def test():

    # initialize
    gi = GitlabIssue(id=GITLAB_ISSUE_ID)

    assert gi.issue is not None

    #################
    # EXTRACT_LINKS #
    #################

    result = gi.extract_links()

    assert True

    #################
    # EXTRACT_NOTES #
    #################

    result = gi.extract_notes()

    assert True

    ########################
    # EXTRACT_PARTICIPANTS #
    ########################

    result = gi.extract_participants()

    assert True
