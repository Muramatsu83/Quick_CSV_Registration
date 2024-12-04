import os 
import csv
import pyperclip
import keyboard
from playsound import playsound
#効果音は効果音ラボから https://soundeffect-lab.info/sound/button/
import subprocess
import flet as ft
import json

# グローバル変数
hotkey_value = "ctrl + alt + c"
row_id = 0

# 設定ファイルのパス
settings_file = "settings.json"

# 設定の読み込み
def load_settings():
    global hotkey_value
    if os.path.exists(settings_file):
        with open(settings_file, "r", encoding="utf-8") as file:
            settings = json.load(file)
            hotkey_value = settings.get("hotkey", hotkey_value)

# 設定の保存
def save_settings(hotkey_value):
    with open(settings_file, "w", encoding="utf-8") as file:
        json.dump({"hotkey": hotkey_value}, file)

# CSVファイル操作関連
def setup_csv():
    """CSVファイルを初期化"""
    if not os.path.exists("clipboard_data.csv"):
        with open("clipboard_data.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "title", "content"])

def fetch_data():
    """CSVファイルからデータを取得"""
    if not os.path.exists("clipboard_data.csv"):
        return []
    with open("clipboard_data.csv", mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # ヘッダーをスキップ
        rows = [row for row in reader]
    return sorted(rows, key=lambda x: int(x[0]), reverse=True)  # IDの大きい順にソートして取得

def insert_into_csv(title, content):
    """CSVファイルにデータを挿入"""
    rows = fetch_data()
    new_id = max([int(row[0]) for row in rows], default=0) + 1
    with open("clipboard_data.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([new_id, title, content])

def update_csv_row(row_id, title, content):
    """CSVファイルの行を更新"""
    rows = fetch_data()
    with open("clipboard_data.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "title", "content"])
        for row in rows:
            if row[0] == str(row_id):
                writer.writerow([row_id, title, content])
            else:
                writer.writerow(row)

# GUI関連 (Fletを使用するように変更)
def main(page: ft.Page):
    setup_csv()
    load_settings()

    content_A = ""
    content_B = ""

    def display_data():
        """リストビューにデータを表示"""
        data = fetch_data()
        items = []
        latest_id = int(data[0][0]) if data else None
        for row in data:
            items.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(row[0])),
                    ft.DataCell(ft.Text(row[1])),
                    ft.DataCell(ft.Text(row[2]))
                ],
                color=ft.colors.TEAL_900 if int(row[0]) == latest_id else None
            ))
        return items

    def clipboard_to_csv():
        """クリップボードのデータをCSVに追加"""
        nonlocal content_A, content_B

        current_content = pyperclip.paste()
        if current_content:
            content_A = current_content

        if content_B:
            # 二つのコンテンツの文字列長さを比べ、長い方をcontent、短い方をtitleとしてcsvに追加
            contents = [content_A, content_B]
            contents.sort(key=len)
            title, content = contents[0], contents[1]
            insert_into_csv(title, content)
            data_table.rows = display_data()
            status_message.value = "新しいカラムを追加しました。\n"
            playsound("assets\complete_dataset.mp3")
            content_A = ""
            content_B = ""
        else:
            content_B = content_A
            status_message.value = "『" + content_B + "』を記録しました。再度ctrl+Cでコピー、ctrl+alt+cでデータセット登録。\n"
            playsound("assets\got_data.mp3")
            content_A = ""

        page.update()

    def open_directory(e):
        """CSVファイルがあるディレクトリをエクスプローラーで開く"""
        directory = os.path.abspath(os.path.dirname("clipboard_data.csv"))
        subprocess.Popen(f'explorer "{directory}"', shell=True)

    def swap_data_by_id(e):
        """IDを入力して指定された行のtitleとcontentを入れ替える"""
        row_id = id_input.value
        if row_id:
            data = fetch_data()
            for row in data:
                if row[0] == row_id:
                    update_csv_row(row_id, row[2], row[1])  # titleとcontentを入れ替え
                    data_table.rows = display_data()
                    status_message.value = f"ID {row_id} のタイトルとコンテンツを入れ替えました。"
                    page.update()
                    return
            status_message.value = f"ID {row_id} のデータが見つかりませんでした。"
        else:
            status_message.value = "有効なIDを入力してください。"
        page.update()

    def update_hotkey(e):
        """ホットキーを更新"""
        hotkey_value = hotkey_input.value
        if hotkey_value:
            keyboard.remove_all_hotkeys()
            keyboard.add_hotkey(hotkey_value, clipboard_to_csv)
            save_settings(hotkey_value)  # 設定を保存
            status_message.value = f"ホットキーを {hotkey_value} に変更しました。"
        else:
            status_message.value = "有効なホットキーを入力してください。"
        page.update()
        print("ホットキーを登録しsetting.jsonに保存しました: " + hotkey_value)

    # 初期ホットキーの登録
    keyboard.add_hotkey(hotkey_value, clipboard_to_csv)

    # UIコンポーネントの作成
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Title")),
            ft.DataColumn(ft.Text("Content")),
        ],
        rows=display_data(),
        # width=600,
        # height=400,
        # border=ft.border.all(1, ft.colors.GREY)
    )

    # add_button = ft.ElevatedButton("追加", on_click=clipboard_to_csv)
    status_message = ft.Text(value="ctrl+Cでコピー、ctrl+alt+Cでデータセット登録", color=ft.colors.GREEN)
    guide_message = ft.Text(value="エクスプローラーで開くと、csvファイルを複製・名称変更できます", color=ft.colors.WHITE)
    id_input = ft.TextField(label="入れ替えたい行のIDを入力", value=row_id, width=200)
    open_dir_button = ft.ElevatedButton("エクスプローラーで開く", on_click=open_directory)
    swap_button = ft.ElevatedButton("タイトルと内容を入れ替え", on_click=swap_data_by_id)
    hotkey_input = ft.TextField(label="ホットキーを設定 (例: ctrl+alt+c)", value=hotkey_value, width=200)
    update_hotkey_button = ft.ElevatedButton("ホットキー更新", on_click=update_hotkey)

    # レイアウト設定
    page.add(
        ft.Column(
            [
                # add_button,  # 必要に応じてコメントを解除
                open_dir_button,
                status_message,
                guide_message,
                ft.Row(
                    [
                        id_input,
                        swap_button,
                    ],
                ),
                ft.Row(
                    [
                        hotkey_input,
                        update_hotkey_button,
                    ],
                ),
                data_table,
            ]
        )
    )



# Fletアプリの実行
ft.app(target=main)
