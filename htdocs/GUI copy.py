import tkinter as tk
import threading
import os
import webbrowser

class ScriptExecutorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jomo Database Manager")

        # 実行するファイルとそのラベルを定義
        self.script_mapping = {
            "C:/xampp/htdocs/processingTable.py": "データベースの更新",
            "C:/xampp/htdocs/renameDir.py": "ディレクトリの改名・移動"
        }

        # フレームを作成
        frame = tk.Frame(root)
        frame.pack(pady=10)

        # "Select File"のテキストラベルをフレーム内に配置
        select_label = tk.Label(frame, text="Select file and click [execute].\nOr click [Open Database].", font="Meiryo 12 bold", fg="black")
        select_label.pack()

        # 実行ファイルの候補リストを表示するリストボックス
        self.file_listbox = tk.Listbox(root, width=50, height=20)
        self.file_listbox.pack(pady=10)

        # ファイルリストの更新ボタン
        refresh_button = tk.Button(root, text="Refresh List", command=self.refresh_list, bg="white", fg="black")
        refresh_button.pack()

        # 実行ボタン
        execute_button = tk.Button(root, text="Execute", command=self.execute_selected_script, bg="white", fg="black")
        execute_button.pack(pady=10)

        # HTMLを開くボタン
        open_html_button = tk.Button(root, text="Open Database", command=self.open_html, bg="white", fg="black")
        open_html_button.pack(pady=10)

        self.refresh_list()

    def refresh_list(self):
        self.file_listbox.delete(0, tk.END)  # リストボックスをクリア

        # 実行ファイルの候補をリストボックスに追加
        for filename, label in self.script_mapping.items():
            self.file_listbox.insert(tk.END, f"{label}: {filename}")

    def execute_selected_script(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_item = self.file_listbox.get(selected_index[0])
            selected_filename = selected_item.split(": ")[1]  # ファイル名を取得
            os.system(f"python {selected_filename}")  # 選択されたスクリプトを実行

    def open_html(self):
        # ブラウザを非同期で開く
        threading.Thread(target=self.open_browser).start()

    def open_browser(self):
        # HTMLファイルをデフォルトのブラウザで開く
        html_path = "http://localhost/pbl2/index.html"
        webbrowser.open(html_path)

root = tk.Tk()
app = ScriptExecutorApp(root)
root.mainloop()

sub = """
import tkinter as tk
import os

class ScriptExecutorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jomo Database Manager")

        # 実行するスクリプトとそのラベルを定義
        self.script_mapping = {
            "データベース更新": "C:/xampp/htdocs/processingTable.py",
            "ディレクトリの改名・移動": "C:/xampp/htdocs/renameDir.py",
            "データベース起動": "http://localhost/pbl2/index.html"
        }

        # フレームを作成
        frame = tk.Frame(root)
        frame.pack(pady=10)

        # ボタンを配置
        for label_text, filename in self.script_mapping.items():
            button = tk.Button(frame, text=label_text, font="游ゴシック 12 bold", fg="black", command=lambda script=filename: self.execute_script(script) if script.startswith("http") else self.execute_python_script(script))
            button.pack(pady=5)

        # ウィンドウが閉じられたときの処理を設定
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def execute_python_script(self, filename):
        # ラベルに関連付けられたスクリプトを実行
        os.system(f"python {filename}")

    def execute_script(self, script):
        # ブラウザで開く
        os.system(f"start {script}")

    def on_closing(self):
        # ウィンドウが閉じられるときに呼び出される関数
        self.stop_services()
        self.root.destroy()

    def stop_services(self):
        # ApacheとMySQLを停止するバッチファイルを実行
        os.system("apache_stop.bat")
        os.system("mysql_stop.bat")
        
        # XAMPPのコントロールパネルを閉じる
        os.system("taskkill /f /im xampp-control.exe")

root = tk.Tk()
app = ScriptExecutorApp(root)
root.mainloop()
"""