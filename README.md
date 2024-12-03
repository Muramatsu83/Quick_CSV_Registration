
# Quick_CSV_Registration

プログラム起動中、ショートカットキー（ctrl + alt + C）を使って、CSVファイルにデータを登録します。
2つのデータを登録すると、短い方をタイトル、長い方をコンテンツとして自動で判定します。  
現状、ガイドはWindowsにのみ対応しています。  
このリポジトリは学習成果を発表する目的で公開されています。

## インストール方法(Windows)

このガイドでは、WindowsでVTT File Translatorをインストールし、実行する手順を説明します。

- 準備:
Pythonのインストール: Python公式サイトからPythonをダウンロードしてインストールします
Gitのインストール: Git for Windowsをダウンロードしてインストールします.

- リポジトリをクローンします：
```
git clone https://github.com/Muramatsu83/Quick_CSV_Registration.git
cd Quick_CSV_Registration
```
- 必要なパッケージをインストールします：
```
pip install -r requirements.txt
```
- アプリケーションを実行します：
```
python ./main.py
```

## 使用方法
- アプリケーションを起動した状態で、クリップボードに文字列をコピーします（ctrl+C）。タイトルでも内容でもどちらでも構いません。
- ctrl+alt+Cを押して、一つ目のデータを登録します。
- クリップボードに新たな文字列をコピーします（ctrl+C）
- 再びctrl+alt+Cを押して、二つ目のデータを登録します。CSVにデータが追加され、画面に表示されます
