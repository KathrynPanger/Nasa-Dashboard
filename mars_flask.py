############
#Flask Ap Starts Here
############
from flask import Flask, render_template
import pymongo
#from scrape.py import scrape

app = Flask(__name__)

conn='mongodb://localhost:27017'
client=pymongo.MongoClient(conn)

db=client.mars_db
mars_info = db.mars
db.mars.drop()

db.mars.insert_many(
    [
        {
            'player': 'Jessica',
            'position': 'Point Guard'
        },
        {
            'player': 'Mark',
            'position': 'Center'
        }
    ]
)
@app.route("/")
def home():
    mongolist=list(db.mars.find())
    print(mongolist)
    return render_template("index.html",text="Mission to Mars?", data=mongolist)



if __name__ == "__main__":
    app.run(debug=True)