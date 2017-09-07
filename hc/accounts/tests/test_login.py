from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from hc.api.models import Check


class LoginTestCase(TestCase):

    def test_it_sends_link(self):
        check = Check()
        check.save()
        code = check.code

        session = self.client.session
        session["welcome_code"] = str(check.code)
        session.save()

        form = {"email": "alice@example.org"}

        r = self.client.post("/accounts/login/", form)
        assert r.status_code == 302

        ### Assert that a user was created
        user = User.objects.get(email=form.get('email'))
        self.assertEqual(user.email, form.get('email'))


        # And email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Log in to healthchecks.io')

        ### Assert contents of the email body
        self.assertIn('please open the link below', mail.outbox[0].body,)

        ### Assert that check is associated with the new user
        chk = Check.objects.get(user_id=user.id)
        self.assertEqual(chk.user_id, user.id)
        self.assertEqual(chk.code, code)


    def test_it_pops_bad_link_from_session(self):
        self.client.session["bad_link"] = True
        self.client.get("/accounts/login/")
        assert "bad_link" not in self.client.session

        ### Any other tests?

