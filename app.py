# -*- coding: UTF-8 -*-

from flask import Flask, jsonify, request, abort, url_for, render_template
import requests
import json
# import marshmallow as ma
# from flask_smorest import Api, Blueprint, abort
from mysql_files import gen_mission, gen_story

app = Flask(__name__)
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.json.ensure_ascii = False
# api = Api(app)

# class PetSchema(ma.Schema):
#     id = ma.fields.Int(dump_only=True)
#     name = ma.fields.String()

# サンプルのデータベース代わりにリストを使用
tasks = [
    {
        'id': 1,
        'title': 'Task 1',
        'done': False
    },
    {
        'id': 2,
        'title': 'Task 2',
        'done': False
    }
]

# indexページの表示
@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')

# タスク一覧を取得するエンドポイント
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

# 特定のタスクを取得するエンドポイント
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        abort(404, description='Task not found')
    return jsonify({'task': task})

# タスクを追加するエンドポイント
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400, description='Title is required')

    new_task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'done': False
    }
    tasks.append(new_task)
    return jsonify({'task': new_task}), 201

@app.route('/genmission', methods=['GET'])
def get_mission():
    result = gen_mission.generate_mission_module()
    return jsonify({'genmission': result})

@app.route('/genstory', methods=['GET'])
def get_story():
    req = request.args
    input_story_id = req.get('story_id')
    print(input_story_id)
    input_story_start = req.get('story_start')
    print(input_story_start)
    result = gen_story.generate_story_module(input_story_id, input_story_start)
    return jsonify({'genstory': result})


if __name__ == '__main__':
    app.run(debug=True)
