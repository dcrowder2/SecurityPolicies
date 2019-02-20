from django.test import TestCase, RequestFactory, Client
from SecurityApp.views import logon
from SecurityApp.models import Logon, User
import time
import datetime
from django.contrib.sessions.middleware import SessionMiddleware



class LogonTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="base_user", password="SecurePassword1")
        temp = User.objects.get_by_natural_key("base_user")
        Logon.objects.create(user_id=temp.id)
        temp.save()
        User.objects.create_user(username="locked_out_user", password="StillSecure1")
        temp = User.objects.get_by_natural_key("locked_out_user")
        Logon.objects.create(user_id=temp.id, user_lockout=True, lockouts=1, lockout_time=time.time())
        temp.save()
        User.objects.create_user(username="almost_locked_out", password="Thereisnowaythisissecure1")
        temp = User.objects.get_by_natural_key("almost_locked_out")
        Logon.objects.create(user_id=temp.id, logon_attempts=4, attempt_time=time.time())
        temp.save()
        User.objects.create_user(username="To_be_unlocked", password="OkayThisoneMightBeSecure91123")
        temp = User.objects.get_by_natural_key("To_be_unlocked")
        Logon.objects.create(user_id=temp.id, user_lockout=True, lockouts=1, lockout_time=(time.time())-901)
        temp.save()
        User.objects.create_user(username="almost_hardlocked", password="EnoughOfTheseSillyPasswords1")
        temp = User.objects.get_by_natural_key("almost_hardlocked")
        Logon.objects.create(user_id=temp.id, logon_attempts=4, lockouts=2, lockout_time=time.time(), attempt_time=time.time())
        temp.save()
        User.objects.create_user(username="Shouldnt_be_locked_out", password="aVaeGrTahe!223h!a3h@3ha")
        temp = User.objects.get_by_natural_key("Shouldnt_be_locked_out")
        Logon.objects.create(user_id=temp.id, logon_attempts=4, attempt_time=(time.time()-301))
        temp.save()

    def test_logging_on(self):
        base_user = User.objects.get_by_natural_key("base_user")
        locked_out_user = User.objects.get_by_natural_key("locked_out_user")
        almost_locked_out = User.objects.get_by_natural_key("almost_locked_out")
        to_be_unlocked = User.objects.get_by_natural_key("To_be_unlocked")
        to_be_hard_locked_out = User.objects.get_by_natural_key("almost_hardlocked")
        shouldnt_be_locked_out = User.objects.get_by_natural_key("Shouldnt_be_locked_out")
        request_creator = RequestFactory()
        response_creator = Client()
        # testing base user
        context = {
            "logon": True,
            "username": base_user.username,
            "password": "SecurePassword1",
        }
        # base user should be able to login just fine
        temp = request_creator.post("", context)
        temp.session = response_creator.session
        # 302 is a proper redirect
        self.assertEqual(logon(temp).status_code, 302)

        # testing locked out user
        context = {
            "logon": True,
            "username": locked_out_user.username,
            "password": "wrong_password"
        }
        ret_context = {
            "logon": True,
            "username": locked_out_user.username,
            "password": "wrong_password",
            'user_locked_out': True,
            'time': "0:15:00",
            'lockouts': locked_out_user.logon.lockouts
        }
        # the first 114 are enough to distinguish the results, as the timing messes up sometimes, and there is a csrf token
        # that changes every run so it will never be the same, therefore it is excluded
        self.assertEqual(logon(request_creator.post("", context)).content[:114], response_creator.post("", ret_context).content[:114])

        # testing locking out a user who has failed too many times
        context = {
            "logon": True,
            "username": almost_locked_out.username,
            "password": "wrong_password"
        }
        ret_context = {
            "logon": True,
            "username": locked_out_user.username,
            "password": "wrong_password",
            'user_locked_out': True,
            'time': "0:15:00",
            'lockouts': locked_out_user.logon.lockouts
        }
        temp = logon(request_creator.post("", context))
        # Same as before, the first 114 will be the part that changes
        self.assertEqual(temp.content[:114], response_creator.post("", ret_context).content[:114])

        # testing the unlocking and subsequent redirect of a user
        context = {
            "logon": True,
            "username": to_be_unlocked.username,
            "password": "OkayThisoneMightBeSecure91123"
        }
        temp = request_creator.post("", context)
        temp.session = response_creator.session
        # It should successfully redirect
        self.assertEqual(logon(temp).status_code, 302)

        # testing the hard locking of a user
        context = {
            "logon": True,
            "username": to_be_hard_locked_out.username,
            "password": "wrong_password"
        }
        temp = logon(request_creator.post("", context))
        # this is the first part of the response that shows it is hard locked, i had to hard code this for reasons of
        # django being real bad at handling database changes in a test database it seems
        response = b'\n\n\n    <p><font color="red">This account is locked out</font> </p>\n    <p><font color="red">Please contact an administrator to unlock your account</font>'
        self.assertEqual(temp.content[:153], response)

        # This user should not be locked out because it has been more than 5 minutes since they started to fail their password
        # so their counter should go back to 1, giving 4 more attempts
        context = {
            "logon": True,
            "username": shouldnt_be_locked_out.username,
            "password": "wrong_password"
        }
        ret_context = {
            "logon": True,
            "username": shouldnt_be_locked_out.username,
            "password": "wrong_password",
        }
        temp = logon(request_creator.post("", context))
        # the content that should be returned
        response = b'\n\n\n    <p><font color="red">Incorrect Login, please try again</font> </p>\n    <p><font color="red">4/5 attemps remaing</font>'
        self.assertEqual(temp.content[:125], response)

        # testing a random username that isn't a real user
        context = {
            'logon': True,
            'username': "Not_real_user",
            'password': "doesn't matter",
        }

        temp = logon(request_creator.post("", context))
        response = b'\n\n\n    <p><font color="red">Incorrect Login</font></p>'
        self.assertEqual(temp.content[:54], response)
