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

def save_story_to_db(conn, prompt, story):
    cursor = conn.cursor()
    # cursor.execute("CREATE TABLE IF NOT EXISTS stories (id INT AUTO_INCREMENT PRIMARY KEY, story_text TEXT)")
    cursor.execute("INSERT INTO GenStory (GenStoryRequest, GenStoryResponse) VALUES (%s, %s);", (prompt, story))
    conn.commit()

def get_story_by_id(conn, story_id):
    cursor = conn.cursor()
    cursor.execute("SELECT story_text FROM stories WHERE id = %s;", (story_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_story_username(conn, input_username):
    cursor = conn.cursor()
    cursor.execute("SELECT child.childname FROM user INNER JOIN child ON user.userid = child.userid WHERE user.username = %s ;", (input_username, ))
    result = cursor.fetchone()
    return result[0] if result else None

def get_story_mapplace(conn, input_mapplace):
    cursor = conn.cursor()
    cursor.execute("SELECT mapplace FROM map WHERE mapplace = %s ;", (input_mapplace, ))
    result = cursor.fetchone()
    return result[0] if result else None

def create_story_prompt(conn, prompt_story_start, input_username):
    username = get_story_username(conn, input_username)
    mapplace = get_story_mapplace(conn, input_mapplace)
    prompt_story_all = """あなたは優秀なストーリーテラーです。次のガイドラインに従い、物語を出力してください。
    # 指示
    物語の題材:ポケモン
    出力文字数:250文字程度
    主人公:
    """+ username + """、ピカチュウ
    舞台:
    """+ mapplace + """
    登場キャラクター：他のポケモンキャラクター
    世界観：ポケモン
    言語：日本語
    出力内容:物語部分のみ物語部分のみ。コマンドに対する返答や補足説明は不要
    次の文章に続く物語を生成
    """ + prompt_story_start
    print(prompt_story_all)
    return prompt_story_all

def generate_story(prompt_story_all, max_tokens=500):
    ### gpt3.5-turbo
    # response = client.completions.create(
    #     model="gpt-3.5-turbo-instruct",
    #     prompt = prompt_story_all,
    #     max_tokens = max_tokens
    # )
    # generated_story = response.choices[0].text

    ### gpt4
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt_story_all}
        ],
        max_tokens = max_tokens
    )
    generated_story = response.choices[0].message.content
    # print(type(story))
    return generated_story

def generate_story_module(input_story_id, input_story_start):
    # MySQLデータベースの接続情報を設定
    host = MYSQL_HOST
    user = MYSQL_USERNAME
    password = MYSQL_PASSWORD
    database = DATABASE_NAME
    # ssl_ca = SSL_CA

    conn = create_connection(host, user, password, database)
    # ユーザーに物語の参照または新規作成を選択させる
    # choice = input("新しい物語を生成するには 'new' を、過去の物語を参照するにはそのIDを入力してください: ")
    choice = input_story_id
    # if choice.isdigit():
    #     story_id = int(choice)
    #     existing_story = get_story_by_id(conn, story_id)
    #     if existing_story:
    #         print("参照された物語:", existing_story)
    #         prompt = existing_story + "\n\n続き: "  # 続編のプロンプト
    #     else:
    #         print("指定されたIDの物語は見つかりませんでした。新しい物語を生成します。")
    #         prompt = input("物語の始まりを入力してください: ")
    # elif choice == 'new':
    #     prompt = input("物語の始まりを入力してください: ")
    # else:
    #     print("無効な選択です。新しい物語を生成します。")
    #     prompt = input("物語の始まりを入力してください: ")

    prompt_story_start = input_story_start
    prompt_story_all = create_story_prompt(conn, prompt_story_start, input_username)
    generated_story = generate_story(prompt_story_all)
    print("生成された物語:", generated_story)

    # 生成された物語をデータベースに保存
    save_story_to_db(conn, prompt_story_all, generated_story)
    return generated_story

def main():
    input_story_id = 'new'
    input_story_start = '公園で'
    generate_story_module(input_story_id, input_story_start)

if __name__ == "__main__":
    main()