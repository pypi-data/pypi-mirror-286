from glapi import configuration
from glapi.connection import GitlabConnection

def test():

    ###########
    # CONNECT #
    ###########

    # no params
    assert GitlabConnection().query(endpoint="version")
