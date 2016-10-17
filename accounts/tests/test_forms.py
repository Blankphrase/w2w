import unittest
from unittest.mock import Mock, patch

from accounts.forms import DeleteAccountForm
from accounts.models import User


@patch("accounts.models.User.check_password")
class DeleteAccountFormTest(unittest.TestCase):

    def test_for_checking_user_password(self, mock_password):
        user = User(password="test")
        form = DeleteAccountForm(user, {"password": "test"})
        form.is_valid()
        self.assertTrue(mock_password.called)

    def test_check_password_called_with_correct_argument(self, mock_password):
        user = User(password="test")
        form = DeleteAccountForm(user, {"password": "blabla"})
        form.is_valid()   
        mock_password.assert_called_with("blabla")   

    def test_returns_false_for_incorrect_password(self, mock_password):
        mock_password.return_value = False
        user = User(password="test")
        form = DeleteAccountForm(user, {"password": "test2"})
        self.assertFalse(form.is_valid())

    def test_returns_true_for_correct_password(self, mock_password):
        mock_password.return_value = True
        user = User(password="test")
        form = DeleteAccountForm(user, {"password": "test"})
        self.assertTrue(form.is_valid())