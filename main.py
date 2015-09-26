from flask import Flask, request, render_template

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

@app.route("/add_food")
def add_food():
    result = Mash(
        name=request.args.get('name'),
        time=request.args.get('time'),
        location=request.args.get('location'),
    )
    foods.append(result)
    return "success!!!"


if __name__ == "__main__":
    app.run()
