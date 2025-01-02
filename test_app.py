import pytest
from app import app as main_app, db  # Import the main app and db


# Define user data
user_data = {
    'fullname': 'Hamed Daneshvar',
    'username': 'hamed',
    'email': 'hamed@gmail.com',
    'password': 'password123',
    'confirm_password': 'password123',
}


@pytest.fixture
def test_client():
    # Create a new instance of the app for testing
    app = main_app  # Use the existing app instance
    app.config['TESTING'] = True  # Enable testing mode

    with app.app_context():
        db.create_all()  # Create tables in the in-memory SQLite database
        yield app.test_client()  # Provide the test client
        db.session.remove()  # Clean up the session
        db.drop_all()  # Clean up after tests


@pytest.fixture
def create_user(test_client):
    # First, get the registration page to retrieve the CSRF token
    response = test_client.get('/register')

    # Extract CSRF token from the response data
    csrf_token = None
    for line in response.data.decode().splitlines():
        if 'csrf_token' in line:
            # Find the CSRF token in the rendered HTML
            csrf_token = line.split('value="')[1].split('"')[0]  # Extract the token value
            break

    # add csrf token
    user_data['csrf_token'] = csrf_token

    # Post data to the register endpoint including the CSRF token
    response = test_client.post('/register', data=user_data)

    # remove csrf token from user_data
    del user_data['csrf_token']

    return user_data


@pytest.fixture
def logged_in_user(test_client, create_user):
    # Use the user data from the create_user fixture
    user_data = create_user  # This should contain the user data created in the signup process

    # First, get the login page to retrieve the CSRF token
    response = test_client.get('/login')
    assert response.status_code == 200  # The login page should load successfully

    # Extract CSRF token from the response data
    csrf_token = None
    for line in response.data.decode().splitlines():
        if 'csrf_token' in line:
            csrf_token = line.split('value="')[1].split('"')[0]  # Extract the token value
            break

    # Now, log in
    response = test_client.post('/login', data={
        'identifier': user_data['username'],
        'password': user_data['password'],
        'csrf_token': csrf_token
    })
    assert response.status_code == 302  # Redirect after successful login

    # Follow the redirect to the home page or dashboard
    response = test_client.get(response.headers['Location'])  # Follow the redirect
    assert b'Login successful!' in response.data

    return user_data


# Test the home endpoint
def test_home(test_client):
    response = test_client.get('/')
    print(response.data)
    assert response.status_code == 200
    assert b'Welcome' in response.data


# Test the register endpoint
def test_register(test_client):
    # First, get the registration page to retrieve the CSRF token
    response = test_client.get('/register')
    assert response.status_code == 200  # The registration page should load successfully

    # Extract CSRF token from the response data
    csrf_token = None
    for line in response.data.decode().splitlines():
        if 'csrf_token' in line:
            # Find the CSRF token in the rendered HTML
            csrf_token = line.split('value="')[1].split('"')[0]  # Extract the token value
            break

    # Post data to the register endpoint including the CSRF token
    response = test_client.post('/register', data={
        'fullname': 'Hamed',
        'username': 'hamed_username',
        'email': 'hamed_email@gmail.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'csrf_token': csrf_token  # Include the CSRF token in the POST request
    })

    # Check for redirect status code
    assert response.status_code == 302  # Expecting a redirect after successful registration

    # Follow the redirect to the home page
    response = test_client.get(response.headers['Location'])  # Follow the redirect

    # Check for success message in the response data
    assert b'Signup successful!' in response.data


# Test the login endpoint
def test_login(test_client, create_user):
    # First, get the login page to retrieve the CSRF token
    response = test_client.get('/login')
    assert response.status_code == 200  # The login page should load successfully

    # Extract CSRF token from the response data
    csrf_token = None
    for line in response.data.decode().splitlines():
        if 'csrf_token' in line:
            # Find the CSRF token in the rendered HTML
            csrf_token = line.split('value="')[1].split('"')[0]  # Extract the token value
            break

    # Now, log in
    response = test_client.post('/login', data={
        'identifier': user_data['username'],
        'password': user_data['password'],
        'csrf_token': csrf_token
    })
    assert response.status_code == 302  # Redirect after successful login
    response = test_client.get(response.headers['Location'])  # Follow the redirect
    assert b'Login successful!' in response.data


# Test the logout endpoint
def test_logout(test_client, logged_in_user):
    # Test the logout
    response = test_client.get('/logout')
    assert response.status_code == 302  # Redirect after logout

    # Follow the redirect to the home page or wherever you redirect after logout
    response = test_client.get(response.headers['Location'])  # Follow the redirect

    # Check for flash message in the redirected response
    assert b'You have been logged out' in response.data


# Test the diagnosis endpoint
def test_diagnosis(test_client, logged_in_user):
    # First, get the input page to retrieve the CSRF token
    response = test_client.get('/input')
    assert response.status_code == 200  # The input page should load successfully

    # Extract CSRF token from the response data
    csrf_token = None
    for line in response.data.decode().splitlines():
        if 'csrf_token' in line:
            # Find the CSRF token in the rendered HTML
            csrf_token = line.split('value="')[1].split('"')[0]  # Extract the token value
            break

    # Post diagnosis data
    response = test_client.post('/input', data={
        'mean_radius': 12.0,
        'mean_texture': 10.0,
        'mean_perimeter': 80.0,
        'mean_area': 500.0,
        'mean_smoothness': 0.1,
        'mean_compactness': 0.2,
        'mean_concavity': 0.3,
        'mean_concave_points': 0.4,
        'mean_symmetry': 0.5,
        'mean_fractal_dimension': 0.6,
        'radius_error': 1.0,
        'texture_error': 1.0,
        'perimeter_error': 1.0,
        'area_error': 1.0,
        'smoothness_error': 1.0,
        'compactness_error': 1.0,
        'concavity_error': 1.0,
        'concave_points_error': 1.0,
        'symmetry_error': 1.0,
        'fractal_dimension_error': 1.0,
        'worst_radius': 15.0,
        'worst_texture': 10.0,
        'worst_perimeter': 85.0,
        'worst_area': 550.0,
        'worst_smoothness': 0.2,
        'worst_compactness': 0.3,
        'worst_concavity': 0.4,
        'worst_concave_points': 0.5,
        'worst_symmetry': 0.6,
        'worst_fractal_dimension': 0.7,
        'csrf_token': csrf_token  # Include the CSRF token in the POST request
    })
    assert response.status_code == 200  # Check for successful response
    assert b'Cancerous' in response.data or b'Non-Cancerous' in response.data  # Check for results


# Test the history endpoint
def test_history(test_client, logged_in_user):
    # Access the history endpoint
    response = test_client.get('/history')
    assert response.status_code == 200  # Successful access
    assert b'Diagnosis History' in response.data


# Test error handling for 404
def test_not_found(test_client):
    response = test_client.get('/nonexistent-page')
    assert response.status_code == 404
    assert b'404 - Page Not Found' in response.data


# Test error handling for 403
def test_unauthorized_access(test_client):
    response = test_client.get('/logout')  # Attempt to log out without being logged in
    assert response.status_code == 403
    assert b'You do not have access to this page.' in response.data
