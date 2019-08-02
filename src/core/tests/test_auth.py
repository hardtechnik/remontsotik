from django.urls import reverse
from bs4 import BeautifulSoup


def test_login_page(client):
    auth_url = reverse('login')
    soup = BeautifulSoup(client.get(auth_url).content)
    form = soup.find('form', action=auth_url, method='POST')
    assert form.find('input', {'name': 'username'})
    assert form.find('input', {'name': 'password'})
    assert form.find('button', type='submit')


def test_login(db, client, faker, user_factory):
    user = user_factory()
    password = faker.password()
    user.set_password(password)
    user.save()
    response = client.post(
        reverse('login'),
        {'username': user.username, 'password': password},
        follow=True,
    )
    assert response.status_code == 200
    assert response.context['user'] == user
