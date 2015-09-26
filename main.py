from flask import Flask, request

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
    result = "<html><body><table>"
    result += """
        <tr>
            <th>Name</th>
            <th>Time</th>
            <th>Location</th>
        </tr>"""
    for food in foods:
        result += """
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
            </tr>
        """ % (food.name, food.time, food.location)
    return result

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
