import phonenumbers
from flask_wtf import FlaskForm
from wtforms import HiddenField, RadioField, StringField, SubmitField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, ValidationError


def validate_phone(form, field):
    try:  # noqa:WPS229
        phone = phonenumbers.parse(field.data, 'RU')
        if not phonenumbers.is_valid_number(phone):
            raise ValueError()
    except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
        raise ValidationError('Введите ваш номер, с 8 или без.')


class RequestForm(FlaskForm):
    goals = RadioField(
        '',
        choices=[
            ('travel', 'Для путешествий'),
            ('study', 'Для школы'),
            ('work', 'Для работы'),
            ('relocate', 'Для переезда'),
        ],
        default='travel',
    )
    times = RadioField(
        '',
        choices=[
            ('1-2', '1-2 часа в неделю'),
            ('3-5', '3-5 часа в неделю'),
            ('5-7', '5-7 часа в неделю'),
            ('7-10', '7-10 часа в неделю'),
        ],
        default='1-2',
    )
    client_name = StringField('Вас зовут', validators=[DataRequired()])
    client_phone = TelField('Ваш телефон', validators=[DataRequired(), validate_phone])
    submit = SubmitField('Найдите мне преподавателя')


class BookingForm(FlaskForm):
    client_name = StringField('Вас зовут', validators=[DataRequired()])
    client_phone = TelField('Ваш телефон', validators=[DataRequired(), validate_phone])
    client_day = HiddenField('client_day')
    client_time = HiddenField('client_time')
    tutor_id = HiddenField('tutor_id')
    submit = SubmitField('Записаться на пробный урок')
