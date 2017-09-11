from django.conf import settings
from django.core.signing import base64_hmac

from hc.api.models import Check
from hc.test import BaseTestCase


class BadgeTestCase(BaseTestCase):
    """Contains budge tests"""
    def setUp(self):
        super(BadgeTestCase, self).setUp()
        self.check = Check.objects.create(user=self.alice, tags="foo bar")

    def test_it_rejects_bad_signature(self):
        """Test it regects bad signature"""
        r = self.client.get("/badge/%s/12345678/foo.svg" % self.alice.username)
        result = r.status_code
        self.assertEquals(result, 400)

    def test_it_returns_svg(self):
        """Test it returns a svg"""
        sig = base64_hmac(str(self.alice.username), "foo", settings.SECRET_KEY)
        sig = sig[:8].decode("utf-8")
        url = "/badge/%s/%s/foo.svg" % (self.alice.username, sig)
        r = self.client.get(url)
        self.assertContains(r, "xml")
