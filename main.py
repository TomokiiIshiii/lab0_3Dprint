from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, UserMixin, login_required
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row
import os
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash

# .envファイルの読み込み
load_dotenv()

# Flaskアプリケーションの作成
app = Flask(__name__)


# ログイン関係
login_manager = LoginManager()
login_manager.init_app(app) #ログイン管理をFlaskアプリ app に適用する

# ユーザーを表すクラス
class User(UserMixin):
    def __init__(self, id): # ユーザーオブジェクトを作るときに呼ばれる
        self.id = id    # 受け取ったIDを、そのユーザーのIDとして保存する

# ユーザーIDからユーザー情報を読み込む関数として登録
@login_manager.user_loader
def load_user(user_id):
     # 渡されたユーザーIDが環境変数 LOGIN_USER の値と一致するか確認
    if user_id == os.getenv('LOGIN_USER'):
        return User(user_id)    # 一致した場合、ユーザーオブジェクトを作成して返す
    return None

# Flask-Bootstrapの初期化
bootstrap = Bootstrap(app)

# データベース接続
def connect_db():
    return psycopg.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        row_factory=dict_row  # クエリ結果を辞書形式で取得
    )

# 進捗確認画面
@app.route('/')
def progress():
    with connect_db() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT apply_id, progress_status, engraving_text, remark_text FROM requests;")
                db_requests = cur.fethcall()
            except Exception as e:
                print('データ取得に失敗', e)
                return 'データ取得に失敗', 500
    return render_template('progress.html', requests=db_requests)

# lab0メンバ－ログイン画面
@app.route('/member-login', methods=['GET', 'POST'])
def member_login():
    if request.method == 'GET':
        return render_template('member-login.html')
    elif request.method == 'POST':
        username = request.form.get('userame')
        password = request.form.get('password')
        if username == os.getenv('LOGIN_USER') and check_password_hash(os.getenv('LOGIN_PASSWORD_HASH'), password):
            user = User(id=username)
            login_user(user)
            return redirect(url_for('member'))
        else:
            return render_template('member-login.html', error='ユーザー名またはパスワードが間違っています')

# lab0メンバー画面
@app.route('/member')
def member():
    pass