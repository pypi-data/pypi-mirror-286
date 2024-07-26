import os

from glapi.project import GitlabProject

GITLAB_EVENT_ACTIONS = [d.strip() for d in os.environ["GITLAB_EVENT_ACTIONS"].split(",")]
GITLAB_PROJECT_ID = os.environ["GITLAB_PROJECT_ID"]

def test():

    # initialize
    gp = GitlabProject(id=GITLAB_PROJECT_ID)

    assert gp.project is not None

    ##################
    # EXTRACT_EVENTS #
    ##################

    result = gp.extract_events(actions=GITLAB_EVENT_ACTIONS)

    assert isinstance(result, list)

    ##################
    # EXTRACT_ISSUES #
    ##################

    result = gp.extract_issues()

    assert isinstance(result, list)
