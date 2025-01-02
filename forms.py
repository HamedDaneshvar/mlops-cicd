from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired


class RegisterForm(FlaskForm):
    fullname = StringField('Full Name', validators=[
        DataRequired(message="Full name is required."),
        Length(min=3, message="Full name must be at least 3 characters long.")
    ])

    username = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(min=3, message="Username must be at least 3 characters long.")
    ])

    email = StringField('Email', validators=[
        DataRequired(message="Email is required."),
        Email(message="Enter a valid email address.")
    ])

    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        Length(min=8, message="Password must be at least 8 characters long.")
    ])

    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo('password', message="Passwords must match.")
    ])

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    identifier = StringField('Username or Email', validators=[
        DataRequired(message="Username or Email is required."),
        Length(min=3, message="Username or Email must be at"
               " least 3 characters long.")
    ])

    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        Length(min=8, message="Password must be at least 8 characters long.")
    ])

    submit = SubmitField('Login')


class CancerDiagnosisForm(FlaskForm):
    mean_radius = FloatField('Mean Radius',
                             validators=[InputRequired(
                                 message="Mean Radius is required.")])
    mean_texture = FloatField('Mean Texture',
                              validators=[InputRequired(
                                  message="Mean Texture is required.")])
    mean_perimeter = FloatField('Mean Perimeter',
                                validators=[InputRequired(
                                    message="Mean Perimeter is required.")])
    mean_area = FloatField('Mean Area',
                           validators=[InputRequired(
                               message="Mean Area is required.")])
    mean_smoothness = FloatField('Mean Smoothness',
                                 validators=[InputRequired(
                                     message="Mean Smoothness is required.")])
    mean_compactness = FloatField('Mean Compactness',
                                  validators=[InputRequired(
                                      message="Mean Compactness is required."
                                      )])
    mean_concavity = FloatField('Mean Concavity',
                                validators=[InputRequired(
                                    message="Mean Concavity is required.")])
    mean_concave_points = FloatField('Mean Concave Points',
                                     validators=[InputRequired(
                                         message="Mean Concave Points is"
                                         "required.")])
    mean_symmetry = FloatField('Mean Symmetry',
                               validators=[InputRequired(
                                   message="Mean Symmetry is required.")])
    mean_fractal_dimension = FloatField('Mean Fractal Dimension',
                                        validators=[InputRequired(
                                            message="Mean Fractal Dimension is"
                                            "required.")])
    radius_error = FloatField('Radius Error',
                              validators=[InputRequired(
                                  message="Radius Error is required.")])
    texture_error = FloatField('Texture Error',
                               validators=[InputRequired(
                                   message="Texture Error is required.")])
    perimeter_error = FloatField('Perimeter Error',
                                 validators=[InputRequired(
                                     message="Perimeter Error is required.")])
    area_error = FloatField('Area Error',
                            validators=[InputRequired(
                                message="Area Error is required.")])
    smoothness_error = FloatField('Smoothness Error',
                                  validators=[InputRequired(
                                      message="Smoothness Error is required."
                                      )])
    compactness_error = FloatField('Compactness Error',
                                   validators=[InputRequired(
                                       message="Compactness Error is required."
                                       )])
    concavity_error = FloatField('Concavity Error',
                                 validators=[InputRequired(
                                     message="Concavity Error is required.")])
    concave_points_error = FloatField('Concave Points Error',
                                      validators=[InputRequired(
                                          message="Concave Points Error is"
                                          "required.")])
    symmetry_error = FloatField('Symmetry Error',
                                validators=[InputRequired(
                                    message="Symmetry Error is required.")])
    fractal_dimension_error = FloatField('Fractal Dimension Error',
                                         validators=[InputRequired(
                                             message="Fractal Dimension Error"
                                             "is required.")])
    worst_radius = FloatField('Worst Radius',
                              validators=[InputRequired(
                                  message="Worst Radius is required.")])
    worst_texture = FloatField('Worst Texture',
                               validators=[InputRequired(
                                   message="Worst Texture is required.")])
    worst_perimeter = FloatField('Worst Perimeter',
                                 validators=[InputRequired(
                                     message="Worst Perimeter is required.")])
    worst_area = FloatField('Worst Area',
                            validators=[InputRequired(
                                message="Worst Area is required.")])
    worst_smoothness = FloatField('Worst Smoothness',
                                  validators=[InputRequired(
                                      message="Worst Smoothness is required."
                                      )])
    worst_compactness = FloatField('Worst Compactness',
                                   validators=[InputRequired(
                                       message="Worst Compactness is required."
                                        )])
    worst_concavity = FloatField('Worst Concavity',
                                 validators=[InputRequired(
                                     message="Worst Concavity is required.")])
    worst_concave_points = FloatField('Worst Concave Points',
                                      validators=[InputRequired(
                                          message="Worst Concave Points is"
                                          "required.")])
    worst_symmetry = FloatField('Worst Symmetry',
                                validators=[InputRequired(
                                    message="Worst Symmetry is required.")])
    worst_fractal_dimension = FloatField('Worst Fractal Dimension',
                                         validators=[InputRequired(
                                             message="Worst Fractal Dimension"
                                             "is required.")])

    submit = SubmitField('Submit')
