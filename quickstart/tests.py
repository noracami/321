from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory

#from django.core.urlresolvers import Resolver404
#from rest_framework.routers import DefaultRouter

# Create your tests here.
class BasicTestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        # self.factory = RequestFactory()
        self.superuser = User.objects.create_superuser('lena', 'abc@x.yz', 'password')
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'pwd')
        self.anonymoususer = AnonymousUser()

    def test_root_superuser(self):
        self.client.logout()
        self.logged_in = self.client.login(username=self.superuser.username, password='password')
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_root_user(self):
        self.client.logout()
        self.logged_in = self.client.login(username=self.user.username, password='pwd')
        r = self.client.get('/')
        self.assertEqual(r.status_code, 403)

    #def test_details(self):
        # Create an instance of a GET request.
        #request = self.factory.get('/customer/details')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        #request.user = self.user

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        # request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        # response = my_view(request)
        # Use this syntax for class-based views.
        # response = MyView.as_view()(request)
        # self.assertEqual(response.status_code, 200)
        #UserViewSet
        #APIRoot
        #Resolver404
        #response = self.client.get('/')
        #with self.assertRaises(Resolver404, response.resolver_match.func, _) as cm:
        #    pass

        #the_exception = cm.exception
        #self.assertEqual(the_exception.error_code, 9)

        #response = self.client.get('/')
        #d = DefaultRouter('/a')
        #self.assertEqual(response.resolver_match.func.__name__, d.get_api_root_view().__name__)
