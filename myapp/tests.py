from gettext import find
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .views import signin,signup,home,findflight
# Create your tests here.

USER_NAME = "testuser"
USER_EMAIL = "test@test.com"
USER_PASSWORD = "testuser"

class AuthenticationTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username = USER_NAME, email=USER_EMAIL,password=USER_PASSWORD
        )
    def test_authenticated(self):
        request = self.factory.get("")
        request.user = self.user
        response = home(request)
        self.assertEqual(response.status_code,200)
    def test_login(self):
        request = self.factory.post("signin")
        request.user = self.user
        response = signin(request)
        
        self.assertEqual(response.status_code,200)

    

class BookingTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username = USER_NAME, email=USER_EMAIL,password=USER_PASSWORD
        )
    def test_findflight_found(self):
        data = {"source": "Kabankalan","destination":"Himamaylan","date":"2021-03-04"}
        request = self.factory.post("findflight",data)
        request.user = self.user
        # request.method = "POST"
        # request.user = self.user
        # request.data = data

        response = findflight(request)
        print(response)
        self.assertEqual(response.status_code,200)
        # self.assertTemplateUsed(response,"list.html")
        # request.source = "Kabankalan"
        # request.destination = "Himamaylan"
        # request.date = "04/03/2021"
        reponse = self.factory.get("findflight")
        # self.assertTemplateUsed(response,"list.html")
        print(response)

        # response = findflight(request)
        
        # self.assertEqual(response.context["object_list"]["error"],self.user)
    def test_findflight_not_found(self):
        data = {"source": "abankalan","destination":"Himamaylan","date":"2021-03-04"}
        request = self.factory.post("findflight",data)
        request.user = self.user
        # request.method = "POST"
        # request.user = self.user
        # request.data = data

        response = findflight(request)
        print(response)
        self.assertEqual(response.status_code,200)
        # self.assertTemplateUsed(response,"list.html")
        # request.source = "Kabankalan"
        # request.destination = "Himamaylan"
        # request.date = "04/03/2021"
        reponse = self.client.get("findflight")
        # self.assertTemplateUsed(response,"list.html")

        # response = findflight(request)
        
        # self.assertEqua   