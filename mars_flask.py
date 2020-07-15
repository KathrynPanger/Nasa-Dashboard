############
#Flask Ap Starts Here
############
from flask import Flask

app=Flask(__name__)


@app.route("/")
def home():
    return("go to scrape")

@app.route("/scrape")
def scrape():
    from scrape.py import scrape

if __name__=="__main__":
    app.run(debug=True)