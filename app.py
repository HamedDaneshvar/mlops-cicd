import os
from functools import wraps
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    session,
    abort,
)
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm, CancerDiagnosisForm
from database import db, User, CancerDiagnosis
from models.model import predict_cancerous


# Load environment variables from .env file
load_dotenv()

# Get the secret key from the environment
SECRET_KEY = os.getenv('SECRET_KEY')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_DB = os.getenv('POSTGRES_DB')


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
# Check if we are in testing mode
if os.getenv('FLASK_ENV') == 'testing':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory SQLite for testing
else:
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    # PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
db.init_app(app)


def get_current_user():
    """
    Get User information
    """
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        return user
    return None


@app.context_processor
def inject_user_data():
    """
    Make user information available in templates
    """
    user = get_current_user()
    return dict(user=user)


def login_required(f):
    """
    Restrict access to logged-in users only
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You do not have access to this page. Please log in!',
                  'danger')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                # Hash the password
                hashed_password = generate_password_hash(form.password.data)
                # Create instance of user
                new_user = User(fullname=form.fullname.data,
                                username=form.username.data,
                                email=form.email.data,
                                password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                # Save user credentials and the logged-in user to their account
                session['username'] = new_user.username
                flash('Signup successful!', 'success')
                return redirect(url_for('home'))
            except IntegrityError:
                db.session.rollback()
                flash('Username or email already exists. Please choose a '
                      'different one.', 'danger')
                return render_template('register.html', form=form)
        else:
            # Form is invalid, flash errors and
            # redirect back to the register page
            flash('There were errors in the form. \
                  Please fix them and try again.', 'danger')
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Check identifier and password for authentication
            identifier = form.identifier.data
            password = form.password.data
            # Query the User model for the provided username or email
            user = User.query.filter((User.username == identifier) |
                                     (User.email == identifier)).first()

            if user and check_password_hash(user.password, password):
                # Password matches, user authenticated
                # Save user credentials
                session['username'] = user.username

                flash('Login successful!', 'success')
                return redirect(url_for('home'))

            flash('Invalid username or password', 'danger')
            return render_template('login.html', form=form)
        else:
            # Form is invalid, flash errors and
            # redirect back to the login page
            flash('There were errors in the form. \
                  Please fix them and try again.', 'danger')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    # Remove user credentials
    session.pop('username')
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))


@app.route('/input', methods=['GET', 'POST'])
@login_required
def diagnosis():
    form = CancerDiagnosisForm()
    if form.validate_on_submit():
        input_data = [
            form.mean_radius.data,
            form.mean_texture.data,
            form.mean_perimeter.data,
            form.mean_area.data,
            form.mean_smoothness.data,
            form.mean_compactness.data,
            form.mean_concavity.data,
            form.mean_concave_points.data,
            form.mean_symmetry.data,
            form.mean_fractal_dimension.data,
            form.radius_error.data,
            form.texture_error.data,
            form.perimeter_error.data,
            form.area_error.data,
            form.smoothness_error.data,
            form.compactness_error.data,
            form.concavity_error.data,
            form.concave_points_error.data,
            form.symmetry_error.data,
            form.fractal_dimension_error.data,
            form.worst_radius.data,
            form.worst_texture.data,
            form.worst_perimeter.data,
            form.worst_area.data,
            form.worst_smoothness.data,
            form.worst_compactness.data,
            form.worst_concavity.data,
            form.worst_concave_points.data,
            form.worst_symmetry.data,
            form.worst_fractal_dimension.data
        ]

        # make the prediction
        prediction = predict_cancerous(input_data)

        # Based on the prediction, determine the result
        if prediction[0] == 1:
            diagnosis_result = "Cancerous"
            bg_color = "danger"
        else:
            diagnosis_result = "Non-Cancerous"
            bg_color = "success"

        current_user = get_current_user()

        new_diagnosis = CancerDiagnosis(
            user_id=current_user.id,
            mean_radius=form.mean_radius.data,
            mean_texture=form.mean_texture.data,
            mean_perimeter=form.mean_perimeter.data,
            mean_area=form.mean_area.data,
            mean_smoothness=form.mean_smoothness.data,
            mean_compactness=form.mean_compactness.data,
            mean_concavity=form.mean_concavity.data,
            mean_concave_points=form.mean_concave_points.data,
            mean_symmetry=form.mean_symmetry.data,
            mean_fractal_dimension=form.mean_fractal_dimension.data,
            radius_error=form.radius_error.data,
            texture_error=form.texture_error.data,
            perimeter_error=form.perimeter_error.data,
            area_error=form.area_error.data,
            smoothness_error=form.smoothness_error.data,
            compactness_error=form.compactness_error.data,
            concavity_error=form.concavity_error.data,
            concave_points_error=form.concave_points_error.data,
            symmetry_error=form.symmetry_error.data,
            fractal_dimension_error=form.fractal_dimension_error.data,
            worst_radius=form.worst_radius.data,
            worst_texture=form.worst_texture.data,
            worst_perimeter=form.worst_perimeter.data,
            worst_area=form.worst_area.data,
            worst_smoothness=form.worst_smoothness.data,
            worst_compactness=form.worst_compactness.data,
            worst_concavity=form.worst_concavity.data,
            worst_concave_points=form.worst_concave_points.data,
            worst_symmetry=form.worst_symmetry.data,
            worst_fractal_dimension=form.worst_fractal_dimension.data,
            diagnosis_result=diagnosis_result  # Cancerous or Non-Cancerous
        )

        # Save to database
        db.session.add(new_diagnosis)
        db.session.commit()

        # Render a template to show the result
        return render_template('result.html', result=diagnosis_result,
                               bg_color=bg_color)

    # Render the form template
    return render_template('diagnosis.html', form=form)


@app.route('/history')
@login_required
def history():
    user = get_current_user()
    user_diagnoses = CancerDiagnosis.query.filter_by(user_id=user.id)\
        .order_by(desc(CancerDiagnosis.created_at)).all()
    return render_template('history.html', user_diagnoses=user_diagnoses)


@app.errorhandler(404)
def not_found(error):
    context = {'title': 'Page Not Found',
               'heading': '404 - Page Not Found',
               'description': 'Sorry, the page you'
               ' are looking for does not exist.'}

    return render_template('errors.html', **context), 404


@app.errorhandler(403)
def unauthorized(error):
    context = {'title': 'Unauthorized Access',
               'heading': '403 - Unauthorized Access',
               'description': 'You do not have permission'
               ' to access this page.'}

    return render_template('errors.html', **context), 403


@app.errorhandler(500)
def internal_server_error(error):
    context = {'title': 'Internal Server Error',
               'heading': '500 - Internal Server Error',
               'description': 'Oops! Something went wrong on our'
               ' end. Please try again later.'}

    return render_template('errors.html', **context), 500


if __name__ == '__main__':
    # Create tables if it does not exist
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8000)
