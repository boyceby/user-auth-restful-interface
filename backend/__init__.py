import os
from flask import Flask

def create_app():

    app = Flask(__name__, instance_relative_config=True)

    try:
        import production
        # Use production config (located in 'instance/') if production indication file 'production' exists
        app.config.from_pyfile('config.py')
    except Exception as e:
        # Use development config (located in root directory)
        app.config.from_object('config')

    from . import db
    db.init_app(app)

    from . import auth_BP
    app.register_blueprint(auth_BP.bp)

    return app