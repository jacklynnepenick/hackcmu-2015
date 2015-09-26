import random
import string
import os
from datetime import datetime, timedelta

from humanize import naturaltime as humantime
from flask import Flask, request, render_template, url_for, redirect, flash, send_from_directory

app = Flask(__name__)

class Mash(dict):
    def __getattr__(self, attr):
        return self.__getitem__(attr)
    def __setattr__(self, attr):
        return self.__setitem__(attr)
    def __delattr__(self, attr):
        return self.__delitem__(attr)

foods = []
favoriteFood = 0
favFoods = []

@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

@app.route("/addFavorite/<user>/<food>")
def add_favorite(user,food):
    for element in foods:
        if element.name == food:
            favFoods.append(element)
    return ""

@app.route("/")
@app.route("/index")
def login():
    return render_template("index.html")

@app.route("/wheres_the_food.form")
def wheres_the_food():
    try:
        while foods[0].time < datetime.now() - timedelta(hours=2):
            del foods[0]
    except IndexError: pass

    return render_template("wheres_the_food.html", foods=foods, humantime=humantime)

@app.route("/user_homepage")
def user_homepage():
    return render_template('user_homepage.html', favFoods=favFoods, humantime=humantime)

@app.route("/login-in", methods=["POST"])
def loginIn():
    username = request.form['username']
    password = request.form["password"]
    return redirect(url_for('wheres_the_food')) 

@app.route("/wheres_the_food.post", methods=["POST"])
def search_for():
    search = request.form['search']
    newFoods = []
    for food in foods:
        if search in food.name or search in food.description or search in food.location:
            newFoods.append(food)
    return render_template('search_result.html', newFoods=newFoods, humantime=humantime)

@app.route("/add_food.form")
def add_food_form():
    return render_template("add_food_form.html", nowtime=datetime.now().strftime("%Y/%m/%d %H:%M"))

@app.route("/add_food.post", methods=["POST"])
def add_food():
    time = request.form['time']
    time = datetime.strptime(time, "%Y/%m/%d %H:%M")
    if(len(request.form['name']) == 0 or len(request.form['description']) == 0 or len(request.form['location']) == 0):
        flash("Please fill out all boxes.")
        return render_template("add_food_form.html", nowtime=datetime.now().strftime("%Y/%m/%d %H:%M"))
    elif("here" in request.form['location'].lower()):
        flash("Use descriptive location please")
        return render_template("add_food_form.html", nowtime=datetime.now().strftime("%Y/%m/%d %H:%M"))
    result = Mash(
        name=request.form['name'], 
        description=request.form['description'],
        time=time,
        location=request.form['location'],
    )

    foods.append(result)
    foods.sort(key=lambda x: x.time)
    flash("Successfully added a new food event.")
    return redirect(url_for('wheres_the_food'))

def random_string(N):
    # Source: StackOverflow
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

def run():
    app.secret_key = random_string(120)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    run()
