import random
import string

from flask import Flask, request, render_template, url_for, redirect, flash

app = Flask(__name__)

class Mash(dict):
    def __getattr__(self, attr):
        return self.__getitem__(attr)
    def __setattr__(self, attr):
        return self.__setitem__(attr)
    def __delattr__(self, attr):
        return self.__delitem__(attr)

foods = []

@app.route("/")
@app.route("/wheres_the_food")
def wheres_the_food():
    return render_template("wheres_the_food.html", foods=foods)

@app.route("/add_food.form")
def add_food_form():
    return render_template("add_food_form.html")

@app.route("/add_food.post", methods=["POST"])
def add_food():
    result = Mash(
        name=request.form['name'],
        description=request.form['description'],
        time=request.form['time'],
        location=request.form['location'],
    )
    foods.append(result)
    flash("Successfully added a new food event.")
    return redirect(url_for('wheres_the_food'))

def random_string(N):
    # Source: StackOverflow
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

if __name__ == "__main__":
    app.debug = True
    app.secret_key = random_string(120)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
