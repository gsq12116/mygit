import os
import re

from flask import Blueprint, request, render_template, session, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from app.models import db, User, Area, Facility, House, HouseImage, Order
from util.functions import image_code, is_graph
from util.setting import UPLOAD_DIR
from util.status_code import OK, NO, PHONE_NOT_REGISTE, PASSWORD_ERROR, REALNAME_ERROR, IDCARD_ERROR

blue = Blueprint('user', __name__)
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@blue.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        user = User.query.filter_by(phone=mobile).first()
        if user:
            if user.check_pwd(password):
                login_user(user)
                return jsonify({"code": OK})
            else:
                return jsonify({"code": PASSWORD_ERROR})
        else:
            return jsonify({"code": PHONE_NOT_REGISTE})


@blue.route("/logout/")
@login_required
def logout():
    logout_user()
    session.clear()
    return jsonify({"code": OK})


@blue.route("/register/")
def register():
    if request.method == 'GET':
        return render_template('register.html')


@blue.route("/image_code/")
def register_image_code():
    if request.method == 'GET':
        i_code = image_code()
        session['image_code'] = i_code
        return jsonify({"code": OK, "image_code": i_code})


@blue.route("/register_info/", methods=['POST'])
def register_info():
    if request.method == 'POST':
        image_code = session.get('image_code')
        i_code = request.form.get('i_code')
        if image_code == i_code:
            mobile = request.form.get('mobile')
            password = request.form.get('password')
            user = User()
            user.phone = mobile
            user.password = password
            db.session.add(user)
            db.session.commit()
            return jsonify({"code": OK})
        else:
            return jsonify({"code": NO})


@blue.route("/my/")
@login_required
def my():
    if request.method == 'GET':
        return render_template('my.html')


@blue.route("/my_info/")
@login_required
def my_info():
    if request.method == 'GET':
        info = current_user.to_basic_dict()
        info["code"] = OK
        return jsonify(info)


@blue.route("/profile/", methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        return render_template('profile.html')
    if request.method == 'POST':
        avatar = request.files.get('avatar')
        name = request.form.get('name')
        if avatar:
            if is_graph(avatar.filename):
                file_path = os.path.join(UPLOAD_DIR, avatar.filename)
                avatar.save(file_path)
                # 保存图片路径到数据库
                user = current_user
                user.avatar = os.path.join('upload', avatar.filename)
                db.session.add(user)
                db.session.commit()
                return jsonify({"code": OK, "icon": avatar.filename})
            else:
                return jsonify({"code": NO})
        if name:
            old_name = current_user.name
            if name != old_name:
                user = current_user
                user.name = name
                user.add_update()
                return jsonify({"code": OK})
            else:
                return jsonify({"code": NO})


@blue.route("/auth/")
@login_required
def auth():
    if request.method == 'GET':
        return render_template('auth.html')


@blue.route("/id_info/", methods=['GET', 'POST'])
@login_required
def id_info():
    if request.method == 'GET':
        info = current_user.to_auth_dict()
        if info.get('id_name') and info.get('id_card'):
            info["code"] = OK
        else:
            info["code"] = NO
        return jsonify(info)
    if request.method == 'POST':
        user = current_user
        re_name = r'^[\u4E00-\u9FA5A-Za-z]+$'
        re_card = r'(^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)|(^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}[0-9Xx]$)'
        id_name = request.form.get('id_name')
        id_card = request.form.get('id_card')
        if not all([id_name, id_card]):
            return jsonify({"code": NO})
        if not re.fullmatch(re_name, id_name):
            return jsonify({"code": REALNAME_ERROR})
        if not re.fullmatch(re_card, id_card):
            return jsonify({"code": IDCARD_ERROR})
        user.id_name = id_name
        user.id_card = id_card
        user.add_update()
        return jsonify({"code": OK})


@blue.route("/myhouse/")
@login_required
def myhouse():
    if request.method == 'GET':
        return render_template('myhouse.html')


@blue.route("/check_auth/")
@login_required
def check_auth():
    if request.method == 'GET':
        if current_user.id_card:
            return jsonify({"code": OK})
        return jsonify({"code": NO})


@blue.route("/my_houses/")
@login_required
def my_houses():
    if request.method == 'GET':
        houses = House.query.filter_by(user_id=current_user.id).all()
        houses_info = [house.to_dict() for house in houses]
        return jsonify({"code": OK, "houses_info": houses_info})


@blue.route("/newhouse/", methods=['GET', 'POST', 'PATCH'])
@login_required
def newhouse():
    if request.method == 'GET':
        return render_template('newhouse.html')
    if request.method == 'POST':
        user = current_user
        user_id = user.id
        area_id = int(request.form.get('area_id'))
        title = request.form.get('title')
        price = int(request.form.get('price'))
        address = request.form.get('address')
        room_count = int(request.form.get('room_count'))
        acreage = int(request.form.get('acreage'))
        unit = request.form.get('unit')
        capacity = int(request.form.get('capacity'))
        beds = request.form.get('beds')
        deposit = int(request.form.get('deposit'))
        min_days = int(request.form.get('min_days'))
        max_days = int(request.form.get('max_days'))
        facilities = request.form.getlist('facility')
        house = House()
        house.user_id = user_id
        house.area_id = area_id
        house.title = title
        house.price = price
        house.address = address
        house.room_count = room_count
        house.acreage = acreage
        house.unit = unit
        house.capacity = capacity
        house.beds = beds
        house.deposit = deposit
        house.min_days = min_days
        house.max_days = max_days
        for facility in facilities:
            h_facility = Facility.query.filter_by(id=int(facility)).first()
            house.facilities.append(h_facility)
        house.add_update()
        house_id = house.id
        return jsonify({"code": OK, "house_id": house_id})
    if request.method == 'PATCH':
        house_image = request.files.get('house_image')
        house_id = int(request.form.get('house_id'))
        if is_graph(house_image.filename):
            file_path = os.path.join(UPLOAD_DIR, house_image.filename)
            house_image.save(file_path)
            # 保存图片路径到数据库
            house = House.query.get(house_id)
            if house.index_image_url == 'upload\haveno.jpg':
                house.index_image_url = os.path.join('upload', house_image.filename)
                house.add_update()
            else:
                houseimage = HouseImage()
                houseimage.house_id = house_id
                houseimage.url = os.path.join('upload', house_image.filename)
                houseimage.add_update()
            return jsonify({"code": OK, "house_image": os.path.join('upload', house_image.filename)})
        else:
            return jsonify({"code": NO})


@blue.route("/area_info/")
def area_info():
    if request.method == 'GET':
        area_infos = []
        facility_infos = []
        areas = Area.query.all()
        facilities = Facility.query.all()
        for area in areas:
            area_infos.append(area.to_dict())
        for facility in facilities:
            facility_infos.append(facility.to_dict())
        return jsonify(area_infos=area_infos, facility_infos=facility_infos)


@blue.route("/detail/<int:house_id>/")
@login_required
def detail(house_id):
    if request.method == 'GET':
        session['house_id'] = house_id
        return render_template('detail.html')


@blue.route("/detail_info/")
@login_required
def detail_info():
    if request.method == 'GET':
        house_id = int(session.get("house_id"))
        house = House.query.get(house_id)
        house_info = house.to_full_dict()
        if house.user_id == current_user.id:
            house_info['booking'] = 0
        else:
            house_info['booking'] = 1
        return jsonify(house_info)


@blue.route("/orders/")
@login_required
def orders():
    if request.method == 'GET':
        return render_template('orders.html')


@blue.route("/u_orders/")
@login_required
def u_orders():
    if request.method == 'GET':
        orders = Order.query.filter_by(user_id=current_user.id).all()
        orders_info = [order.to_dict() for order in orders]
        return jsonify(orders=orders_info)


@blue.route("/lorders/")
@login_required
def lorders():
    if request.method == 'GET':
        return render_template('lorders.html')


@blue.route("/u_lorders/")
@login_required
def u_lorders():
    if request.method == 'GET':
        houses = House.query.filter_by(user_id=current_user.id).all()
        house_ids = [house.id for house in houses]
        orders = Order.query.filter(Order.house_id.in_(house_ids)).all()
        orders_info = [order.to_dict() for order in orders]
        return jsonify(orders=orders_info)


@blue.route("/accept_order/", methods=['POST'])
@login_required
def accept_order():
    if request.method == 'POST':
        order_id = int(request.form.get('order_id'))
        # 状态变更，从待接单到待评价
        order = Order.query.get(order_id)
        order.status = "WAIT_COMMENT"
        order.add_update()
        return jsonify({'code': OK})


@blue.route("/reject_order/", methods=['POST'])
@login_required
def reject_order():
    if request.method == 'POST':
        order_id = int(request.form.get('order_id'))
        comment = request.form.get('reject_reason')
        # 状态变更，从待接单到已拒单
        order = Order.query.get(order_id)
        order.status = "REJECTED"
        order.comment = comment
        order.add_update()
        return jsonify({'code': OK})


@blue.route("/comment_order/", methods=['POST'])
@login_required
def comment_order():
    if request.method == 'POST':
        order_id = int(request.form.get('order_id'))
        comment = request.form.get('comment')
        # 状态变更，从待评价到已完成
        order = Order.query.get(order_id)
        order.status = "COMPLETE"
        order.comment = comment
        order.add_update()
        return jsonify({'code': OK})

# @blue.route("/createdb/")
# def create_db():
#     db.create_all()
#     return 'ok'
