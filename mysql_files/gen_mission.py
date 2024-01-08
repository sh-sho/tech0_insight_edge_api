import os
import openai
from openai import OpenAI
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()
# set env
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USERNAME = os.getenv('MYSQL_USERNAME')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')
# SSL_CA = os.getenv('SSL_CA')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI()

# input variables
input_username = '田中太郎'
input_mapplace = '品川'

def create_connection(host_name, user_name, user_password, db_name):
    conn = None
    try:
        conn = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            # ssl_ca=ssl_ca
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return conn

def save_mission_to_db(conn, prompt, story):
    cursor = conn.cursor()
    # cursor.execute("CREATE TABLE IF NOT EXISTS stories (id INT AUTO_INCREMENT PRIMARY KEY, story_text TEXT)")
    cursor.execute("INSERT INTO GenMission (GenMissionRequest, GenMissionResponse) VALUES (%s, %s);", (story, prompt))
    conn.commit()

def get_mission_by_id(conn, story_id):
    cursor = conn.cursor()
    cursor.execute("SELECT story_text FROM stories WHERE id = %s;", (story_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_mission_username(conn, input_username):
    cursor = conn.cursor()
    cursor.execute("SELECT child.childname FROM user INNER JOIN child ON user.userid = child.userid WHERE user.username = %s ;", (input_username, ))
    result = cursor.fetchone()
    return result[0] if result else None

def get_mission_mapplace(conn, input_mapplace):
    cursor = conn.cursor()
    cursor.execute("SELECT mapplace FROM map WHERE mapplace = %s ;", (input_mapplace, ))
    result = cursor.fetchone()
    return result[0] if result else None

def create_mission_prompt(conn, input_username):
    username = get_mission_username(conn, input_username)
    prompt_mission_all = """あなたは優秀なストーリーテラーです。
    以下の条件でミッションを生成してください。
    ミッションのタイトルはありきたりなものではなく「実施者の年齢」でも興味が湧くものにしてください。
    ミッションの内容はステップを分けて実施者が何をすればよいのか明確に指示してください。
    ミッション数は最大で5つです。
    分けたステップに対し、所要時間を記載してください。
    ミッションの難易度は提示する「探求、探究リスト」を参考にし、年齢に応じて調整してください。
    生成するミッションには条件の文言は使用せず「実施者の年齢」でも楽しめるように工夫してください。
    生成されたミッションの文言を実施者が見ると想定して文言を生成してください。
    文言はついミッションをやってみたくなるような親しみやすいものにしてください。
    実施者の名前：
    """ + username + """
    文字数：500文字
    実施者の年齢：5歳
    ミッション実施者：子
    ミッション監督者：親
    ミッション所要時間：30分
    場所：品川駅
    対象：新幹線
    探求、探究リスト：
    ・対象を探す
    ・対象が見えるところを探す
    ・対象と似ているものを探す
    ・対象と同じような色のものを複数集める
    ・対象と同じような感触のものを複数集める
    ・対象と同じような形のものを複数集める
    ・その他、年齢に応じた最適な探求、探究
    ミッション完了条件：
    ・ミッションを通して発見したことを実施者は監督者に報告する
    ・ミッションを通して発見したことをスケッチする
    ・その他、年齢に応じた最適な振り返り方法
    """
    print(prompt_mission_all)
    return prompt_mission_all

def generate_mission(prompt_mission_all, max_tokens=800):
    ### gpt-3.5-turbo
    # response = client.completions.create(
    #     model="gpt-3.5-turbo-instruct",
    #     prompt = prompt_mission_all,
    #     max_tokens = max_tokens
    # )
    # generated_mission = response.choices[0].text

    ### gpt-4
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt_mission_all}
        ],
        max_tokens = max_tokens
    )
    # print(response)
    generated_mission = response.choices[0].message.content
    # print(type(story))
    return generated_mission

def generate_mission_module():
    # MySQLデータベースの接続情報を設定
    host = MYSQL_HOST
    user = MYSQL_USERNAME
    password = MYSQL_PASSWORD
    database = DATABASE_NAME
    # ssl_ca = SSL_CA

    conn = create_connection(host, user, password, database)
    # ユーザーに物語の参照または新規作成を選択させる

    prompt_mission_all = create_mission_prompt(conn, input_username)
    generated_mission = generate_mission(prompt_mission_all)
    print("生成されたMission:", generated_mission)

    # 生成された物語をデータベースに保存
    save_mission_to_db(conn, prompt_mission_all, generated_mission)
    return generated_mission

def main():
    generate_mission_module()

if __name__ == "__main__":
    main()