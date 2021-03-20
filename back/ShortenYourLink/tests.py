import secrets
import string
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from ShortenYourLink.models import Link


class RegistrationTestCase(APITestCase):
    def test_registration_201(self):
        data = {
            'username': 'egor',
            'password': 'egor12345678',
            're_password': 'egor12345678'
        }
        response = self.client.post('/auth/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_400_1(self):
        data = {
            'username': '',
            'password': 'egor12345678',
            're_password': 'egor12345678'
        }
        response = self.client.post('/auth/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_400_2(self):
        data = {
            'username': 'egor',
            'password': '',
            're_password': ''
        }
        response = self.client.post('/auth/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_400_3(self):
        data = {
            'username': 'egor',
            'password': 'egor12345678',
            're_password': ''
        }
        response = self.client.post('/auth/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_400_4(self):
        data = {
            'username': 'egor',
            'password': 'egor',
            're_password': 'egor'
        }
        response = self.client.post('/auth/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTestCase(APITestCase):
    def test_login(self):
        data = {
            'username': 'egor',
            'password': 'egor12345678',
            're_password': 'egor12345678'
        }
        response = self.client.post('/auth/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            'username': 'egor',
            'password': 'egor12345678'
        }
        response = self.client.post('/auth/token/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            'username': 'egor',
            'password': 'egor'
        }
        response = self.client.post('/auth/token/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'username': 'ego1',
            'password': 'egor12345678'
        }
        response = self.client.post('/auth/token/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'username': '',
            'password': ''
        }
        response = self.client.post('/auth/token/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'username': 'egor',
            'password': ''
        }
        response = self.client.post('/auth/token/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'username': '',
            'password': 'egor12345678'
        }
        response = self.client.post('/auth/token/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateLinkTests(APITestCase):
    def test_case(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='egor',
            password='egor12345678'
        )
        self.token = Token.objects.create(user=self.user)
        data = {
            'orig_link':
                'https://www.youtube.com/'
                'watch?v=90DnUhSDzKY&list=PLWQhUNXl0L'
                'njBIaE72hq1RkDsbWWSgeUr&index=7',
            'life_time': 1
        }

        response = self.client.post(
            reverse('create_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertRegex(
            text=response.data,
            expected_regex="^https://shortenyourlink.herokuapp.com/"
                           "[A-Za-zА-Яа-я0-9-]+$"
        )

    def test_case_2(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='egor',
            password='egor12345678'
        )
        self.token = Token.objects.create(user=self.user)
        data = {
            'orig_link':
                '                      ',
            'life_time': 1
        }

        response = self.client.post(
            reverse('create_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'Link is empty')

    def test_case_3(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='egor',
            password='egor12345678'
        )
        self.token = Token.objects.create(user=self.user)
        data = {
            'orig_link':
                'https://www.youtube.com/watch?v='
                '90DnUhSDzKY&list=PLWQhUNXl0Ln'
                'jBIaE72hq1RkDsbWWSgeUr&index=7',
            'life_time': 0
        }

        response = self.client.post(
            reverse('create_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, 'Link life time is less than zero')


class MyLinksTest(APITestCase):
    def test_case(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='egor',
            password='egor12345678'
        )
        self.token = Token.objects.create(user=self.user)
        orig_link = 'https://www.youtube.com/' \
                    'watch?v=90DnUhSDzKY&list=PLWQhUNXl0' \
                    'LnjBIaE72hq1RkDsbWWSgeUr&index=7'
        domain_name = 'youtube.com'
        random_sequence = ''.join(secrets.choice(
            string.ascii_lowercase + string.digits)
                                  for _ in range(8))
        link_owner = self.user
        life_time_end = datetime.utcnow() + timedelta(days=int(1))
        Link.objects.create(
            orig_link=orig_link,
            domain_name=domain_name,
            random_sequence=random_sequence,
            link_owner=link_owner,
            life_time_end=life_time_end
        )
        response = self.client.get(
            reverse('my_links'),
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[0]), 8)
        self.assertEqual(response.data[0]['orig_link'], orig_link)
        self.assertEqual(response.data[0]['domain_name'], domain_name)
        self.assertEqual(response.data[0]['random_sequence'], random_sequence)
        self.assertEqual(response.data[0]['link_owner'], link_owner.id)
        self.assertEqual(datetime.fromisoformat(
            response.data[0]['life_time_end']),
            life_time_end
        )


class CheckLinkTests(APITestCase):
    def test_case_2(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='egor',
            password='egor12345678'
        )
        self.token = Token.objects.create(user=self.user)
        data = {
            'orig_link':
                'https://www.youtube.com/watch?v='
                '90DnUhSDzKY&list=PLWQhUNXl0LnjBIa'
                'E72hq1RkDsbWWSgeUr&index=7',
            'life_time': 1
        }
        response = self.client.post(
            reverse('create_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        data = {'short_link': response.data}
        response = self.client.post(
            reverse('check_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_case_3(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='egor',
            password='egor12345678'
        )
        self.token = Token.objects.create(user=self.user)
        data = {
            'orig_link':
                'https://www.youtube.com/watch?v='
                '90DnUhSDzKY&list=PLWQhUNXl0LnjBIa'
                'E72hq1RkDsbWWSgeUr&index=7',
            'life_time': 1
        }
        self.client.post(
            reverse('create_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        data = {'short_link': '         '}
        response = self.client.post(
            reverse('check_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.data,
            'Short link is empty'
        )


class ChangeLinkTests(APITestCase):
    def test_case(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='egor',
            password='egor12345678'
        )
        self.token = Token.objects.create(user=self.user)
        data = {
            'orig_link':
                'https://www.youtube.com/watch?v='
                '90DnUhSDzKY&list=PLWQhUNXl0LnjBIa'
                'E72hq1RkDsbWWSgeUr&index=7',
            'life_time': 1
        }
        response = self.client.post(
            reverse('create_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        data = {'short_link': response.data, 'new_idx': 'tutifrut'}
        response = self.client.patch(
            reverse('change_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_case_2(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='egor',
            password='egor12345678'
        )
        self.token = Token.objects.create(user=self.user)
        data = {
            'orig_link':
                'https://www.youtube.com/watch?v='
                '90DnUhSDzKY&list=PLWQhUNXl0LnjBIa'
                'E72hq1RkDsbWWSgeUr&index=7',
            'life_time': 1
        }
        self.client.post(
            reverse('create_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        data = {
            'short_link': '         ',
            'new_idx': 'tutifrut'
        }
        response = self.client.patch(
            reverse('change_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(
            response.data['message'],
            'There are no link like this'
        )

    def test_case_3(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='egor',
            password='egor12345678'
        )
        self.token = Token.objects.create(user=self.user)
        data = {
            "orig_link":
                'https://www.youtube.com/watch?v='
                '90DnUhSDzKY&list=PLWQhUNXl0LnjBIa'
                'E72hq1RkDsbWWSgeUr&index=7',
            'life_time': 1
        }
        response = self.client.post(
            reverse('create_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        data = {
            'short_link': response.data,
            'new_idx': '              '
        }
        response = self.client.patch(
            reverse('change_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'New identifier is empty')


class DeactivateLinkTests(APITestCase):
    def test_case(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='egor',
            password='egor12345678'
        )
        self.token = Token.objects.create(user=self.user)
        data = {
            'orig_link':
                'https://www.youtube.com/watch?v='
                '90DnUhSDzKY&list=PLWQhUNXl0LnjBIa'
                'E72hq1RkDsbWWSgeUr&index=7',
            'life_time': 1
        }
        response = self.client.post(reverse('create_link'),
                                    data=data,
                                    HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.delete(reverse('deactivate_link'),
                                      data={'short_link': response.data},
                                      HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_case_2(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='egor',
            password='egor12345678'
        )
        self.token = Token.objects.create(user=self.user)
        data = {
            'orig_link':
                'https://www.youtube.com/watch?v='
                '90DnUhSDzKY&list=PLWQhUNXl0LnjBIa'
                'E72hq1RkDsbWWSgeUr&index=7',
            'life_time': 1
        }
        self.client.post(
            reverse('create_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        response = self.client.delete(
            reverse('deactivate_link'),
            data={'short_link': '      '},
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            response.data['message'],
            'There are no link like this'
        )


class AddHashtagTests(APITestCase):
    def test_case(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='egor',
            password='egor12345678'
        )
        self.token = Token.objects.create(user=self.user)
        data = {
            'orig_link':
                'https://www.youtube.com/watch?v='
                '90DnUhSDzKY&list=PLWQhUNXl0LnjBIa'
                'E72hq1RkDsbWWSgeUr&index=7',
            'life_time': 1
        }
        response = self.client.post(
            reverse('create_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        data = {
            'short_link': response.data,
            'link_tag': 'tag'
        }
        response = self.client.patch(
            reverse('add_hashtag'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_case_2(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='egor',
            password='egor12345678'
        )
        self.token = Token.objects.create(user=self.user)
        data = {
            'orig_link':
                'https://www.youtube.com/watch?v='
                '90DnUhSDzKY&list=PLWQhUNXl0LnjBIa'
                'E72hq1RkDsbWWSgeUr&index=7',
            'life_time': 1
        }
        self.client.post(
            reverse('create_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        data = {'short_link': '     ', 'link_tag': 'tag'}
        response = self.client.patch(
            reverse('add_hashtag'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            response.data['message'],
            'There are no link like this'
        )

    def test_case_3(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='egor',
            password='egor12345678'
        )
        self.token = Token.objects.create(user=self.user)
        data = {
            'orig_link':
                'https://www.youtube.com/watch?v='
                '90DnUhSDzKY&list=PLWQhUNXl0LnjBIa'
                'E72hq1RkDsbWWSgeUr&index=7',
            'life_time': 1
        }
        response = self.client.post(
            reverse('create_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        data = {'short_link': response.data, 'link_tag': '            '}
        response = self.client.patch(
            reverse('add_hashtag'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Link tag is empty")


class MyAccountInfoTests(APITestCase):
    def test_case(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='egor',
            password='egor12345678'
        )
        self.token = Token.objects.create(user=self.user)
        response = self.client.get(
            reverse('my_account'),
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 11)


class LinkInfoTests(APITestCase):
    def test_case(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='egor',
            password='egor12345678'
        )
        self.token = Token.objects.create(user=self.user)
        data = {
            'orig_link':
                'https://www.youtube.com/watch?v='
                '90DnUhSDzKY&list=PLWQhUNXl0LnjBIa'
                'E72hq1RkDsbWWSgeUr&index=7',
            'life_time': 1
        }
        self.client.post(
            reverse('create_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        data = {
            'orig_link':
                'https://www.youtube.com/watch?v='
                '90DnUhSDzKY&list=PLWQhUNXl0LnjBIa'
                'E72hq1RkDsbWWSgeUr&index=8',
            'life_time': 1
        }
        response = self.client.post(
            reverse('create_link'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        data = {
            'short_link': response.data
        }
        response = self.client.post(
            reverse('link_info'),
            data=data,
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(len(response.data), 7)
