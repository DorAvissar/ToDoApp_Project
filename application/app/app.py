from flask import Flask, render_template, request, redirect, url_for
from bson import ObjectId
from pymongo import MongoClient
import os
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')
title = "TODO sample application with Flask and MongoDB"
heading = "TODO Reminder with Flask and MongoDB"

mongo_username = os.getenv("MONGO_USERNAME")  
mongo_password = os.getenv("MONGO_PASSWORD")  
mongo_dbname = os.getenv("MONGO_DBNAME")  
mongo_host = os.getenv("MONGO_HOST")  
mongo_port = os.getenv("MONGO_PORT")  

mongo_url = f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_dbname}?authSource=admin"
client = MongoClient(mongo_url)
db = client[mongo_dbname]  # Select the database dynamically
todos = db.todo  # Select the collection name

def redirect_url():
    return request.args.get('next') or request.referrer or url_for('lists')


@app.route("/list")
def lists():
    # Display all Tasks
    todos_l = todos.find()
    a1 = "active"
    return render_template('index.html', a1=a1, todos=todos_l, t=title, h=heading)

@app.route("/")
@app.route("/uncompleted")
def tasks():
    # Display Uncompleted Tasks
    todos_l = todos.find({"done": "no"})
    a2 = "active"
    return render_template('index.html', a2=a2, todos=todos_l, t=title, h=heading)

@app.route("/completed")
def completed():
    # Display Completed Tasks
    todos_l = todos.find({"done": "yes"})
    a3 = "active"
    return render_template('index.html', a3=a3, todos=todos_l, t=title, h=heading)

@app.route("/done")
def done():
    # Done-or-not ICON
    id = request.values.get("_id")
    task = todos.find_one({"_id": ObjectId(id)})
    if task["done"] == "yes":
        todos.update_one({"_id": ObjectId(id)}, {"$set": {"done": "no"}})
    else:
        todos.update_one({"_id": ObjectId(id)}, {"$set": {"done": "yes"}})
    return redirect(redirect_url())

@app.route("/action", methods=['POST'])
def action():
    # Adding a Task
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    pr = request.values.get("pr")
    assignee = request.values.get("assignee")
    todos.insert_one({"name": name, "desc": desc, "date": date, "pr": pr, "assignee": assignee, "done": "no"})
    return redirect("/list")

@app.route("/remove")
def remove():
    # Deleting a Task with various references
    key = request.values.get("_id")
    todos.delete_one({"_id": ObjectId(key)})
    return redirect("/")

@app.route("/update")
def update_task():
    task_id = request.values.get("_id")
    task = db.collection.find_one({'_id': ObjectId(task_id)})
    return render_template('update.html', task=task)


@app.route("/action3", methods=['POST'])
def action3():
    # Updating a Task with various references
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    pr = request.values.get("pr")
    assignee = request.values.get("assignee")
    id = request.values.get("_id")
    todos.update_one({"_id": ObjectId(id)}, {'$set': {"name": name, "desc": desc, "date": date, "pr": pr, "assignee": assignee}})
    return redirect("/")

@app.route("/search", methods=['GET'])
def search():
    # Searching a Task with various references
    key = request.values.get("key")
    refer = request.values.get("refer")
    if key == "_id":
        todos_l = todos.find({refer: ObjectId(key)})
    else:
        todos_l = todos.find({refer: key})
    return render_template('searchlist.html', todos=todos_l, t=title, h=heading)

@app.route("/collections")
def collections():
    # List all collections
    collections = db.list_collection_names()
    return render_template('collections.html', collections=collections, t=title, h=heading)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
