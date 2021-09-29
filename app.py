from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
import pandas as pd
import pandas.io.common
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload-file", methods=["GET", "POST"])
def upload_file():
    if request.method=="POST":

        if request.files:
            file = request.files["CSV-file"]
            file.save('/static/file.csv')
            print("Success saving")
            df = pd.read_csv("/static/file.csv")
            try: 
                return render_template("graph.html", tokens = df["Currency"].unique())
            except KeyError:
                return redirect("/")
        else:
            return redirect("/")

@app.route("/<token>")
def graph(token):
    df = pd.read_csv("/static/file.csv")
    df.set_index(df["Currency"], inplace=True)
    df_al = df.copy()
    df_al.drop(["Updated At", "Status"], axis=1, inplace=True)
    df_al["Created At"] = df_al["Created At"].apply(lambda x: x[:10])
    # df_al["Total Quantity"] = df_al["Total Quantity"].apply(lambda x: round(x, 2))
    quantity, date = list(df_al.loc[token]["Total Quantity"]), list(df_al.loc[token]["Created At"])
    return render_template("graph.html", token=token, data=quantity, labels=date, tokens = df["Currency"].unique())

if __name__ == "__main__":
    app.run(debug=True)
