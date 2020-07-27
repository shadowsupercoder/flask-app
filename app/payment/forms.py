from wtforms import Form, TextAreaField, SelectField, DecimalField
from wtforms.validators import DataRequired

from .models import CURRENCY_CHOICE


class PaymentCreateForm(Form):
    '''
    A form creation for the Log model.
    '''
    description = TextAreaField('Description', [DataRequired()])
    amount = DecimalField('Payment amount', [DataRequired()])
    currency = SelectField(
        'Currency',
        [DataRequired()],
        choices=CURRENCY_CHOICE)
