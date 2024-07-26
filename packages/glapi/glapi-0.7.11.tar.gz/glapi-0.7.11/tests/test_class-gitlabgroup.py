import os

from glapi.group import GitlabGroup

GITLAB_EVENT_ACTIONS = [d.strip() for d in os.environ["GITLAB_EVENT_ACTIONS"].split(",")]
GITLAB_GROUP_ID = os.environ["GITLAB_GROUP_ID"]

def test():

    # initialize
    gg = GitlabGroup(id=GITLAB_GROUP_ID)

    assert gg.group is not None

    #################
    # EXTRACT_EPICS #
    #################

    result = gg.extract_epics()

    assert isinstance(result, list)

    ##################
    # EXTRACT_ISSUES #
    ##################

    result = gg.extract_issues()

    assert isinstance(result, list)

    ####################
    # EXTRACT_PROJECTS #
    ####################

    result = gg.extract_projects()

    assert isinstance(result, list)

    #################
    # EXTRACT_USERS #
    #################

    result = gg.extract_users()

    assert isinstance(result, list)
