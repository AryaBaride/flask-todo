from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/tasks"
mongo = PyMongo(app)



@app.route('/')
def index():
    tasks = mongo.db.tasks.find()
    return render_template('main.html', tasks=tasks)




@app.route('/add', methods=['POST'])
def add():
    new_task = request.form['task']
    mongo.db.tasks.insert_one({'task': new_task, 'complete': False})
    return redirect(url_for('index'))



@app.route('/complete/<oid>')
def complete(oid):
    task = mongo.db.tasks.find_one_and_update(
        {"_id": oid, 'complete': False},
        {"$set": {'complete': True}},
        return_document=True
    )
    return redirect(url_for('index'))



@app.route('/delete_completed')
def delete_completed():
    mongo.db.tasks.delete_many({'complete': True})
    return redirect(url_for('index'))



@app.route('/delete_all')
def delete_all():
    mongo.db.tasks.delete_many({})
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
