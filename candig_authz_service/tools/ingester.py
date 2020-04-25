"""
The ingester module provides methods to ingest tsv files
"""

import os
import sys

# from sqlalchemy.exc import IntegrityError

sys.path.append(os.getcwd())

# from candig_authz_service.api.exceptions import FileTypeError  # noqa: E402
# from candig_authz_service.api.exceptions import KeyExistenceError  # noqa: E402
# from candig_authz_service.api.exceptions import HeaderError  # noqa: E402
# from candig_authz_service.orm import init_db, get_engine  # noqa: E402
# from candig_authz_service.orm.models import authorization  # noqa: E402


class Ingester:
    """
    This class ingests a candig-server v1-compatible access_list into the database.
    TODO: Implement this
    """
    def __init__(self, database, patient, sample, tsv_file):
        """Constructor method
        """
        self.db = "sqlite:///" + database
        self.file_type = self.get_type()
        self.engine = self.db_setup()
        self.segments = []
        self.required_headers = [
            'issuer',
            'username',
            'project',
            ]
        self.ingests = {
            "tsv": self.ingest_tsv
        }

    def db_setup(self):
        """
        Connects to the database given using SQLAlchemy Core and
        attempts to query the username provided. Returns the
        engine if successful or an error if the Sample cannot
        be located.

        :raises: KeyExistenceError
        :return: engine object
        :rtype: `~sqlalchemy.engine.Engine`

        TODO: Implement this
        """
        pass

        # init_db(self.db)
        # engine = get_engine()
        # return engine

    def ingest_tsv(self):
        """
        Ingest the candig-server v1 compatible tsv file to populate authorization info.

        :raises: HeaderError
        :return: None
        """
        # TODO: Use existing TSV files to population authz info.
        pass

    def upload(self):
        """

        :raises: IntegrityError
        :return
        """
        pass
