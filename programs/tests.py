from django.test import TestCase, RequestFactory, Client
from programs.models import Programs
from django.contrib.auth.models import User, Group
from SecurityApp.views import logon
from SecurityApp.models import Logon
from programs.views import programs


# Create your tests here.

class ProgramsTestCase(TestCase):
    def setUp(self):
        Programs.objects.create(name="User Program", permission_level="U")
        Programs.objects.create(name="Software engineer program", permission_level="SE")
        Programs.objects.create(name="Admin program", permission_level="A")
        Group.objects.create(name="super_admin")
        Group.objects.create(name="admin")
        Group.objects.create(name="software_engineer")
        Group.objects.create(name="user")
        User.objects.create_user(username="Super_admin", password="SecurePasswd1")
        User.objects.create_user(username="admin", password="SecurePasswd2")
        User.objects.create_user(username="software_engineer", password="SecurePasswd3")
        User.objects.create_user(username="user", password="SecurePasswd4")
        Logon.objects.create(user_id=1)
        Logon.objects.create(user_id=2)
        Logon.objects.create(user_id=3)
        Logon.objects.create(user_id=4)
        temp_group = Group.objects.get_by_natural_key("super_admin")
        temp_group.user_set.add(User.objects.get_by_natural_key("Super_admin"))
        temp_group.save()
        temp_group = Group.objects.get_by_natural_key("admin")
        temp_group.user_set.add(User.objects.get_by_natural_key("admin"))
        temp_group.save()
        temp_group = Group.objects.get_by_natural_key("software_engineer")
        temp_group.user_set.add(User.objects.get_by_natural_key("software_engineer"))
        temp_group.save()
        temp_group = Group.objects.get_by_natural_key("user")
        temp_group.user_set.add(User.objects.get_by_natural_key("user"))
        temp_group.save()

    def test_programs(self):
        super_admin = User.objects.get_by_natural_key("Super_admin")
        admin = User.objects.get_by_natural_key("admin")
        software_engineer = User.objects.get_by_natural_key("software_engineer")
        user = User.objects.get_by_natural_key("user")
        request_creator = RequestFactory()
        response_creator = Client()

        # Logging in all the users so I can access the page
        temp = request_creator.post("", {'logon': True, 'username': super_admin.username, 'password': "SecurePasswd1"})
        temp.session = response_creator.session
        logon(temp)
        super_admin_session = temp.session

        temp = request_creator.post("", {'logon': True, 'username': admin.username, 'password': "SecurePasswd2"})
        temp.session = response_creator.session
        logon(temp)
        admin_session = temp.session

        temp = request_creator.post("", {'logon': True, 'username': software_engineer.username, 'password': "SecurePasswd3"})
        temp.session = response_creator.session
        logon(temp)
        software_engineer_session = temp.session

        temp = request_creator.post("", {'logon': True, 'username': user.username, 'password': "SecurePasswd4"})
        temp.session = response_creator.session
        logon(temp)
        user_session = temp.session

        # Testing what the super_admin can see
        temp = request_creator.get("/programs", {})
        temp.user = super_admin
        temp.session = super_admin_session
        retrn = programs(temp)
        # Because I am testing what programs can be selected, here is the actual programs that should be viewable
        comp_value = b'<select name="programs" size="6">\n      \n      \n        \n            <option value="User Program">User Program</option>\n        \n      \n      \n        \n            <option value="Software engineer program">Software engineer program</option>\n        \n      \n      \n        \n            <option value="Admin program">Admin program</option>\n        \n      \n  </select>\n  <input type="submit">\n</form>\n\n\n'
        self.assertEqual(retrn.content[-400:], comp_value)

        # Testing what the admin can see
        temp = request_creator.get("/programs", {})
        temp.user = admin
        temp.session = admin_session
        retrn = programs(temp)
        # Admin should see the same as super_Admin
        comp_value = b'<select name="programs" size="6">\n      \n      \n        \n            <option value="User Program">User Program</option>\n        \n      \n      \n        \n            <option value="Software engineer program">Software engineer program</option>\n        \n      \n      \n        \n            <option value="Admin program">Admin program</option>\n        \n      \n  </select>\n  <input type="submit">\n</form>\n\n\n'
        self.assertEqual(retrn.content[-400:], comp_value)

        # Testing what the software_engineer can see
        temp = request_creator.get("/programs", {})
        temp.user = software_engineer
        temp.session = software_engineer_session
        retrn = programs(temp)
        # Because I am testing what programs can be selected, here is the actual programs that should be viewable
        comp_value = b'<select name="programs" size="6">\n      \n      \n        \n            \n                <option value="User Program">User Program</option>\n            \n        \n      \n      \n        \n            \n                <option value="Software engineer program">Software engineer program</option>\n            \n        \n      \n      \n        \n            \n        \n      \n  </select>\n  <input type="submit">\n</form>\n\n\n'
        self.assertEqual(retrn.content[-408:], comp_value)

        # Testing what a User can see
        temp = request_creator.get("/programs", {})
        temp.user = user
        temp.session = user_session
        retrn = programs(temp)
        # Because I am testing what programs can be selected, here is the actual programs that should be viewable
        comp_value = b'<select name="programs" size="6">\n      \n      \n        \n            \n             <option value="User Program">User Program</option>\n            \n        \n      \n      \n        \n            \n        \n      \n      \n        \n            \n        \n      \n  </select>\n  <input type="submit">\n</form>\n\n\n'
        self.assertEqual(retrn.content[-299:], comp_value)
