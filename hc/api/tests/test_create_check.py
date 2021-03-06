import json

from django.utils.encoding import force_text
from hc.api.models import Channel, Check
from hc.test import BaseTestCase


class CreateCheckTestCase(BaseTestCase):
    """Test create chech"""
    URL = "/api/v1/checks/"

    def post(self, data, expected_error=None):
        """Make a post request to /api/v1/checks/"""
        r = self.client.post(self.URL, json.dumps(data),
                             content_type="application/json")

        if expected_error:
            self.assertEqual(r.status_code, 400)
            self.assertEqual(json.loads(
                r.content.decode('utf-8'))['error'], expected_error)

        return r

    def test_it_works(self):
        """Test create check works"""
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
        })

        self.assertEqual(r.status_code, 201)

        doc = r.json()
        assert "ping_url" in doc
        self.assertEqual(doc["name"], "Foo")
        self.assertEqual(doc["tags"], "bar,baz")

        self.assertEqual(Check.objects.count(), 1)
        check = Check.objects.get()
        self.assertEqual(check.name, "Foo")
        self.assertEqual(check.tags, "bar,baz")
        self.assertEqual(check.timeout.total_seconds(), 3600)
        self.assertEqual(check.grace.total_seconds(), 60)

    def test_it_accepts_api_key_in_header(self):
        """Test It accepsts api key in the header"""
        payload = json.dumps({"name": "Foo"})

        r = self.client.post(
            self.URL,
            payload,
            content_type='application/json',
            HTTP_X_API_KEY='abc'
        )

        self.assertEqual(r.status_code, 201)

    def test_it_handles_missing_request_body(self):
        """Test it handles missing request body"""
        r = self.client.post(self.URL, content_type='application/json')

        self.assertEqual(json.loads(r.content.decode('utf-8'))['error'],
                         "wrong api_key")
        self.assertEqual(r.status_code, 400)

    def test_it_handles_invalid_json(self):
        """Test it handles invalid json data type"""
        r = self.client.post(self.URL, ["this is my data"],
                             content_type='application/json')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(json.loads(r.content.decode('utf-8'))['error'],
                         "could not parse request body")

    def test_it_rejects_wrong_api_key(self):
        """Test it rejects wrong API"""
        self.post({"api_key": "wrong"},
                  expected_error="wrong api_key")

    def test_it_rejects_non_number_timeout(self):
        """Test it rejects non number timeout"""
        self.post({"api_key": "abc", "timeout": "oops"},
                  expected_error="timeout is not a number")

    def test_it_rejects_non_string_name(self):
        """Test it regects non string name"""
        self.post({"api_key": "abc", "name": False},
                  expected_error="name is not a string")

    def test_assigns_channels(self):
        """Tests the assignment works"""
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60})
        check = Check.objects.get()
        self.assertTrue(check.assign_all_channels)

    def test_timeout_is_too_small(self):
        """Test timeout is too small"""
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 1,
            "grace": 60})
        string_content = r.content.decode("utf-8")
        json_content = json.loads(string_content)
        self.assertEqual(json_content.get("error"), "timeout is too small")
