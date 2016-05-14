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


class PriceTestCase(TestCase):
    def setUp(self):
        pass

    def test_askTAAZE(self):
        from quickstart.price import PriceInvestigator
        a = PriceInvestigator()
        a.askTAAZE(book='大數據', number=3)
        output = a.price(book=None, debug=False)
        a.clear()
