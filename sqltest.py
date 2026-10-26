import psycopg
from psycopg.rows import dict_row
import os
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    return psycopg.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        row_factory=dict_row  # クエリ結果を辞書形式で取得
    )
    
with connect_db() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT apply_id, progress_status, engraving_text, remark_text FROM requests;")
                db_requests = cur.fetchall()
            except Exception:
                pass

print(db_requests)