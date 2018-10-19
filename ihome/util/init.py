from flask_session import Session

from app.models import db
from app.views import login_manager


def init_ext(app):
    # 获取Session对象,并初始化app
    se = Session()
    se.init_app(app)

    # 绑定db和app
    db.init_app(app)

    # 绑定login_manager和app
    login_manager.login_view = 'user.login'
    login_manager.init_app(app)