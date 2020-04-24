import string
import random
import uuid
import pytest
import os
import sys

sys.path.append("{}/{}".format(os.getcwd(), "candig_authz_service"))
sys.path.append(os.getcwd())

from candig_authz_service import orm
from candig_authz_service.__main__ import app
from candig_authz_service.api import operations


@pytest.fixture(name="test_client")
def load_test_client(db_filename="operations.db"):
    try:
        orm.close_session()
        os.remove(db_filename)
    except FileNotFoundError:
        pass
    except OSError:
        pass

    context = app.app.app_context()

    with context:
        orm.init_db("sqlite:///" + db_filename)
        app.app.config["BASE_DL_URL"] = "http://127.0.0.1"

    return context


def test_get_authz_levels(test_client):
    """
    Test 'get_authz' method
    """
    pass
       

def test_get_authz_levels_with_projects(test_client):
    """
    Test 'get_authz' method when specifying the project
    """
    pass
