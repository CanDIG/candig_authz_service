import sys
import os
import json
import argparse
import logging
import pkg_resources


import connexion

from tornado.options import define
import candig_authz_service.orm


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser("Run CanDIG Authorization service")
    parser.add_argument("--port", default=25320)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--database", default="./data/authz_service.db")
    parser.add_argument("--logfile", default="./log/authz_service.log")
    parser.add_argument(
        "--loglevel",
        default="INFO",
        choices=["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"],
    )
    parser.add_argument("--name", default="candig_service")

    args, _ = parser.parse_known_args()
    try:
        log_handler = logging.FileHandler(args.logfile)
    except FileNotFoundError:
        os.mkdir(os.getcwd()+"/log")
        log_handler = logging.FileHandler(args.logfile)

    numeric_loglevel = getattr(logging, args.loglevel.upper())
    log_handler.setLevel(numeric_loglevel)

    app.app.logger.addHandler(log_handler)
    app.app.logger.setLevel(numeric_loglevel)

    app.app.config["name"] = args.name
    app.app.config["self"] = "http://{}/{}".format(args.host, args.port)

    app.run(host=args.host, port=args.port)
    # define("dbfile", default=args.database)
    # candig_authz_service.orm.init_db()
    # db_session = candig_authz_service.orm.get_session()

    # @app.app.teardown_appcontext
    # def shutdown_session(exception=None):
    #     db_session.remove()

    # return app, args.port


def configure_app():
    app = connexion.FlaskApp(
        __name__, server="tornado", options={"swagger_url": "/"}
    )
    api_def = pkg_resources.resource_filename('candig_authz_service',
                                              'api/api_definition.yaml')

    app.add_api(api_def, strict_validation=True, validate_responses=True)

    @app.app.after_request
    def rewrite_bad_request(response):
        if (
            response.status_code == 400
            and response.data.decode("utf-8").find('"title":') != -1
        ):
            original = json.loads(response.data.decode("utf-8"))
            response.data = json.dumps(
                {"code": 400, "message": original["detail"]}
            )
            response.headers["Content-Type"] = "application/json"

        return response

    return app


app = configure_app()

application = app.app

if __name__ == "__main__":
    main()

    # APPLICATION, PORT = main()
    # APPLICATION.app.logger.info(
    #     "{} running at {}".format(
    #         APPLICATION.app.config["name"], APPLICATION.app.config["self"]
    #     )
    # )

    # print("going to start server")
    # APPLICATION.run(port=PORT)
