"""Unit tests for djblets.configforms.forms.ConfigPageForm."""

from __future__ import unicode_literals

import warnings

from django import forms
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django.utils import six

from djblets.configforms.forms import ConfigPageForm
from djblets.configforms.pages import ConfigPage
from djblets.configforms.views import ConfigPagesView
from djblets.testing.testcases import TestCase


class TestForm(ConfigPageForm):
    form_id = 'my-form'
    field1 = forms.CharField(label='Field 1',
                             required=False)
    field2 = forms.CharField(label='Field 2',
                             required=False)


class TestPage(ConfigPage):
    page_id = 'my-page'
    form_classes = [TestForm]


class ConfigPageFormTests(TestCase):
    """Unit tests for djblets.configforms.forms.ConfigPageForm."""

    def setUp(self):
        super(ConfigPageFormTests, self).setUp()

        request = RequestFactory().request()
        user = User.objects.create_user(username='test-user',
                                        password='test-user')
        page = TestPage(ConfigPagesView, request, user)

        self.form = TestForm(page, request, user)

    def test_profile(self):
        """Testing ConfigPageForm.profile raises a deprecation warning"""
        with warnings.catch_warnings(record=True) as w:
            try:
                self.form.profile
            except Exception:
                # This is either a SiteProfileNotAvailable (on Django 1.6) or
                # an AttributeError (Django 1.7+). Ignore it. We only care
                # about the warning.
                pass

        # We may get two warnings: One about the get_profile() deprecation in
        # Django 1.6, the other about our own deprecation. Ours will be first.
        message = w[0].message

        self.assertIsInstance(message, DeprecationWarning)
        self.assertEqual(
            six.text_type(message),
            'ConfigFormPage.profile is deprecated. Update your code to '
            'fetch the profile manually instead.')
