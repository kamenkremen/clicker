from flask import Flask
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_restful import Api


database = dec.declarative_base()
__factory = None
# путь относительно main.py
DB_PATH = 'website/db/clicker.sqlite'


def db_init(db_file=DB_PATH):
    global __factory

    if __factory:
        return

    db_file = db_file.strip()
    if not db_file:
        raise Exception('Необходимо указать файл базы данных.')

    conn_str = f'sqlite:///{db_file}?check_same_thread=False'
    print(f'Подключение к базе данных по адресу {conn_str}')

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from .models import __all_models

    database.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'kamen_secret_key'
    api = Api(app)

    db_init()

    login_manager = LoginManager()
    login_manager.init_app(app)
    from .clicker_blueprint import clicker_blueprint
    app.register_blueprint(clicker_blueprint)


    @login_manager.user_loader
    def load_user(user_id):
        db_sess = create_session()
        return db_sess.query(users.User).get(user_id)

    from .resources.users import UserResource, UserListResource
    from .resources.upgrades import UpgradeResource, UpgradeListResource
    api.add_resource(UserListResource, '/api/v1/users')
    api.add_resource(UserResource, '/api/v1/users/<int:user_id>')
    api.add_resource(UpgradeListResource, '/api/v1/upgrades')
    api.add_resource(UpgradeResource, '/api/v1/upgrades/<int:upgrade_id>')

    return app
