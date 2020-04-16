from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import MyUser, Product, Category
from .views import AccountView, ResultsView, SavedFoodView, AddToFavoriteView
from.views import LegalView, IndexView, ContactView, LoginView, ProductView
from.views import RegisterView, DeleteView, LogoutView


class IndexViewTest(TestCase):

    def test_can_access_index_view(self):
        response = self.client.get(reverse('Nutella:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Du gras, oui mais de qualité!")

    def test_index_view_is_tested(self):
        response = self.client.get(reverse('Nutella:index'))
        self.assertEqual(response.resolver_match.func.__name__,
                         IndexView.as_view().__name__)


class LegalViewTest(TestCase):

    def test_can_access_legal_view(self):
        response = self.client.get(reverse('Nutella:legals'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SARL Pur Beurre")

    def test_legal_view_is_tested(self):
        response = self.client.get(reverse('Nutella:legals'))
        self.assertEqual(response.resolver_match.func.__name__,
                         LegalView.as_view().__name__)


class ContactViewTest(TestCase):

    def test_can_access_contact_view(self):
        response = self.client.get(reverse('Nutella:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dites nous tout!")

    def test_contact_view_is_tested(self):
        response = self.client.get(reverse('Nutella:contact'))
        self.assertEqual(response.resolver_match.func.__name__,
                         ContactView.as_view().__name__)


class AccountViewTest(TestCase):

    def setUp(self):
        # create a basic user to interact with in our tests
        self.factory = RequestFactory()
        self.user = MyUser.objects.create_user(
            email='john@doe.com',
            name='john',
            password='johndoe')

    def test_account_view_is_tested(self):
        response = self.client.get(reverse('Nutella:account'))
        self.assertEqual(response.resolver_match.func.__name__,
                         AccountView.as_view().__name__)

    def test_cant_access_account_view_if_not_logged_in(self):
        response = self.client.get(reverse('Nutella:account'))
        self.assertEqual(response.status_code, 302)

    def test_can_access_account_view_if_logged_in(self):
        request = self.factory.get('/account/')
        request.user = self.user
        response = AccountView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Voici les informations que l'on a sur vous...")


class SavedFoodViewTest(TestCase):

    def setUp(self):
        # create a basic user to interact with in our tests
        self.factory = RequestFactory()
        self.user = MyUser.objects.create_user(
            email='john@doe.com',
            name='john',
            password='johndoe')

    def test_saved_food_view_is_tested(self):
        response = self.client.get(reverse('Nutella:saved_food'))
        self.assertEqual(response.resolver_match.func.__name__,
                         SavedFoodView.as_view().__name__)

    def test_cant_access_saved_food_view_if_not_logged_in(self):
        response = self.client.get(reverse('Nutella:saved_food'))
        self.assertEqual(response.status_code, 302)

    def test_can_access_saved_food_view_if_logged_in(self):
        request = self.factory.get('/saved_food/')
        request.user = self.user
        response = SavedFoodView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Vos aliments sauvegardés!")


class AddToFavoriteViewTest(TestCase):

    def setUp(self):
        # create a basic user to interact with in our tests
        self.user = MyUser.objects.create_user(
            email='john@doe.com',
            name='john',
            password='johndoe')
        self.category = Category.objects.create(
            name='test_category'
        )
        self.product = Product.objects.create(
            name='test',
            category=self.category
        )
        self.factory = RequestFactory()

    def test_add_to_favorite_view_is_tested(self):
        response = self.client.post(reverse(
            'Nutella:add_to_favorite',
            args=(10221,)
            ))
        self.assertEqual(response.resolver_match.func.__name__,
                         AddToFavoriteView.as_view().__name__)

    def test_cant_add_to_favorite_if_not_logged_in(self):
        response = self.client.post(reverse(
            'Nutella:add_to_favorite',
            args=(10221,)
        ))
        self.assertEqual(response.status_code, 404)

    def test_can_add_to_favorite_if_logged_in(self):
        request = self.factory.post(reverse(
            'Nutella:add_to_favorite',
            args=(self.product.id,)
        ))
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = AddToFavoriteView.as_view()(
            request,
            product_id=self.product.id)
        self.assertEqual(response.status_code, 302)


class ResultsViewTest(TestCase):

    def setUp(self):
        # create a basic user to interact with in our tests
        self.user = MyUser.objects.create_user(
            email='john@doe.com',
            name='john',
            password='johndoe')

    def test_can_access_results_view_with_post_method(self):
        response = self.client.post('/results/', {'search': 'search_terms'})
        self.assertEqual(response.status_code, 200)

    def test_can_access_results_view_with_get_method_and_session_data(self):
        session = self.client.session
        session['last_search'] = {'search_terms': 'test'}
        session.save()
        response = self.client.get('/results/')
        self.assertEqual(response.status_code, 200)

    def test_results_view_is_tested(self):
        session = self.client.session
        session['last_search'] = {'search_terms': 'test'}
        session.save()
        response = self.client.get(reverse('Nutella:results'))
        self.assertEqual(response.resolver_match.func.__name__,
                         ResultsView.as_view().__name__)

    def test_search_product_method(self):
        pass


class ProductViewTest(TestCase):

    def setUp(self):
        # create a basic user to interact with in our tests
        self.user = MyUser.objects.create_user(
            email='john@doe.com',
            name='john',
            password='johndoe')
        self.category = Category.objects.create(
            name='test_category'
        )
        self.product = Product.objects.create(
            name='test',
            category=self.category
        )
        self.factory = RequestFactory()

    def test_can_access_to_product_view(self):
        request = self.factory.post(reverse(
            'Nutella:product',
            args=(self.product.id,)
        ))
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = AddToFavoriteView.as_view()(
            request,
            product_id=self.product.id)
        self.assertEqual(response.status_code, 302)


class LoginViewTest(TestCase):

    def setUp(self):
        # create a basic user to interact with in our tests
        self.user = MyUser.objects.create_user(
            email='john@doe.com',
            name='john',
            password='johndoe')

    def test_login_view_is_tested(self):
        response = self.client.get(reverse('Nutella:login'))
        self.assertEqual(response.resolver_match.func.__name__,
                         LoginView.as_view().__name__)

    def test_can_access_login_view(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_can_log_in_with_correct_values(self):
        response = self.client.post(
            '/login/',
            {'name': 'john@doe.com', 'password': 'johndoe'})
        self.assertEqual(response.status_code, 200)

    def test_cannot_log_in_with_incorrect_data(self): # à vérifier
        self.client.post(
            '/login/',
            {'name': 'joe_test', 'password': ''}
        )
        self.assertEqual(request.user, None)

    def test_get_redirected_to_home_page_when_logged_in(self): # à vérifier
        response = self.client.post(
            '/login/',
            {'name': 'john@doe.com', 'password': 'johndoe'})
        self.assertEqual(response.url, '/')


class DeleteViewTest(TestCase):

    def setUp(self):
        # create a basic user to interact with in our tests
        self.user = MyUser.objects.create_user(
            email='john@doe.com',
            name='john',
            password='johndoe')
        self.category = Category.objects.create(
            name='test_category'
        )
        self.product = Product.objects.create(
            name='test',
            category=self.category
        )
        self.factory = RequestFactory()

    def test_delete_view_is_tested(self):
        response = self.client.get(reverse(
            'Nutella:delete',
            args=(10221,)
        ))
        self.assertEqual(response.resolver_match.func.__name__,
                         DeleteView.as_view().__name__)

    def test_call_delete_view_without_product_id_get_404(self):
        response = self.client.post(reverse(
            'Nutella:delete',
            args=(0,)
        ))
        self.assertEqual(response.status_code, 404)

    def test_get_redirected_to_saved_food_page_when_deleting(self):
        request = self.factory.post(reverse(
            'Nutella:product',
            args=(self.product.id,)
        ))
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = DeleteView.as_view()(
            request,
            product_id=self.product.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/saved_food/')


class RegisterViewTest(TestCase):

    def test_register_view_is_tested(self):
        response = self.client.get(reverse('Nutella:register'))
        self.assertEqual(response.resolver_match.func.__name__,
                         RegisterView.as_view().__name__)

    def test_can_access_register_view(self):
        response = self.client.get(reverse('Nutella:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Créer un compte")

    def can_register_with_post_method(self):
        self.client.post(
            '/register/',
            {'name': 'john@doe.com', 'password': 'johndoe'}
        )
        new_user = MyUser.objects.last()
        self.assertEquals(new_user.name, 'john@doe.com')

    def test_cannot_register_with_incorrect_data(self):
        self.client.post(
            '/register/',
            {'name': 'joe_test', 'password': ''}
        )
        new_user = MyUser.objects.last()
        self.assertEqual(new_user, None)

    def test_get_redirected_to_home_page_when_registered(self): # à vérifier
        response = self.client.post(
            '/register/',
            {'name': 'john@doe.com', 'password': 'johndoe'}
            )
        self.assertEqual(response.url, '/')


class LogoutViewTest(TestCase):

    def setUp(self):
        # create a basic user to interact with in our tests
        self.user = MyUser.objects.create_user(
            email='john@doe.com',
            name='john',
            password='johndoe')
        self.client.post(
            '/login/',
            {'name': 'john@doe.com', 'password': 'johndoe'})

    def test_logout_view_is_tested(self):
        response = self.client.get(reverse('Nutella:logout'))
        self.assertEqual(response.resolver_match.func.__name__,
                         LogoutView.as_view().__name__)

    def test_logout_when_logged_in(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

    def test_get_redirected_to_home_page_when_logged_out(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.url, '/')


class AdminViewTest(TestCase):

    def test_can_access_admin_view(self):
        response = self.client.get(reverse('Nutella:register'))
        self.assertEqual(response.status_code, 200)
