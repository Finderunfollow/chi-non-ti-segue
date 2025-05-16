from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = []
    if request.method == "POST":
        following_file = request.files["following"]
        followers_file = request.files["followers"]

        if not following_file or not followers_file:
            return render_template("index.html", result=[], error="Carica entrambi i file.")

        try:
            following_data = json.load(following_file)
            followers_data = json.load(followers_file)

            following_usernames = set()
            for item in following_data.get("relationships_following", []):
                for user in item.get("string_list_data", []):
                    following_usernames.add(user["value"])

            followers_usernames = set()
            for item in followers_data:
                for user in item.get("string_list_data", []):
                    followers_usernames.add(user["value"])

            non_following_back = sorted(following_usernames - followers_usernames)
            return render_template("index.html", result=non_following_back, count=len(non_following_back))

        except Exception as e:
            return render_template("index.html", result=[], error=str(e))

    return render_template("index.html", result=[])

if __name__ == "__main__":
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

