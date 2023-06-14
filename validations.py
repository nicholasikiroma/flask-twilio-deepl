from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, equal_to


class SignupForm(FlaskForm):
    """ Validations for signup form """

    username = StringField(
        label="Username", validators=[InputRequired(message="Username cannot be left blank")]
    )

    password = PasswordField(
        label="Password",
        validators=[InputRequired(message="Password cannot be left blank")],
    )

    language = SelectField(
        "Language",
        choices=[
            "BG", "CS", "DA", "DE", "EL", "EN-US", "EN-GB", "ES", "ET", "FI", "FR", "HU",
            "ID", "IT", "JA", "KO", "LT", "LV", "NB", "NL", "PL", "PT", "RO",
            "RU", "SK", "SL", "SV", "TR", "UK", "ZH",
        ],
    )

    confirm_password = PasswordField(
        label="Confirm Password",
        validators=[
            InputRequired(message="Password cannot be left blank"),
            equal_to("password", message="passwords do not match"),
        ],
    )


class LoginForm(FlaskForm):
    """ Validation for login form """

    username = StringField(
        label="Username", validators=[InputRequired(message="Provide a username")]
    )
    password = PasswordField(
        label="Password",
        validators=[InputRequired(message="Password cannot be left blank")],
    )
