# 必要なライブラリのインポート
import pandas as pd
from sqlalchemy import create_engine
import tkinter as tk
from tkinter import filedialog, messagebox

def select_file():
    file_path = filedialog.askopenfilename()
    return file_path

# Tkinterウィンドウの作成
root = tk.Tk()
root.withdraw()  # ウィンドウを表示しない

# ファイル選択ダイアログを表示
data_path = select_file()
print("選択されたファイル:", data_path)

if not data_path:
    messagebox.showinfo("Cancel", "Operation canceled.")
    exit()

# データの読み込みと整形
df = pd.read_csv(data_path)
df.dropna(subset=['title'], inplace=True)
df['area_id'] = df['area_id'].astype(str)
df['page'] = df['page'].astype(int)
df['page_number'] = df['page_number'].astype(int)
df['advertising'] = df['advertising'].astype(str)
df['area_id'] = df['area_id'].str.replace('.0', '', regex=False)
df['file_name'] = df['file_name'].str.replace('.txt', '.pdf', regex=False)
df.replace("nan", pd.NA, inplace=True)
# "page"を0埋めした2桁，"page_number"を0埋めした3桁の文字列に変換
df['page'] = df['page'].apply(lambda x: str(x).zfill(2))
df['page_number'] = df['page_number'].apply(lambda x: str(x).zfill(3))

# ローカルホストのデータベースの更新 ----------------------------------------------

# データベースの接続情報
db_connection_str = 'mysql+mysqlconnector://root:@localhost:3306/pbl2'
db_connection = create_engine(db_connection_str)

# タグ（ジャンル管理用のテーブル）
table_name = 'article'
df.to_sql(table_name, con=db_connection, index=False, if_exists='replace')
print(f"Table '{table_name}' created in the database.")

# データベースにジャンル識別用のテーブルを作成--------------------------------------
article_tags = pd.DataFrame(columns=['article_id', 'tag_id'])

# 各レコードの tags 列を処理
for index, row in df.iterrows():
    article_id = row['id']
    tags = row['tags']
    if pd.notna(tags):
        tag_list = tags.split(',')
        for tag in tag_list:
            article_tags = pd.concat([article_tags, pd.DataFrame({'article_id': [article_id], 'tag_id': [str(tag)]})], ignore_index=True)

# article_tagsにid列を追加
article_tags['id'] = article_tags.index + 1
# "id"が一番左になるようにカラムの並び替え
article_tags = article_tags[['id', 'article_id', 'tag_id']]

# データベースにタグのテーブルを作成
table_name = 'article_tags'
article_tags.to_sql(table_name, con=db_connection, index=False, if_exists='replace')
print(f"Table '{table_name}' created in the database.")

# 記事へのアクセス数のテーブルを更新----------------------------------------------
tmp = pd.DataFrame(columns=['id', 'count'])
tmp['id'] = df['id']
tmp['count'] = 0

# データベース接続情報
db_connection_str = 'mysql+mysqlconnector://root:@localhost:3306/pbl2'
db_connection = create_engine(db_connection_str)

# テーブル名
table_name = 'access_log'

# データベースからテーブルの内容を取得してデータフレームに格納
query = f"SELECT * FROM {table_name}"
df_tmp = pd.read_sql(query, con=db_connection)

# tmp にしか存在しない id を抽出する
tmp_unique_ids = tmp[~tmp['id'].isin(df_tmp['id'])]
# df に tmp にしか存在しない id を追加する
df_tmp = pd.concat([df_tmp, tmp_unique_ids], ignore_index=True)

# データベースのテーブルを更新
df_tmp.to_sql(table_name, con=db_connection, index=False, if_exists='replace')

print(f"Table '{table_name}' created in the database.")

# 完了時にポップアップで知らせる
messagebox.showinfo("Completed", "Process completed successfully.")