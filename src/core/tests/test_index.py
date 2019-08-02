

def test_index_page_is_rendered(client):
    response = client.get('/')
    assert response.status_code == 200


def test_anonymous_user(client):
    content = client.get('/').content.decode()
    assert 'Вход' in content
    assert 'Выход' not in content


def test_logged_in_user(admin_client):
    content = admin_client.get('/').content.decode()
    assert 'Вход' not in content
    assert 'Выход' in content
