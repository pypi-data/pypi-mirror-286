import os

from glapi.user import GitlabUser

GITLAB_EVENT_ACTIONS = [d.strip() for d in os.environ["GITLAB_EVENT_ACTIONS"].split(",")]
GITLAB_USER_ID = os.environ["GITLAB_USER_ID"]

def test():

    # initialize
    gu = GitlabUser(id=GITLAB_USER_ID)

    assert gu.user is not None

    ##################
    # EXTRACT_EVENTS #
    ##################

    result = gu.extract_events(actions=GITLAB_EVENT_ACTIONS)

    assert isinstance(result, list)

    ##################
    # EXTRACT_ISSUES #
    ##################

    result = gu.extract_issues(scope="created_by_me")

    assert isinstance(result, list)

    ##########################
    # EXTRACT_MERGE_REQUESTS #
    ##########################

    result = gu.extract_merge_requests(scope="created_by_me")

    assert isinstance(result, list)

    ####################
    # EXTRACT_PROJECTS #
    ####################

    result = gu.extract_projects()

    assert isinstance(result, list)
