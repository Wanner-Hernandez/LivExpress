from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField


app = Flask(__name__)

app.config["SECRET_KEY"] = "Misfoimew50932"

class MyForm(FlaskForm):
    image = FileField("image")

@app.route('/', methods=["GET", "POST"])
def index():
    form = MyForm()

    if form.validate_on_submit():
        print(form.image.data)

    return render_template("index.html", form=form)

app.run(port=5003)