import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def rename_and_move_directories(root_directory):
    for dir_name in os.listdir(root_directory):
        if len(dir_name) == 8 and dir_name.isdigit():
            year = dir_name[:4]
            month = dir_name[4:6]
            day = dir_name[6:8]

            new_year_dir = os.path.join(root_directory, year)
            new_month_dir = os.path.join(new_year_dir, month)
            new_day_dir = os.path.join(new_month_dir, day)

            for new_dir in [new_year_dir, new_month_dir, new_day_dir]:
                if not os.path.exists(new_dir):
                    os.makedirs(new_dir)

            old_dir_path = os.path.join(root_directory, dir_name)
            new_dir_path = os.path.join(new_day_dir, dir_name)
            os.rename(old_dir_path, new_dir_path)

            for subdir_name in os.listdir(new_dir_path):
                subdir_path = os.path.join(new_dir_path, subdir_name)
                if os.path.isdir(subdir_path):
                    new_subdir_name = subdir_name.split("_")[-1]
                    new_subdir_path = os.path.join(new_dir_path, new_subdir_name)
                    os.rename(subdir_path, new_subdir_path)

                    for subsubdir_name in os.listdir(new_subdir_path):
                        subsubdir_path = os.path.join(new_subdir_path, subsubdir_name)
                        if os.path.isdir(subsubdir_path):
                            new_subsubdir_name = subsubdir_name.split("_")[-1]
                            new_subsubdir_path = os.path.join(new_subdir_path, new_subsubdir_name)
                            os.rename(subsubdir_path, new_subsubdir_path)

            for item_name in os.listdir(new_dir_path):
                item_path = os.path.join(new_dir_path, item_name)
                if os.path.isdir(item_path):
                    new_item_path = os.path.join(new_day_dir, item_name)
                    os.rename(item_path, new_item_path)
                else:
                    shutil.move(item_path, new_day_dir)

            os.rmdir(new_dir_path)
            
    if root_directory != None:
        messagebox.showinfo("Success", "Directories renamed and moved successfully!")

    return root_directory

def select_and_process_directory():
    root = tk.Tk()
    root.withdraw()
    root_directory = filedialog.askdirectory(title="Select Directory")
    root.destroy()

    if not root_directory:
        messagebox.showinfo("Cancel", "Operation canceled.")
        return
    
    return root_directory

# ここで関数を呼び出す
root_directory = rename_and_move_directories(select_and_process_directory())

# ディレクトリのリネームと移動
new_root_directory = os.path.join(os.path.dirname(root_directory), "jomo")
os.rename(root_directory, new_root_directory)

specified_directory = "C:/xampp/htdocs/pbl2/"
jomo_directory = os.path.join(specified_directory, "jomo")
if os.path.exists(jomo_directory):
    shutil.rmtree(jomo_directory)
shutil.move(new_root_directory, specified_directory)