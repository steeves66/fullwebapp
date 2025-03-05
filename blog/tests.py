from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase

# Create your tests here.

class BasicTests(APITestCase):
    def test_basic_req(self):
        """
        Test the basic url path response
        """
        
        # ARRANGE-Create a url and expected response
        url = 'blog/hello-world/'
        expected_data = {'msg': "hello world!"}

        # ACT - Perform API call by DRF's test APIClient.
        response = self.client.get(url, format='json')

        # ASSERT - Verify the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


class BasicTests2(APITestCase):
    def test_unauthenticated_req(self):
        url = 'blog/hello-world-2/'
        response = self.client.get(url, format='json')

        # since user is not logged in it would get 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_authenticated_req(self):
        url = 'blog/hello-world-2/'
        expected_data = {
            'msg': "hello world!"
        }
        user = User.objects.create_user(username='demouser', password="demopass")
        token, created = Token.objects.get_or_create(user="demouser")

        # Login the request using the HTTP header token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = self.client.get(url, format='json')

        # User is logged in we would get the expected 200 response code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


    def test_wrong_authenticated_req(self):
        url = 'blog/hello-world-2/'
        # Login to the request using a random wrong token
        self.client.credentials(HTTP_AUTHORIZATION= f'Token random')
        response = self.client.get(url, format='json')

        # Request has wrong token so it would get 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_force_authenticate_with_user(self):
        """
        Setting `.force_authenticate()` with a user forcibly authenticates.
        """
        u1 = User.objects.create_user('a1', 'a1@abc.co')
        url = '/blog/hello-world-2/'
        # Forcefully login and update request.user
        self.client.force_authenticated(user=u1)
        response = self.client.get(url)
        expected_data = {"msg": "hello world!"}

        # Tests work with the login user
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    
class BasicTests3(APITestCase):
    def setUp(self):
        self.url = '/blog/hello-world/'
        user =  User.objects.create_user('a1', 'a1@abc.co')
        self.client.force_authenticate(user=user)
        print('Running Setup')

    def test_with_setup_authenticated_req(self):
        print('test 1 running')
        expected_data = {
            'msg': "hello world!"
        }
        response = self.client.get(self.url, format='json')

        # User is logged in, expected 200 response code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    # demo_test
    def test_demo(self):
        print('test 2 running')
        self.assertEqual(1, 1)
    
    def tearDown(self):
        self.client.logout()
        print('Running teardown')


from django.test import tag
from rest_framework.test import APITestCase
class BlogTests8(APITestCase):
    @tag("fast")
    def test_fast(self):
        print("fast test running")
    @tag("slow")
    def test_slow(self):
        print("slow test running")
    @tag("slow", "core")
    def test_slow_but_core(self):
        print("slow but core test running")

# python manage.py test --tag=core