from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


def test_registration_page(client):
    registration_url = reverse('django_registration_register')
    response = client.get(registration_url)
    soup = BeautifulSoup(response.content)

    form = soup.find('form', action=registration_url, method='POST')
    assert form.find('input', {'name': 'username'}, type='text')
    assert form.find('input', {'name': 'email'}, type='email')
    assert form.find('input', {'name': 'password1'}, type='password')
    assert form.find('input', {'name': 'password2'}, type='password')
    assert form.find('button', type='submit')


def test_registration(db, client, faker):
    assert User.objects.count() == 0
    password = faker.password()

    response = client.post(
        reverse('django_registration_register'),
        data={
            'username': faker.user_name(),
            'email': faker.email(),
            'password1': password,
            'password2': password,
        },
        follow=True,
    )

    assert response.status_code == 200
    assert response.context['user'].check_password(password)
