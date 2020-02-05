from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired


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
    client_phone = TelField('Ваш телефон', validators=[DataRequired()])
    submit = SubmitField('Найдите мне преподавателя')
