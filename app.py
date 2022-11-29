from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.yxgix5r.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')
@app.route("/todo", methods=["POST"])
def todo_post():
    todo_receive = request.form['todo_give']

    todo_list = list(db.todo.find({}, {'_id':False}))
    count = len(todo_list) + 1

    doc = {
        'num' : count,
        'todo': todo_receive,
        'done' : 0
    }
    db.todo.insert_one(doc)

    return jsonify({'msg' : '할 일 등록'})
@app.route('/todo', methods=["GET"])
def todo_get():
    todo_list = list(db.todo.find({}, {'_id':False}))
    return jsonify({'todos' : todo_list})
@app.route('/todo/done', methods=["POST"])
def todo_done():
    num_receive = request.form['num_give']
    db.todo.update_one({'num':int(num_receive)}, {'$set':{'done':1}})
    return jsonify({'msg':'할 일 완료'})

@app.route('/todo/del', methods=["POST"])
def todo_del():
    num_receive = request.form['num_give']
    db.todo.delete_one({'num':int(num_receive)})
    return jsonify({'msg' : '삭제 완료'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)