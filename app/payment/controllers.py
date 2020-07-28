import json

import requests
import hashlib

from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, current_app,
    Response
)
from sqlalchemy.exc import SQLAlchemyError


from .models import Log, db, EUR_CODE, USD_CODE, RUB_CODE
from .forms import PaymentCreateForm


module = Blueprint('log', __name__)
SHOP_ID = current_app.config.get('SHOP_ID')
SECRET_KEY = current_app.config.get('SECRET_KEY_PTX')


def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


@module.route("/ptx_4415.txt")
def ptx():
    # TODO - it should be more flexible
    with open("app/static/data/ptx_4415.txt", "r") as f:
        return Response(f.read(), mimetype='text/plain')


@module.route('/logs', methods=['GET'])
def get_logs():
    '''
    Get Log list.
    '''
    return render_template('payment/list.html', logs=Log.query.all())


@module.route('/', methods=['GET', 'POST'])
def pay():
    '''
    Get form for the payment and recieve a POST request to create a Log object.
    '''
    form = PaymentCreateForm(request.form)
    try:
        if request.method == 'POST' and form.validate():
            log = Log(**form.data)
            db.session.add(log)
            db.session.flush()
            db.session.commit()

            payment_data, url = get_payment_data(
                str(log.amount),
                log.currency.code,
                str(log.id))

            if log.currency.code == EUR_CODE:
                return render_template(
                    'payment/pay_bill_form.html',
                    payment_data=payment_data,
                    payment_url=url)
            else:
                # TODO - simplify levels
                response = make_request(payment_data, url)
                if response.status_code == 200:
                    content = json.loads(response.content)
                    data = content.get('data')
                    if data and 'url' in data:
                        if log.currency.code == RUB_CODE:
                            data_source = data.get('data')
                            return render_template(
                                'payment/pay_invoice_form.html',
                                payment_data={
                                    'data_source': data_source,
                                    'method_source': data.get('method'),
                                    'url_source': data.get('url'),
                                    'id_source': data.get('id')
                                })
                        else:
                            # TODO - check that it is a USD currency
                            return redirect(data['url'])
                    else:
                        flash(content.get('message'), 'fail')
                        return redirect(url_for('log.pay'))
                else:
                    flash(response.status_code, 'fail')
                    return redirect(url_for('log.pay'))

            flash('The Log object was added successfully.', 'success')
            return redirect(url_for('log.pay'))
    except SQLAlchemyError as e:
        log_error('There was error while querying database.', exc_info=e)
        db.session.rollback()
        flash('Something went wrong', 'error')
    return render_template('payment/create.html', form=form)


def get_payment_data(amount, currency, shop_order_id):
    data = {
        'currency': currency,
        'amount': amount,
    }
    keys = None

    if currency == EUR_CODE:
        keys = [amount, currency, SHOP_ID, shop_order_id]
        # create a contect for the autosubmit form
        url = 'https://pay.piastrix.com/ru/pay'

    elif currency == USD_CODE:
        # bill
        # the second currency in the keys list is a payer_currency
        keys = [currency, amount, currency, SHOP_ID, shop_order_id]
        url = 'https://core.piastrix.com/bill/create'
        data = {
            'payer_currency': currency,
            'shop_amount': amount,
            'shop_currency': currency
        }
    elif currency == RUB_CODE:
        # incoice
        payway = "card_rub"
        url = 'https://core.piastrix.com/invoice/create'
        keys = [amount, currency, payway, SHOP_ID, shop_order_id]
        data.update({"payway": payway})

    # TODO
    # else:
    #     # raise an error message

    prepared_string = ':'.join(keys) + SECRET_KEY
    sign = sign_generate(prepared_string)
    data.update({
        'shop_id': SHOP_ID,
        'shop_order_id': shop_order_id,
        'sign': sign
    })
    return data, url


def sign_generate(prepared_string):
    return hashlib.sha256(prepared_string.encode('utf-8')).hexdigest()


def make_request(data, url):
    headers = {'Content-Type': 'application/json'}
    return requests.post(url, data=json.dumps(data), headers=headers)
