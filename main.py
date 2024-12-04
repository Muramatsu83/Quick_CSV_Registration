import os 
import csv
import pyperclip
import keyboard
from playsound import playsound
#効果音は効果音ラボから https://soundeffect-lab.info/sound/button/
import subprocess

import flet as ft

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
    return rows[::-1]  # データを逆順で取得

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

    def swap_data(e):
        """選択中の行のtitleとcontentを入れ替える"""
        if data_table.selected_row_indices:
            selected_index = data_table.selected_row_indices[0]
            row = fetch_data()[selected_index]
            row_id, title, content = row[0], row[1], row[2]
            update_csv_row(row_id, content, title)
            data_table.rows = display_data()
            page.update()
            status_message.value = f"ID {row_id} のタイトルとコンテンツを入れ替えました。"
        else:
            status_message.value = "行を選択してください。"
        page.update()

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
            status_message.value = content_B + "を記録しました。再度ctrl+Cでコピー、ctrl+alt+cでデータセット登録。\n"
            playsound("assets\got_data.mp3")
            content_A = ""

        page.update()

    def open_directory(e):
        """CSVファイルがあるディレクトリをエクスプローラーで開く"""
        directory = os.path.abspath(os.path.dirname("clipboard_data.csv"))
        subprocess.Popen(f'explorer "{directory}"', shell=True)

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
    status_message = ft.Text(value="ctrl+Cでコピー、ctrl+alt+cでデータセット登録", color=ft.colors.GREEN)
    guide_message = ft.Text(value="エクスプローラーで開くと、csvファイルを複製・名称変更できます", color=ft.colors.WHITE)

    open_dir_button = ft.ElevatedButton("エクスプローラーで開く", on_click=open_directory)

    # レイアウト設定
    page.add(
        ft.Column(
            [
                # add_button,  # 必要に応じてコメントを解除
                open_dir_button,
                status_message,
                guide_message,
                data_table,
            ]
        )
    )

    # キーボードショートカットの登録
    hotkey = 'ctrl + alt + c'
    keyboard.add_hotkey(hotkey, clipboard_to_csv)

# Fletアプリの実行
ft.app(target=main)
