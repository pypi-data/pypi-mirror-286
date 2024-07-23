import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog, Menu

import pyperclip


# トークン情報を読み込む関数
def load_tokens(filepath):
    tokens = {}
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                name, token = line.strip().split(':')
                tokens[name] = token  # トークンをキーとして保存
    return tokens


# トークン情報を保存する関数
def save_token(filepath, name, token):
    if os.path.exists(filepath):
        with open(filepath, 'r+', encoding='utf-8') as file:
            lines = file.readlines()
            if lines and lines[-1].strip():
                file.write('\n')
            file.write(f"{name}:{token}\n")
    else:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(f"{name}:{token}\n")


# 設定を保存する関数
def save_settings(filepath, user, notify_on):
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(f"{user}:{'on' if notify_on else 'off'}\n")


# 設定を読み込む関数
def load_settings(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            line = file.readline().strip()
            user, notify_on = line.split(':')
            return user, notify_on == 'on'
    return None, False


# メインアプリケーションクラス
class App:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-topmost', True)
        self.root.title("通知設定マネージャー")
        self.root.configure(bg='#000000')  # 背景色を黒に設定

        self.tokens_file = r'tokens.txt'
        self.settings_file = r'notification_setting.txt'
        self.tokens = load_tokens(self.tokens_file)
        self.current_user, self.notify_on = load_settings(self.settings_file)

        # スタイル設定
        self.style = ttk.Style()
        self.style.configure("Custom.TCombobox",
                             fieldbackground='#000000',
                             background='#000000',
                             foreground='#00FFFF',
                             selectbackground='#000000',
                             selectforeground='#00FFFF',
                             arrowsize=20,
                             bordercolor='#00FFFF')
        self.style.map("Custom.TCombobox",
                       fieldbackground=[("readonly", "#000000")],
                       selectbackground=[("readonly", "#000000")],
                       selectforeground=[("readonly", "#00FFFF")],
                       background=[("readonly", "#000000")],
                       foreground=[("readonly", "#00FFFF")],
                       arrowcolor=[("readonly", "#00FFFF")],
                       bordercolor=[("readonly", "#00FFFF")])

        # メインウィンドウのグリッド設定
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # メニューバーの作成
        menubar = tk.Menu(self.root, background='#000000', foreground='#00FFFF', activebackground='#00FFFF',
                          activeforeground='#000000', font=("Yu Gothic", 12))
        self.root.config(menu=menubar)
        user_menu = tk.Menu(menubar, tearoff=0, background='#000000', foreground='#00FFFF', activebackground='#00FFFF',
                            activeforeground='#000000', font=("Yu Gothic", 12))
        menubar.add_cascade(label="ユーザー管理", menu=user_menu)
        user_menu.add_command(label="ユーザー管理画面を開く", command=self.open_user_management)

        # ユーザー名と通知モードの大きな表示
        display_frame = tk.Frame(self.root, bg='#000000')
        display_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.user_display = tk.Label(display_frame, text="", font=("Yu Gothic", 30), fg='#00FFFF', bg='#000000')
        self.user_display.pack()

        self.notify_display = tk.Label(display_frame, text="", font=("Yu Gothic", 30), fg='#00FFFF', bg='#000000')
        self.notify_display.pack()

        # ユーザー指定フレーム
        left_frame = tk.LabelFrame(self.root, text="ユーザー指定", bg='#000000', fg='#00FFFF', font=("Yu Gothic", 12))
        left_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # ユーザー選択用コンボボックス
        self.user_var = tk.StringVar(value=self.current_user)
        self.user_combobox = ttk.Combobox(left_frame, textvariable=self.user_var, values=list(self.tokens.keys()),
                                          state="readonly")
        self.user_combobox.pack(pady=10)

        self.user_combobox.configure(style="Custom.TCombobox")

        if self.tokens and self.current_user in self.tokens:
            index = list(self.tokens.keys()).index(self.current_user)
            self.user_combobox.current(index)

        self.user_combobox.bind("<<ComboboxSelected>>", self.update_settings)

        # 通知モードフレーム
        right_frame = tk.LabelFrame(self.root, text="通知モード", bg='#000000', fg='#00FFFF', font=("Yu Gothic", 12))
        right_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        self.notify_var = tk.BooleanVar(value=self.notify_on)
        self.notify_checkbox = tk.Checkbutton(right_frame, text="通知をオンにする", variable=self.notify_var,
                                              command=self.update_settings, bg='#000000', fg='#00FFFF',
                                              font=("Yu Gothic", 12), selectcolor='#000000')
        self.notify_checkbox.pack(pady=10)

        self.user_management_window = None  # 管理画面のウィンドウを追跡するための変数

        # 起動時に設定を反映
        self.update_display()

    def open_user_management(self):
        if self.user_management_window and self.user_management_window.winfo_exists():
            self.user_management_window.deiconify()  # 最小化されている場合にウィンドウを復元
            self.user_management_window.lift()
            self.user_management_window.attributes('-topmost', True)
            self.user_management_window.attributes('-topmost', False)
            return

        self.user_management_window = tk.Toplevel(self.root)
        self.user_management_window.title("ユーザー管理")
        self.user_management_window.configure(bg='#000000')

        # ボタンフレームを作成して左寄せ
        button_frame = tk.Frame(self.user_management_window, bg='#000000')
        button_frame.pack(anchor="w", padx=10, pady=5)

        # ユーザー追加ボタン
        add_button = tk.Button(button_frame, text="ユーザー追加", command=self.add_user, bg='#000000', fg='#00FFFF',
                               font=("Yu Gothic", 12), highlightbackground='#00FFFF', highlightthickness=2)
        add_button.pack(side=tk.LEFT, padx=5)

        # ファイルから追加ボタン
        add_from_file_button = tk.Button(button_frame, text="ファイルから追加", command=self.add_user_from_file,
                                         bg='#000000', fg='#00FFFF', font=("Yu Gothic", 12),
                                         highlightbackground='#00FFFF', highlightthickness=2)
        add_from_file_button.pack(side=tk.LEFT, padx=5)

        # ユーザーリスト表示
        columns = ("name", "token")
        self.user_tree = ttk.Treeview(self.user_management_window, columns=columns, show="headings",
                                      style="Custom.Treeview")
        self.user_tree.heading("name", text="ユーザー名", anchor="center")
        self.user_tree.heading("token", text="アクセストークン", anchor="center")

        # 列の幅を設定
        self.user_tree.column("name", width=150, anchor="center")
        self.user_tree.column("token", width=300, anchor="center")

        self.user_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # スクロールバー
        tree_scroll = ttk.Scrollbar(self.user_management_window, orient="vertical", command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.style.configure("Custom.Treeview", background="#000000", foreground="#00FFFF", fieldbackground="#000000",
                             font=("Yu Gothic", 12), rowheight=25)
        self.style.map("Custom.Treeview", background=[("selected", "#00FFFF")], foreground=[("selected", "#000000")])
        self.style.configure("Vertical.TScrollbar", background="#000000", foreground="#00FFFF", arrowcolor="#00FFFF")

        for name, token in self.tokens.items():
            self.user_tree.insert("", "end", iid=token, values=(name, token))

        self.user_tree.bind('<Double-1>', self.edit_user)
        self.user_tree.bind('<Button-3>', self.show_context_menu)

        # 削除ボタン
        delete_button = tk.Button(self.user_management_window, text="選択したユーザーを削除", command=self.delete_user,
                                  bg='#000000', fg='#00FFFF', font=("Yu Gothic", 12), highlightbackground='#00FFFF',
                                  highlightthickness=2)
        delete_button.pack(pady=5)

        # コンテキストメニュー
        self.context_menu = Menu(self.user_tree, tearoff=0)
        self.context_menu.add_command(label="トークンをクリップボードにコピー", command=self.copy_token_to_clipboard)
        self.context_menu.add_command(label="ユーザー名を変更", command=self.edit_user_from_context)

    def show_context_menu(self, event):
        item = self.user_tree.identify_row(event.y)
        if item:
            self.user_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def copy_token_to_clipboard(self):
        selected_item = self.user_tree.selection()[0]
        token = selected_item
        pyperclip.copy(token)

    def edit_user_from_context(self):
        self.edit_user(None)

    def add_user(self):
        popup = tk.Toplevel(self.root)
        popup.title("ユーザーの追加")
        popup.configure(bg='#000000')

        tk.Label(popup, text="ユーザー名:", bg='#000000', fg='#00FFFF', font=("Yu Gothic", 12)).grid(row=0, column=0,
                                                                                                     padx=10, pady=5)
        name_entry = tk.Entry(popup, bg='#000000', fg='#00FFFF', insertbackground='#00FFFF', font=("Yu Gothic", 12))
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(popup, text="アクセストークン:", bg='#000000', fg='#00FFFF', font=("Yu Gothic", 12)).grid(row=1,
                                                                                                           column=0,
                                                                                                           padx=10,
                                                                                                           pady=5)
        token_entry = tk.Entry(popup, bg='#000000', fg='#00FFFF', insertbackground='#00FFFF', font=("Yu Gothic", 12))
        token_entry.grid(row=1, column=1, padx=10, pady=5)

        def save_user():
            name = name_entry.get()
            token = token_entry.get()
            if not name or not token:
                messagebox.showerror("エラー", "ユーザー名とアクセストークンを入力してください。")
                return
            if token in self.tokens:
                messagebox.showerror("エラー", "このアクセストークンは既に存在します。")
                return
            self.tokens[token] = name
            save_token(self.tokens_file, name, token)
            self.user_combobox['values'] = list(self.tokens.keys())
            self.user_combobox.set(name)
            self.user_tree.insert("", "end", iid=token, values=(name, token))
            self.update_settings()
            popup.destroy()

        tk.Button(popup, text="保存", command=save_user, bg='#000000', fg='#00FFFF', font=("Yu Gothic", 12),
                  highlightbackground='#00FFFF', highlightthickness=2).grid(row=2, column=0, columnspan=2, pady=10)

    def add_user_from_file(self):
        filepath = filedialog.askopenfilename(title="ファイルから追加", filetypes=[("Text Files", "*.txt")])
        if filepath:
            new_tokens = load_tokens(filepath)
            added_count = 0
            for token, name in new_tokens.items():
                if token not in self.tokens:
                    self.tokens[token] = name
                    save_token(self.tokens_file, name, token)
                    self.user_combobox['values'] = list(self.tokens.keys())
                    self.user_tree.insert("", "end", iid=token, values=(name, token))
                    added_count += 1
            messagebox.showinfo("成功", f"{added_count} ユーザーが追加されました。")
            self.update_settings()

    def delete_user(self):
        selected_item = self.user_tree.selection()
        if selected_item:
            token = selected_item[0]
            if messagebox.askyesno("確認", f"{self.tokens[token]} を削除しますか？"):
                del self.tokens[token]
                self.user_tree.delete(selected_item)
                self.user_combobox['values'] = list(self.tokens.keys())
                self.user_combobox.set('')
                self.update_tokens_file()
                self.update_settings()

    def update_tokens_file(self):
        with open(self.tokens_file, 'w', encoding='utf-8') as file:
            for token, name in self.tokens.items():
                file.write(f"{name}:{token}\n")

    def update_settings(self, event=None):
        selected_user = self.user_var.get()
        notify_on = self.notify_var.get()
        if selected_user:
            save_settings(self.settings_file, selected_user, notify_on)
            self.current_user = selected_user
            self.notify_on = notify_on
            self.update_display()
            print(f"設定が更新されました - ユーザー: {selected_user}, 通知モード: {'on' if notify_on else 'off'}")
        else:
            messagebox.showerror("エラー", "ユーザーが選択されていません。")

    def update_display(self):
        self.user_display.config(text=f"ユーザー: {self.current_user}")
        self.notify_display.config(text=f"通知モード: {'ON' if self.notify_on else 'OFF'}")

    def edit_user(self, event):
        item = self.user_tree.selection()[0]
        old_name = self.user_tree.item(item, "values")[0]
        token = item
        new_name = simpledialog.askstring("ユーザー名の編集", "新しいユーザー名を入力してください:",
                                          initialvalue=old_name)
        if new_name:
            self.tokens[token] = new_name
            self.user_tree.item(item, values=(new_name, token))
            self.user_combobox['values'] = list(self.tokens.keys())
            self.update_tokens_file()
            self.update_settings()


def run():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    run()
