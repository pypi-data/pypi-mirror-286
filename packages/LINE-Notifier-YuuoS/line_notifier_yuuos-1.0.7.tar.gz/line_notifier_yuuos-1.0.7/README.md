# Notifier

Notifierは、UI通知を管理するためのPythonパッケージです。

## インストール

まず、必要な依存関係をインストールします。

```bash
pip install -r requirements.txt
```

次に、`setup.py`を使用してパッケージをインストールします。

```bash
pip install .
```

## 使い方

### Notifierクラス

`notifier.py`ファイルには、通知機能を実行するための`Notifier`クラスが含まれています。以下は使用例です。

```python
from notifier.line_notifier import Notifier

notifier = Notifier()
success = notifier.run_notifier("Laser Machine", "加工が終わったよ")

if success:
    print("通知が送信されました")
else:
    print("通知の送信に失敗しました")
```

### Appクラス

`ui_manager.pyw`ファイルには、通知設定を管理するための`App`クラスが含まれています。以下は使用例です。

```python
import tkinter as tk
from notifier.line_notifier.ui_manager import App

root = tk.Tk()
app = App(root)
root.mainloop()
```

## テスト

テストは`unittest`を使用して実行します。以下のコマンドでテストを実行できます。

```bash
python -m unittest discover -s src/test
```

## ファイル構成

```
notifier/
├── notifier/
│   ├── __init__.py
│   ├── line_notifier/
│   │   ├── __init__.py
│   │   ├── notification_setting.txt
│   │   ├── notifier.py
│   │   ├── tokens.txt
│   │   ├── ui_manager.pyw
├── test/
│   ├── __init__.py
│   ├── test_ui_manager.py
├── setup.py
├── requirements.txt
└── README.md
```

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。
