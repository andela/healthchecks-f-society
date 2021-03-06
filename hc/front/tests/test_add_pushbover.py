from django.test.utils import override_settings
from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddPushoverTestCase(BaseTestCase):
    def test_it_adds_channel(self):
        self.client.login(
            username="alice@example.org", password="password")

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        params = "pushover_user_key=a&nonce=n&prio=0"
        r = self.client.get("/integrations/add_pushover/?%s" % params)
        assert r.status_code == 302

        channels = list(Channel.objects.all())
        assert len(channels) == 1
        assert channels[0].value == "a|0"

    @override_settings(PUSHOVER_API_TOKEN=None)
    def test_it_requires_api_token(self):
        self.client.login(
            username="alice@example.org",password="password")

        r = self.client.get("/integrations/add_pushover/")
        self.assertEqual(r.status_code, 404)

    def test_it_validates_nonce(self):
        self.client.login(
            username="alice@example.org", password="password")

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        params = "pushover_user_key=a&nonce=INVALID&prio=0"
        r = self.client.get("/integrations/add_pushover/?%s" % params)
        assert r.status_code == 403


    def test_pushover_validates_priority(self):
        """Test that pushover validates priority"""
        self.client.login(
            username='alice@example.org', password='password')

        session = self.client.session
        # set po_once to n
        session["po_nonce"] = "n"
        session.save()
        # set prio to a number greater than 2
        params = "pushover_user_key=a&nonce=n&prio=3"
        response = self.client.get('/integrations/add_pushover/?%s' % params)
        self.assertEqual(response.status_code, 400)


    def test__it_checks_nonce_and_po_nonce_are_equal(self):
        """Test that check nonce and po_nonce are equal"""
        self.client.login(
            username='alice@example.org', password='password')

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        # set nonce to different value from session po_once
        params = "pushover_user_key=a&nonce=s&prio=0"
        response = self.client.get("/integrations/add_pushover/?%s" % params)
        self.assertEqual(response.status_code, 403)

    def test_it_requires_nonce(self):
        """Test that integration requires nonce"""
        self.client.login(username='alice@example.org', password='password')

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        # omit nonce in param
        params = "pushover_user_key=a&prio=0"
        response = self.client.get("/integrations/add_pushover/?%s" % params)
        self.assertEqual(response.status_code, 400)

    def test_it_requires_prio(self):
        """Test that integration requires prio"""
        self.client.login(username='alice@example.org', password='password')

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        # omit prio in param
        params = "pushover_user_key=a&nonce=n"
        response = self.client.get("/integrations/add_pushover/?%s" % params)
        self.assertEqual(response.status_code, 400)
