import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        # if not testing, load the instance config
        app.config.from_pyfile('config.py', silent=True)

    else:
        # load test config if passed in
        app.config.from_mapping(test_config)

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # hello page

    @app.route('/hello')
    def hello():
        return 'Hi there. Very first flask app'

    from . import db, auth, blog
    db.init_app(app)  # register db
    app.register_blueprint(auth.bp)  # register auth blueprint
    app.register_blueprint(blog.bp)  # register blog blueprint
    app.add_url_rule('/', endpoint='index')

    return app
