import json
from datetime import datetime
from flask import Flask, render_template, redirect, Markup, escape, request

application = Flask(__name__)

DATE_FILE = 'norilog.json'


def save_data(start, finish, memo, created_at):
    """記録データを保存します
    :param start: 乗った駅
    :type start: str
    :param finish: 降りた駅
    :type finish: str
    :param memo: 乗り降りメモ
    :type memo: str
    :param created_at: 乗り降り日付
    :type created_at: datetime.datetime
    :return: None
    """

    try:
        # json モジュールでデータベースファイルを開きます
        database = json.load(open(DATE_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        database = []

    database.insert(0, {
        "start": start,
        "finish": finish,
        "memo": memo,
        "created_at": created_at.strftime("%Y-%m-%d %H:%M")
    })

    json.dump(database, open(DATE_FILE, mode="w", encoding="utf-8"),
              indent=4, ensure_ascii=False)


def load_data():
    """記録データを返します"""

    try:
        # json モジュールでデータベースファイルを開きます
        database = json.load(open(DATE_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        database = []
    return database


@application.route('/')
def index():
    """トップページ
    テンプレートを使用してページを表示します
    """
    # 記録データを読み込みます
    rides = load_data()

    return render_template('index.html', rides=rides)


@application.route('/save', methods=['POST'])
def save():
    """記録用URL"""
    # 記録されたデータを取得します
    start = request.form.get('start')  # 出発
    finish = request.form.get('finish')  # 到着
    memo = request.form.get('memo')  # メモ
    created_at = datetime.now()
    save_data(start, finish, memo, created_at)
    # 保存後はトップページにリダイレクトします
    return redirect('/')


@application.template_filter('nl2br')
def nl2br_filter(s):
    """改行文字をbrタグに置き換えるテンプレートフィルター"""
    return escape(s).replace('\n', Markup('<br>'))


def main():
    application.run('127.0.0.1', 8000)


if __name__ == '__main__':
    # IPアドレス0.0.0.0の8000番ポートでアプリケーションを実行します
    application.run('0.0.0.0', 8000, debug=True)
