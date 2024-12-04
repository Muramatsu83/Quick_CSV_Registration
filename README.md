# Quick_CSV_Registration(クイックCSV登録)

プログラム起動中、ショートカットキー（デフォルト：ctrl + alt + C）を使って、CSVファイルにデータを登録します。  
2つのデータを登録すると、短い方をタイトル、長い方をコンテンツとして自動で判定します。   
Anki等、学習アプリの辞書データを作成するのに役立ちます。  
カラム入れ替え機能、ショートカットキー変更機能を備えています。  
現状、ガイドはWindowsにのみ対応しています。  
このリポジトリは学習成果を発表する目的で公開されています。

## インストール方法(Windows)

このガイドでは、WindowsでVTT File Translatorをインストールし、実行する手順を説明します。

- 準備:  
Pythonのインストール: Python公式サイトからPythonをダウンロードしてインストールします。  
Gitのインストール: Git for Windowsをダウンロードしてインストールします。

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
- ホットキー（デフォルト：ctrl+alt+C）を押して、一つ目のデータを登録します。
- クリップボードに新たな文字列をコピーします。
- 再びホットキーを押して、二つ目のデータを登録します。CSVにデータが追加され、画面に表示されます。

## クレジット
- 効果音：[効果音ラボ](https://soundeffect-lab.info/sound/button/)

## ライセンス
[MIT License](https://opensource.org/license/MIT)の元で提供されます 

# Quick_CSV_Registration

During program execution, data can be registered to a CSV file using a shortcut key combination (defalt: Ctrl + Alt + C).  
When registering two pieces of data, the shorter one is automatically identified as the title, and the longer one as the content.  
This tool is useful for creating dictionary data for learning applications such as Anki.  
It includes features for swapping columns and customizing shortcut keys.
Currently, this guide only supports Windows.  
This repository is made public to share the results of the learning process.

## Installation (Windows)

This guide explains how to install and run the application on Windows.

### Prerequisites:
1. **Install Python**: Download and install Python from the official Python website.  
2. **Install Git**: Download and install Git for Windows.

### Clone the Repository:
```
git clone https://github.com/Muramatsu83/Quick_CSV_Registration.git
cd Quick_CSV_Registration
```

### Install Required Packages:
```
pip install -r requirements.txt
```

### Run the Application:
```
python ./main.py
```

## Usage
- Start the application and copy a string to the clipboard (Ctrl+C). This string can serve as either the title or the content. 
- Press Hotkey (defalt: Ctrl+Alt+C) to register the first piece of data.  
- Copy a new string to the clipboard.  
- Press Ctrl+Alt+C again to register the second piece of data. The data will be added to the CSV file and displayed on the screen.

## Credits
- Sound effects: **Sound Effect Lab**  
  [https://soundeffect-lab.info/sound/button/](https://soundeffect-lab.info/sound/button/)

## License
This app is provided under the terms of the [MIT License](https://opensource.org/license/MIT)
