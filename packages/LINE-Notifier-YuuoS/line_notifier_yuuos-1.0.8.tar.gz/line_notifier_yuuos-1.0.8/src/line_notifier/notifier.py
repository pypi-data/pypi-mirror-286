import os
import random
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

import requests


# トークン情報を読み込む関数
def load_tokens(filepath):
    """トークン情報をファイルから読み込む関数。

    Args:
        filepath (str): トークン情報が記載されたファイルのパス。

    Returns:
        dict: トークン名をキー、トークン値を値とする辞書。
    """
    tokens = {}
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            name, token = line.strip().split(':')
            tokens[name] = token
    return tokens


# 設定を読み込む関数
def load_settings(filepath):
    """設定をファイルから読み込む関数。

    Args:
        filepath (str): 設定が記載されたファイルのパス。

    Returns:
        tuple: ユーザー名と通知オン/オフのブール値。
    """
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            line = file.readline().strip()
            user, notify_on = line.split(':')
            return user, notify_on == 'on'
    return None, False


# LINE Notify APIを使用してメッセージを送信する関数
def send_line_notify(message, token, sticker_package_id=None, sticker_id=None):
    """LINE Notify APIを使用してメッセージを送信する関数。

    Args:
        message (str): 送信するメッセージ。
        token (str): LINE Notifyのアクセストークン。
        sticker_package_id (str, optional): スタンプパッケージID。
        sticker_id (str, optional): スタンプID。

    Returns:
        int: HTTPレスポンスのステータスコード。
    """
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    data = {
        'message': message
    }
    if sticker_package_id and sticker_id:
        data['stickerPackageId'] = sticker_package_id
        data['stickerId'] = sticker_id

    response = requests.post(line_notify_api, headers=headers, data=data)
    return response.status_code


# 通知機能を実行するクラス
class Notifier:
    def __init__(self):
        self.user_response = None
        self.no_response_flg = None
        self.tokens_file = os.path.join(os.path.dirname(__file__), 'tokens.txt')
        self.settings_file = os.path.join(os.path.dirname(__file__), 'notification_setting.txt')
        self.tokens = load_tokens(self.tokens_file)
        self.user, self.notify_on = load_settings(self.settings_file)
        self.debug_settings()
        self.initialize_notifier()

    def debug_settings(self):
        """設定内容とトークンをデバッグ出力する関数。"""
        print(f"読み込まれた設定: ユーザー: {self.user}, 通知オン: {self.notify_on}")
        print(f"ユーザーのトークン: {self.tokens.get(self.user, 'トークンが見つかりません')}")

    def initialize_notifier(self):
        root = tk.Tk()
        root.withdraw()  # メインウィンドウを隠す

        if not self.user or self.user not in self.tokens:
            messagebox.showerror("エラー", "ユーザーが設定されていないか、無効です。")
            return

        # 応答を格納する変数
        self.user_response = None
        self.no_response_flg = False

        def on_timeout():
            self.no_response_flg = True
            root.quit()  # メインループを停止
            root.destroy()

        def ask_notify():
            self.user_response = messagebox.askyesno("通知設定", f"ユーザー: {self.user}\n通知を送信しますか？")
            root.quit()  # ユーザーが応答した場合もメインループを停止

        root.after(1000, on_timeout)  # 10秒後にタイムアウト
        root.after(0, ask_notify)  # 直ちにポップアップを表示

        root.mainloop()  # メインループ開始

        # レスポンスなし
        if self.no_response_flg:
            pass
        # レスポンスあり
        else:
            if self.user_response:
                self.notify_on = True
            else:
                self.notify_on = False

        with open(self.settings_file, 'w', encoding='utf-8') as file:
            file.write(f"{self.user}:{'on' if self.notify_on else 'off'}\n")

    def run_notifier(self, machine, message):
        """通知機能を実行するメイン関数。

        Args:
            machine (str): レーザー加工機の名前。
            message (str): 送信するメッセージ。

        Returns:
            bool: 送信が成功した場合はTrue、そうでない場合はFalse
        """
        self.tokens = load_tokens(self.tokens_file)
        self.user, self.notify_on = load_settings(self.settings_file)

        if not self.notify_on:
            print("通知はオフになっています。")
            return False

        selected_token = self.tokens.get(self.user)
        if not selected_token:
            print(f"ユーザー {self.user} のトークンが見つかりません。")
            return False

        sticker_package_id = 446
        sticker_id_list = range(1988, 2028)
        sticker_id = random.choice(sticker_id_list)

        if not machine:
            machine = 'Laser Machine'
        if not message:
            message = '加工が終わったよ'
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        full_message = f"\n【{machine}】からの通知\n時刻: {timestamp}\n\n{message}"

        status = send_line_notify(full_message, selected_token, sticker_package_id, sticker_id)

        if status == 200:
            print('通知が送信されました')
            return True
        else:
            print('通知の送信に失敗しました')
            return False
