## JB7015_PBL2(新聞紙面を構成する「記事以外の要素」のデータベース作成)
<p style="text-align:right;">(2024/02/11時点)</p>

### 概要
- 上毛新聞の2023年10月の記事をキーワード，ジャンル等の条件を付けて検索できる.

### 環境
<img src="https://img.shields.io/badge/-XAMPP-FB7A24.svg?logo=xampp&style=flat">
- XAMPPを<a href="https://www.apachefriends.org/jp/index.html">こちら</a>からダウンロード・インストールすること.
- ディレクトリ"xampp"直下の"htdocs"を本プロジェクトの"htdocs"に置き換えること.

### 使用言語
<img src="https://img.shields.io/badge/-HTML5-333.svg?logo=html5&style=flat">
<img src="https://img.shields.io/badge/-CSS3-1572B6.svg?logo=css3&style=flat">
<img src="https://img.shields.io/badge/-JavaScript-276DC3.svg?logo=javascript&style=flat">
<img src="https://img.shields.io/badge/-PHP-777BB4.svg?logo=PHP&style=flat">
<img src="https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat">

### 使用方法１
1. `JomoApp`を起動.
2. `データベース起動`をクリック.
3. 画面左の検索フォーム上で検索キーワードの入力やジャンルのフィルタリングを行う.


### 使用方法２
1. XAMPP Control Panelを起動.(`Apache`, `MySQL`をスタート)
2. localhost/pbl2/index.htmlにアクセス.
3. 画面左の検索フォーム上で検索キーワードの入力やジャンルのフィルタリングを行う.

### データベース更新手順
1. スプレッドシート`template`を.csv形式でダウンロード.
2. `JomoApp`を起動して'データベースの更新'をクリック.
3. ダイアログが起動するので，1でダウンロードした'template.csv'を選択して'開く'をクリック.

### スキャンデータのディレクトリ構造が'PBL2/YYYYMMDD'形式の場合
1. Google Driveからスキャンデータが格納されている'PBL2'をダウンロード.
2. '~/downloads/'に圧縮された'PBL2'を展開(圧縮された'PBL2'はダウンロード時に識別子のようなものが付いているが気にしない).
3. 'JomoApp'を起動して'ディレクトリの改名・移動'をクリック.
4. ダイアログが起動するので，2で展開した'PBL2'を選択して'フォルダの選択'をクリック.

### 現状・展望
- 入力されたキーワードを記事の見出しもしくは本文に含む記事を返す.
- 本PBLの題目にある"記事以外の要素"のデータベース作成には至っていない.
    - 記事全体をアーカイブしているため，今後，必要な情報のエンジニアリングが期待される.
    - 本題目では具体的なユーザが想定されていない. 
    - ユーザの特定と，需要を踏まえた上で機能を付与する必要がある.
- 記事のジャンルについてはデータベースの全てに付与されていない.
- SQLインジェクションなどの対策がされていない.
    - 顔写真のような機微な情報も格納されているものの，現時点で悪意を持ったユーザの利用は想定していない. 一般向けに公開するのであれば対策を講じる必要がある.
- テキストや画像の抽出は人間の手によって行われており，スキャン作業に時間を要する原因となっている. (OCRの精度が想定よりも低かった)
    - スキャンデータから記事の見出しや本文，画像を切り出す作業を画像処理技術等を通じて行えるようにすることが期待される.
- UIの改善.

#### 問い合わせ
- j251a028@gunma-u.ac.jp</br>