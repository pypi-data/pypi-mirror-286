import unittest
from unittest.mock import patch, mock_open, MagicMock
from notifier.line_notifier.notifier import Notifier, load_tokens, load_settings, send_line_notify

class TestNotifier(unittest.TestCase):

    @patch('src.line_notifier.src.open', new_callable=mock_open, read_data='user1:token1\nuser2:token2\n')
    def test_load_tokens(self, mock_file):
        tokens = load_tokens('fake_path/tokens.txt')
        expected_tokens = {'user1': 'token1', 'user2': 'token2'}
        self.assertEqual(tokens, expected_tokens)

    @patch('src.line_notifier.src.os.path.exists', return_value=True)
    @patch('src.line_notifier.src.open', new_callable=mock_open, read_data='user1:on\n')
    def test_load_settings(self, mock_exists, mock_file):
        user, notify_on = load_settings('fake_path/notification_setting.txt')
        self.assertEqual(user, 'user1')
        self.assertTrue(notify_on)

    @patch('src.line_notifier.src.requests.post')
    def test_send_line_notify(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        status_code = send_line_notify('Test message', 'fake_token')
        self.assertEqual(status_code, 200)

    @patch('src.line_notifier.src.load_tokens', return_value={'user1': 'fake_token'})
    @patch('src.line_notifier.src.load_settings', return_value=('user1', True))
    @patch('src.line_notifier.src.send_line_notify', return_value=200)
    def test_run_notifier_success(self, mock_send, mock_load_settings, mock_load_tokens):
        notifier = Notifier()
        success = notifier.run_notifier('Test Machine', 'Test message')
        self.assertTrue(success)

    @patch('src.line_notifier.src.load_tokens', return_value={'user1': 'fake_token'})
    @patch('src.line_notifier.src.load_settings', return_value=('user1', False))
    def test_run_notifier_notify_off(self, mock_load_settings, mock_load_tokens):
        notifier = Notifier()
        success = notifier.run_notifier('Test Machine', 'Test message')
        self.assertFalse(success)

if __name__ == '__main__':
    unittest.main()
