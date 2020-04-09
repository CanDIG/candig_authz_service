"""
Methods to handle incoming authorization service requests
"""
import datetime

import flask
import uuid

from sqlalchemy import exc, or_

from candig_authz_service.orm import get_session, ORMException
from candig_authz_service.orm.models import Authorization
from candig_authz_service import orm
from candig_authz_service.api.user_access_reader import UserAccessMap
from candig_authz_service.api.logging import apilog, logger
from candig_authz_service.api.logging import structured_log as struct_log
from candig_authz_service.api.exceptions import IdentifierFormatError

APP = flask.current_app


def _report_search_failed(typename, exception, **kwargs):
    """
    Generate standard log message + request error for error:
    Internal error performing search
    :param typename: name of type involved
    :param exception: exception thrown by ORM
    :param **kwargs: arbitrary keyword parameters
    :return: Connexion Error() type to return
    """
    report = typename + " search failed"
    message = "Internal error searching for " + typename + "s"
    logger().error(
        struct_log(action=report, exception=str(exception), **kwargs)
    )
    return dict(message=message, code=500)


def _report_object_exists(typename, **kwargs):
    """
    Generate standard log message + request error for warning:
    Trying to POST an object that already exists
    :param typename: name of type involved
    :param **kwargs: arbitrary keyword parameters
    :return: Connexion Error() type to return
    """
    report = typename + " already exists"
    logger().warning(struct_log(action=report, **kwargs))
    return dict(message=report, code=400)


def _report_foreign_key(typename, **kwargs):
    """
    Generate standard log message + request error for warning:
    Trying to POST an object that lacks a foreign key
    :param typename: name of type involved
    :param **kwargs: arbitrary keyword parameters
    :return: Connexion Error() type to return
    """
    report = typename + " requires an existing foreign key"
    logger().warning(struct_log(action=report, **kwargs))
    return dict(message=report, code=400)


def _report_update_failed(typename, exception, **kwargs):
    """
    Generate standard log message + request error for error:
    Internal error performing update (PUT)
    :param typename: name of type involved
    :param exception: exception thrown by ORM
    :param **kwargs: arbitrary keyword parameters
    :return: Connexion Error() type to return
    """
    report = typename + " updated failed"
    message = "Internal error updating " + typename + "s"
    logger().error(
        struct_log(action=report, exception=str(exception), **kwargs)
    )
    return dict(message=message, code=500)


def _report_conversion_error(typename, exception, **kwargs):
    """
    Generate standard log message + request error for warning:
    Trying to POST an object that already exists
    :param typename: name of type involved
    :param exception: exception thrown by ORM
    :param **kwargs: arbitrary keyword parameters
    :return: Connexion Error() type to return
    """
    report = "Could not convert " + typename + " to ORM model"
    message = typename + (
        ": failed validation - could not " "convert to internal representation"
    )
    logger().error(
        struct_log(action=report, exception=str(exception), **kwargs)
    )
    return dict(message=message, code=400)


def _report_write_error(typename, exception, **kwargs):
    """
    Generate standard log message + request error for error:
    Error writing to DB
    :param typename: name of type involved
    :param exception: exception thrown by ORM
    :param **kwargs: arbitrary keyword parameters
    :return: Connexion Error() type to return
    """
    report = "Internal error writing " + typename + " to DB"
    message = typename + ": internal error saving ORM object to DB"
    logger().error(
        struct_log(action=report, exception=str(exception), **kwargs)
    )
    err = dict(message=message, code=500)
    return err

access_map = UserAccessMap()
access_map.initializeUserAccess()

@apilog
def get_authz(issuer, username, project=None):
    """
    Return authorization info of a user.

    @param: issuer: The keycloak issuer of the user.
    @param: username: The username of the user.
    @param: project: Optional. Only this project's authorization info should be returned.

    @response: A JSON object with project being the key, and access_level being the value.
    """
    q = access_map.getUserAccessMap(issuer, username)

    if project:
        if project in q:
            res = {}
            res[project] = q[project]
            return res, 200
        else:
            return {}, 200

    return q, 200
    


@apilog
def get_authz_sql(issuer, username, project=None):
    """
    TODO: Implement a SQL-based data lookup.
    Return authorization info of a user.

    @param: issuer: The keycloak issuer of the user.
    @param: username: The username of the user.
    @param: project: Optional. Only this project's authorization info should be returned.

    @response: A JSON object with project being the key, and access_level being the value.
    """

    db_session = get_session()

    if not issuer:
        err = dict(message="No issuer provided", code=400)
        return err, 400

    if not username:
        err = dict(message="No username provided", code=400)
        return err, 400

    try:
        q = db_session.query(Authorization).filter_by(issuer=issuer, username=username)

        if project:
            q = q.filter(Authorization.project == project)

    except orm.ORMException as e:
        err = _report_search_failed("authorization", e, issuer=issuer, username=username, project=project)
        return err, 500

    response = {}
    dump = [orm.dump(p) for p in q]
    for d in dump:
        response_proj = d["project"]
        response_access = d["access_level"]
        response[response_proj] = response_access

    return response, 200


def validate_uuid_string(field_name, uuid_str):
    """
    Validate that the id parameter is a valid UUID string

    :param uuid_str: query parameter
    :param field_name: id field name
    """
    try:
        uuid.UUID(uuid_str)
    except ValueError:
        raise IdentifierFormatError(field_name)
