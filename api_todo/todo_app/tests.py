
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from todo_app.models import Todo


class PublicToDoApiTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        test_user = User.objects.create(
            username='testuser',
            password='abc123'
        )
        Todo.objects.create(
            user=test_user,
            description='Doing something cool',
            complete=True
        )

    def test_get_todo_unauthorized(self):
        self.url = reverse('todo_app:list_create_todo')
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateToDoApiTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.test_user = User.objects.create_user(
            username='my_user',
            email='my_user@fakemail.com',
            password='abc123'
        )
        Todo.objects.create(
            user=self.test_user,
            description='Doing something cool'
        )
        Todo.objects.create(
            user=self.test_user,
            description='Doing something new'
        )
        self.test_another_user = User.objects.create_user(
            username='another_user',
            email='another_user@fakemail.com',
            password='abc123'
        )
        Todo.objects.create(
            user=self.test_another_user,
            description='Doing something boring'
        )
        self.__login__("my_user", "abc123")

    def __login__(self, username, password):
        token = self.client.post(
            reverse('rest_login'),
            data={"username": username, "password": password},
            format="json"
        )
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.data["key"])
        self.client.login(username=username, password=password)

    def test_list_todo(self):
        url = reverse('todo_app:list_create_todo')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_list_todo_with_filter(self):
        url = reverse('todo_app:list_create_todo')
        response = self.client.get(url + "?description=new", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_get_todo_by_id(self):
        url = reverse('todo_app:detail_todo', kwargs={"pk": 1})
        response = self.client.get(url, format="json")
        todo_1 = Todo.objects.get(id=1)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["id"], todo_1.id)
        self.assertEqual(data["complete"], todo_1.complete)
        self.assertEqual(data["description"], todo_1.description)
        self.assertEqual(data['user']['username'], todo_1.user.username)
        self.assertEqual(data['user']['username'], self.test_user.username)

    def test_can_create_todo(self):
        url = reverse('todo_app:list_create_todo')
        data = {"description": "Send important email"}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["complete"], False)
        self.assertEqual(response.json()["description"], "Send important email")

    def test_can_not_create_todo_with_null_description(self):
        url = reverse('todo_app:list_create_todo')
        data = {"description": ""}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["description"][0], "This field may not be blank.")

    def test_can_not_create_todo_without_description(self):
        url = reverse('todo_app:list_create_todo')
        data = {"complete": True}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["description"][0], "This field is required.")

    def test_can_update_todo(self):
        url = reverse('todo_app:detail_todo', kwargs={"pk": 1})
        data = {"complete": True, "description": "Doing something cool!!!"}
        response = self.client.put(url, data=data, format="json")
        todo_1 = Todo.objects.get(id=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(todo_1.complete, True)
        self.assertEqual(todo_1.description, "Doing something cool!!!")

    def test_can_update_todo_without_description(self):
        url = reverse('todo_app:detail_todo', kwargs={"pk": 2})
        response = self.client.put(url, data={"complete": True}, format="json")
        todo_2 = Todo.objects.get(id=2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(todo_2.complete, True)

    def test_can_delete_todo(self):
        url = reverse('todo_app:detail_todo', kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_not_get_todo_from_another_user(self):
        url = reverse('todo_app:detail_todo', kwargs={"pk": 3})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()["detail"], "You do not have permission to perform this action.")

    def test_can_not_update_todo_from_another_user(self):
        url = reverse('todo_app:detail_todo', kwargs={"pk": 3})
        response = self.client.put(url, data={"complete": True}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()["detail"], "You do not have permission to perform this action.")

    def test_can_not_delete_todo_from_another_user(self):
        url = reverse('todo_app:detail_todo', kwargs={"pk": 3})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()["detail"], "You do not have permission to perform this action.")
