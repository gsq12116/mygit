"""new python"""
import os

from flask import render_template
from flask_script import Manager

from util.app import create_app

app = create_app()


# 主页
@app.route('/')
def index():
    return render_template('index.html')


# 使用manager管理app
manager = Manager(app=app)

if __name__ == '__main__':
    # 运行
    manager.run()