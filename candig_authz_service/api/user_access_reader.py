import os
import math

import pandas as pd
import candig_authz_service.api.exceptions as exceptions


class UserAccessMap(object):
    """
    Loads local authorization info from an access list file to the backend
    ACL tsv file header row contains list of project names(ID)
    """
    def __init__(self, logger=None):
        self.user_access_map = {}
        self.file_path = "access_list.tsv"

        if not os.path.isfile(self.file_path):
            raise exceptions.ConfigurationException("No user access list defined.")

        try:
            self.access_list = pd.read_csv(self.file_path, sep='\t', index_col=['issuer', 'username'])
            # Detect duplicated (issuer, username) tuples
            for issuer_user in self.access_list.index[self.access_list.index.duplicated()]:
                raise ValueError(
                    "Duplicate entries detected for {}. "
                    "User access disabled until ACL resolved.".format(issuer_user))
        except (IOError, ValueError) as err:
            self.access_list = None
            if logger:
                logger.error(err)

        self.list_updated = os.path.getmtime(self.file_path)

    def initializeUserAccess(self):
        # Convert user access table into a dictionary
        if self.access_list is not None:
            self.user_access_map = self.access_list.to_dict(orient='index')

        # Remove non set values
        self.user_access_map = {
            user: {project: level
                   for project, level in value.items() if self.validateAccessLevel(level)
                   }
            for user, value in self.user_access_map.items()
        }

    def validateAccessLevel(self, level):
        """
        Returns True if the level is one of 0, 1, 2, 3, 4, this indicates the user has some access to the dataset.
        Returns False if the level is one of empty string or X, this indicates the user has no access to the dataset.
        Raise an exception otherwise, this indicates that there's illegal characters specified as 'level'.
        The support for empty string will be deprecated and removed in future releases.
        """
        try:
            if 0 <= int(level) <= 4:
                return True
        except (ValueError, TypeError):
            if level == "X" or level == " ":
                return False
            elif math.isnan(level):
                return False

        raise exceptions.InvalidAccessListException(level)

    def getUserAccessMap(self, issuer, username):
        try:
            print("get request")
            print(self.user_access_map)
            access_map = self.user_access_map[(issuer, username)]
        except KeyError:
            access_map = {}
        return access_map

    def getFilePath(self):
        return self.file_path

    def getListUpdated(self):
        return self.list_updated
