import unittest
from notifier.line_notifier.ui_manager import App
import tkinter as tk

class TestUIManager(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = App(self.root)

    def test_initialization(self):
        self.assertIsInstance(self.app, App)
        self.assertEqual(self.app.root.title(), "通知設定マネージャー")

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
