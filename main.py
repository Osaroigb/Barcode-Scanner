# import required modules
from flask import Flask, render_template, redirect, url_for, request, flash
import requests
import os

# setup flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


# home route
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":

        return render_template("index.html")

    elif request.method == "POST":

        barcode = request.form["nutrition_search"]

        if barcode != "":

            req_header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/87.0.4280.141 Safari/537.36",
                "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,es;q=0.7",
                "Content-Type": "application/json"
            }

            food_response = requests.get(url=f"https://us.openfoodfacts.org/api/v0/product/{barcode}",
                                         headers=req_header)
            food_response.raise_for_status()
            food_data = food_response.json()

            return render_template("index.html", food=food_data)
        else:
            flash("You didn't type in any barcode!")  # generate an error message when a barcode isn't entered
            return redirect(url_for("home"))


# start the flask application
if __name__ == "__main__":
    app.run(debug=True)
