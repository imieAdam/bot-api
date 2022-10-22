import os

from flask import Flask, jsonify

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'test_db_1.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY='change_this_in_prod!'
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello world
    @app.route('/')
    def hello():
        return 'These Are Not the Droids You Are Looking For' 

    with app.app_context():
        from api_app.database.database import db_session, init_db, init_ma
        init_db()
        init_ma()
        from api_app.controllers.jwt import init_jwt
        init_jwt()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    #from api_app.database.database import init_db
    #init_db()

    #from api_app.models.models import ma
    #ma.init_app(app)


    from api_app.controllers import locations, auth_jwt, visits
    app.register_blueprint(locations.bp)
    app.register_blueprint(auth_jwt.bp)
    app.register_blueprint(visits.bp)


    return app

if __name__ == "__main__":
    create_app()