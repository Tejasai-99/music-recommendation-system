from flask import Flask, render_template, request
import recommendation  # import your recommendation.py

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    recs = []
    if request.method == "POST":
        song = request.form["song"]
        recs = recommendation.recommend(song, top_n=5)
    return render_template("index.html", recs=recs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
