import tkinter as tk
import subprocess
import os

class ScriptExecutorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jomo App")

        # 実行するスクリプトとそのラベルを定義
        self.script_mapping = {
            "データベース更新": "C:/xampp/htdocs/processingTable.py",
            "ディレクトリの改名・移動": "C:/xampp/htdocs/renameDir.py",
            "データベース起動": "http://localhost/pbl2/index.html",
            "README": "C:/xampp/htdocs/pbl2/README.md"
        }

        # フレームを作成
        frame = tk.Frame(root, bg="white")
        frame.pack(expand=True, fill="both")

        # ボタンを配置
        for label_text, filename in self.script_mapping.items():
            # ボタンの幅を調整
            button_width = max(len(label_text), 20)  # ボタンの幅をラベルの長さに合わせる
            button = tk.Button(frame, text=label_text, width=button_width, font="游ゴシック 12 bold", fg="#40A2D8", bg="white", 
                               cursor="hand2",
                               command=lambda script=filename: self.execute_script(script))
            button.pack(pady=10)

        # ウィンドウが閉じられたときの処理を設定
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def execute_script(self, script):
    # README.mdファイルのパスが指定されているかチェック
        if os.path.isfile(script):
            # ローカルファイルをブラウザで開く
            os.startfile(script)
        elif script.startswith("http"):
            # スクリプトがURLの場合、ブラウザで開く
            os.system(f"start {script}")
        elif script.endswith(".py"):
            # Pythonスクリプトの場合、Pythonインタープリターで実行
            subprocess.Popen(["python", script])
        else:
            # それ以外の場合は通常のスクリプトとして処理
            subprocess.Popen(["start", script])

    def on_closing(self):
        # ウィンドウが閉じられるときに呼び出される関数
        self.stop_services()
        self.root.destroy()

    def stop_services(self):
        # ApacheとMySQLを停止するバッチファイルを実行
        subprocess.run(["C:/xampp/apache_stop.bat"])
        subprocess.run(["C:/xampp/mysql_stop.bat"])
        
        # XAMPPのコントロールパネルを閉じる
        subprocess.run(["taskkill", "/f", "/im", "xampp-control.exe"])

root = tk.Tk()
root.configure(bg="white")
root.geometry("400x300") 
app = ScriptExecutorApp(root)
root.mainloop()