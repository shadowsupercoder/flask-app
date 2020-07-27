from flask import (
    Blueprint, render_template, request, flash, redirect, url_for,
    current_app
)
from sqlalchemy.exc import SQLAlchemyError

from .models import Log, db
from .forms import PaymentCreateForm


module = Blueprint('log', __name__)


def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


@module.route('/', methods=['GET', 'POST'])
def pay():
    form = PaymentCreateForm(request.form)
    try:
        if request.method == 'POST' and form.validate():
            log = Log(**form.data)
            db.session.add(log)
            db.session.flush()
            _id = log.id
            db.session.commit()
            flash('The Log object was added successfully.', 'success')
            return redirect(url_for('log.view', id=_id))
    except SQLAlchemyError as e:
        log_error('There was error while querying database.', exc_info=e)
        db.session.rollback()
        flash('', 'danger')
    return render_template('payment/create.html', form=form)
