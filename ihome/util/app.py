from flask import Flask

from app.views import blue
from app.views_index import index
from util.config import Config
from util.init import init_ext
from util.setting import STATIC_DIR, TEMPLATES_DIR


def create_app():
    app = Flask(__name__,
                static_folder=STATIC_DIR,
                template_folder=TEMPLATES_DIR)

    app.config.from_object(Config)

    # 加载注册蓝图
    app.register_blueprint(blueprint=blue, url_prefix='/user')
    app.register_blueprint(blueprint=index, url_prefix='/index')

    init_ext(app)
    return app