from datetime import datetime, date

from flask import Blueprint, render_template, jsonify, session, request
from flask_login import current_user, login_required
from sqlalchemy import and_, or_, desc

from app.models import Area, House, Order
from util.status_code import NO, OK

index = Blueprint('index', __name__)


@index.route("/")
def my_index():
    return render_template('index.html')


@index.route("/check_user/")
def check_user():
    user = current_user
    if user.is_authenticated:
        return jsonify(code=OK, user=user.to_basic_dict())
    else:
        return jsonify({"code": NO})


@index.route("/search/")
def search():
    return render_template('search.html')


@index.route("/search_info/", methods=['POST'])
def search_info():
    aid = request.form.get('aid')
    sd = request.form.get('sd')
    ed = request.form.get('ed')
    if not sd:
        sd = date.today().strftime('%Y-%m-%d')
    sk = request.form.get('sk')
    # p = request.form.get('p')
    if ed:
        start_date = datetime.strptime(sd, '%Y-%m-%d')
        end_date = datetime.strptime(ed, '%Y-%m-%d')
        differ_days = int((end_date-start_date).days)
        houses_first = House.query.filter(or_(and_(House.min_days <= differ_days, House.max_days >= differ_days),
                                              and_(House.min_days <= differ_days, House.max_days == 0)))
    else:
        houses_first = House.query.filter()
    if aid:
        houses_seconed = houses_first.filter(House.area_id == int(aid))
    else:
        houses_seconed = houses_first
    # 订单房源信息，过滤待接单，待支付，已支付
    orders_filter = Order.query.filter(Order.status.in_(["WAIT_ACCEPT", "WAIT_PAYMENT", "PAID"])).all()
    orders_filter_ids = set([order_filter.house_id for order_filter in orders_filter])
    houses_third = houses_seconed.filter(~House.id.in_(orders_filter_ids))
    # 排序
    if sk == 'new':
        houses_final = houses_third.order_by(desc('update_time'))
    elif sk == 'booking':
        houses_final = houses_third.order_by(desc('order_count'))
    elif sk == 'price-inc':
        houses_final = houses_third.order_by('price')
    else:
        houses_final = houses_third.order_by(desc('price'))
    houses = houses_final.all()
    houses_info = [house.to_full_dict() for house in houses]
    return jsonify(houses_info)


@index.route("/booking/")
@login_required
def booking():
    return render_template('booking.html')


@index.route("/booking_info/")
@login_required
def booking_info():
    house_id = int(request.args.get("h_info_id"))
    house = House.query.get(int(house_id)).to_dict()
    return jsonify(house)


@index.route("/order_add/", methods=['POST'])
@login_required
def order_add():
    data = request.form
    order = Order(**data)
    order.user_id = current_user.id
    order.add_update()
    return jsonify({"code": OK})

