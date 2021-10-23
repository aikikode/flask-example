__version__ = '0.1.0'

from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY="dev",
    SQLALCHEMY_DATABASE_URI="mysql://myusername:secure_password@127.0.0.1:3306/flaskr_db",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Late import so modules can load app and db
from . import views, models, auth, blog

migrate.init_app(app, db)

app.register_blueprint(auth.views.blueprint)
app.register_blueprint(blog.views.blueprint)
app.add_url_rule('/', endpoint='index')
