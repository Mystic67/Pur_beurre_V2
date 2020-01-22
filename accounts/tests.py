from django.contrib.auth.forms import PasswordChangeForm
from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import login, get_user, authenticate

from accounts.forms import RegisterForm, LoginForm, AccountForm
from .models import User


class LoginPageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='Sebastien@fakemail.com')
        self.user.set_password('fake_password')
        self.user.save()
        self.good_user_data = {'email': 'Sebastien@fakemail.com',
                               'password': 'fake_password'}
        self.bad_user_data = {'email': 'Sebastien',
                              'password': 'fake'}

    def test_display_login_page(self):
        # Test if login page is loaded
        client = Client()
        response = client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_form_is_valid_with_good_user_data(self):
        """Test if login form with good user data is valid"""
        loginForm = LoginForm(self.good_user_data)
        self.assertTrue(loginForm.is_valid())

    def test_login_form_is_not_valid_with_bad_user_data(self):
        """Test if login form with bad user data is invalide"""
        loginForm = LoginForm(self.bad_user_data)
        self.assertFalse(loginForm.is_valid())

    def test_login_page_posted_with_good_user_data(self):
        """ If user data are good, then is the user is authenticate and redirect to index page """
        client = Client()
        response = client.post(reverse('accounts:login'), self.good_user_data)
        # Test if user is authenticate
        user = get_user(client)
        self.assertTrue(user.is_authenticated)
        # Test if page redirection
        self.assertEqual(response.status_code, 302)

    def test_login_page_posted_with_bad_user_data(self):
        """ If user data are bad, user is not authenticate and refresh the login page """
        client = Client()
        response = client.post(reverse('accounts:login'), self.bad_user_data)
        user = get_user(client)
        self.assertFalse(user.is_authenticated)
        self.assertEqual(response.status_code, 200)


class LogoutPageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='Sebastien@fakemail.com')
        self.user.set_password('fake_password')
        self.user.save()

    def test_logout_page(self):
        client = Client()
        client.force_login(self.user)
        # Test if user is logged in after login
        user = get_user(client)
        self.assertFalse(user.is_anonymous)
        # Call logout page
        response = client.get(reverse('accounts:logout'))
        # Test if user is unlogged after call logout page
        user = get_user(client)
        self.assertTrue(user.is_anonymous)
        # Test if redirect after call logout page
        self.assertEqual(response.status_code, 302)


class RegisterPageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='Sebastien@fakemail.com', password='fake_password')
        self.user.save()
        # Neu user data, not exist in database
        self.good_user_data = {'email': 'Sebastien@anotherfakemail.com',
                               'password1': 'another_fake_password',
                               'password2': 'another_fake_password'}
        # User already exists in database
        self.bad_user_data = {'email': 'Sebastien@fakemail.com',
                              'password1': 'fake_password',
                              'password2': 'fake_password'}

    def test_display_register_page(self):
        client = Client()
        # Test if register page is loaded
        response = client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_form_is_valid_with_good_user_data(self):
        # Test if register form with bad user data is valide
        registerForm = RegisterForm(self.good_user_data)
        self.assertTrue(registerForm.is_valid())

    def test_register_form_is_not_valid_with_bad_user_data(self):
        # Test if register form with bad user data is invalide
        registerForm = RegisterForm(self.bad_user_data)
        self.assertFalse(registerForm.is_valid())

    def test_register_page_posted_with_good_user_data(self):
        """ If user entries are god, then is the user is authenticate and redirect to index page """
        client = Client()
        response = client.post(reverse('accounts:register'), self.good_user_data)
        # Test if user is authenticate
        user = get_user(client)
        self.assertTrue(login)
        # Test if user is not saved in database
        # One user is already saved in database in setUp also yet must be two user saved
        user_in_database = len(User.objects.all())
        self.assertEqual(user_in_database, 2)
        # Test if page redirection
        self.assertEqual(response.status_code, 302)

    def test_register_page_posted_with_bad_user_data(self):
        """ If user entries are bad, user is not authenticate and refresh the login page """
        client = Client()
        response = client.post(reverse('accounts:register'), self.bad_user_data)
        # Test if user is not authenticate
        user = get_user(client)
        self.assertFalse(user.is_authenticated)
        # Test if user is not saved in database
        # One user is already saved in database in setUp also yet must be only one user saved
        user_in_database = len(User.objects.all())
        self.assertEqual(user_in_database, 1)
        # Test if reload the page
        self.assertEqual(response.status_code, 200)


class AccountPageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='Sebastien@fakemail.com')
        # self.current_user = User.objects.get(pk=self.user.id)
        self.user.set_password('fake_password')
        self.user.save()
        self.good_user_data = {'email': 'Sebastien@fakemail.com'}
        self.bad_user_data = {'email': 'Sebastien'}
        self.updated_good_user_data = {'username': 'fakeusername', 'email': 'Sebastien@fakemail.com'}

    def test_display_account_page_is_loaded(self):
        client = Client()
        # Logged user and test if user is logged
        client.force_login(self.user)
        self.assertTrue(login)
        # Test if myaccount page is loaded
        response = client.get(reverse('accounts:myaccount'))
        self.assertEqual(response.status_code, 200)

    def test_account_form_is_valid_with_good_user_data(self):
        """Test if login form with good user data is valid"""
        # Tests if account form is valid with good user data (needed user instance)
        accountForm = AccountForm(self.good_user_data, instance=self.user)
        self.assertTrue(accountForm.is_valid())

    def test_account_form_is_not_valid_with_bad_user_data(self):
        """Test if login form with bad user data is invalide"""
        client = Client()
        # Tests if account form is invalid with bad user data (needed user instance)
        accountForm = AccountForm(self.bad_user_data, instance=self.user)
        self.assertFalse(accountForm.is_valid())

    def test_account_page_posted_with_good_user_data(self):
        client = Client()
        # Logged user and test if user is logged
        client.force_login(self.user)
        self.assertTrue(login)
        # Test if account page is redirected when posted with good user data
        response = client.post(reverse('accounts:myaccount'), self.updated_good_user_data)
        self.assertEqual(response.status_code, 302)
        # Test if database is updated
        updated_user = User.objects.get(pk=self.user.id)
        self.assertEqual(updated_user.username, self.updated_good_user_data['username'])
        self.assertEqual(updated_user.email, self.updated_good_user_data['email'])

    def test_account_page_posted_with_bad_user_data(self):
        client = Client()
        # Logged user and test if user is logged
        client.force_login(self.user)
        self.assertTrue(login)
        # Test if account page is redirected when posted with good user data
        response = client.post(reverse('accounts:myaccount'), self.bad_user_data)
        self.assertEqual(response.status_code, 200)


class PassWordResetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='Sebastien@fakemail.com')
        self.user.set_password('fake_password')
        self.user.save()
        self.client = Client()
        self.new_password = "new_fake_password"

    def test_password_reset_page(self):
        response = self.client.get(reverse('accounts:password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'accounts/password_reset.html')

        # Post the response with user "email address"
        response = self.client.post(reverse('accounts:password_reset'), {'email': 'Sebastien@fakemail.com'})
        self.assertEqual(response.status_code, 302)

        # Check if email is send with subject
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Réinitialisation de votre mot de passe pur beurre.')
        # Create user id and token
        uid = response.context[0]['uid']
        token = response.context[0]['token']
        return uid, token

    def test_password_reset_done_page(self):
        response = self.client.get(reverse('accounts:password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'accounts/password_reset_done.html')

    def test_password_reset_confirm_page_with_uid_and_token_to_get_password_change_form(self):
        self.uid, self.token = self.test_password_reset_page()
        response = self.client.get(reverse('accounts:password_reset_confirm', kwargs={'uidb64': self.uid,
                                                                                      'token': self.token}),
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'accounts/password_reset_confirm.html')

    def test_password_reset_confirm_page_with_new_password(self):
        # Check if old password is in database
        user = User.objects.get(email='Sebastien@fakemail.com')
        self.assertEqual(user.check_password('fake_password'), True)
        # Get password change page
        self.test_password_reset_confirm_page_with_uid_and_token_to_get_password_change_form()
        # Post password change page with new password
        response = self.client.post(reverse('accounts:password_reset_confirm', kwargs={'uidb64': self.uid,
                                                                                       'token': "set-password"}),
                                    {'new_password1': self.new_password, 'new_password2': self.new_password},
                                    follow=True)
        # Check the reponse page
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'accounts/password_reset_complete.html')
        # Check if new password has been set in database
        user = User.objects.get(email='Sebastien@fakemail.com')
        self.assertEqual(user.check_password(self.new_password), True)

    def test_password_reset_complete_page(self):
        response = self.client.get(reverse('accounts:password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'accounts/password_reset_complete.html')


class PasswordChangeTestCase(TestCase):
    def setUp(self):
        # Init database with user and password
        self.user = User.objects.create(email='Sebastien@fakemail.com')
        self.user.set_password('fake_password')
        self.user.save()
        self.client = Client()
        self.client.login(email='Sebastien@fakemail.com', password="fake_password")
        self.old_password = 'fake_password'
        self.new_password = 'new_fake_password'
        self.data = {
            'old_password': self.old_password,
            'new_password1': self.new_password,
            'new_password2': self.new_password,
        }

    def test_password_change_get_page(self):
        user = User.objects.get(email='Sebastien@fakemail.com')
        self.assertEqual(user.check_password(self.old_password), True)
        response = self.client.get(reverse('accounts:password_change'))
        self.assertEqual(response.status_code, 200)

    def test_password_change_post_page_with_data(self):
        # Test if user is authenticated
        self.assertTrue(self.user.is_authenticated)
        # Test if form with fake data is valid
        form = PasswordChangeForm(self.user, self.data)
        self.assertTrue(form.is_valid())
        # Check if old password in database before POST passwword change page with valid data
        user = User.objects.get(email='Sebastien@fakemail.com')
        self.assertEqual(user.check_password(self.old_password), True)
        # Post passwword change page with valid data
        response = self.client.post(reverse('accounts:password_change'), self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        # Check if password has been changed after POST passwword change page with valid data
        user = User.objects.get(email='Sebastien@fakemail.com')
        self.assertEqual(user.check_password(self.new_password), True)
        #self.assertEqual(response.template_name[0], 'accounts/password_change_done.html')
        print(response.context)



