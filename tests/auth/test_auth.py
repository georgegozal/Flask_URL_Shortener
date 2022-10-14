from flask_login import current_user


APP_URLS = [
    '/',
    '/urls',
    '/sign-up',
    '/login',
    '/api/urls',
]


def test_urls(client):
    for url in APP_URLS:
        response = client.get(url)
        assert response.status_code == 200


def test_login(client):
    assert client.get('/login').status_code == 200

    with client:
        client.post('/login',data={'email': 'test@gmail.com', 'password': 'password123'})
        assert current_user.is_authenticated


def test_failed_register(client):
    assert client.get('/sign-up').status_code == 200
    response = client.post('/sign-up', 
        data={'email': "pytest@gmail.com", 'first_name': 'test',
                "password1": "password5", "password2": "password7"}, 
                    follow_redirects=True)
    assert b'Passwords don`t match.' in response.data


def test_successful_register(client):
    assert client.get('/sign-up').status_code == 200
    response = client.post('/sign-up', 
        data={'email': "pytest@gmail.com", 'first_name': 'test',
                "password1": "password5", "password2": "password5"}, 
                    follow_redirects=True)
    assert response.request.path == '/'
