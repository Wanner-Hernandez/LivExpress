from flask import Flask,flash
from flask import render_template,request,abort
from flask_mail import Mail,Message
from markupsafe import Markup
from jinja2 import contextfilter
from liveexpress.models import Post
from . import main


#Creates the flask mail through the gmail account (livexpress.help@gmail.com
app = Flask("")

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'livexpress.help@gmail.com'
app.config['MAIL_PASSWORD'] = 'CMSC495#team'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

ml = Mail(app)
ml.init_app(app)

def evalify(string):
    html = []
    try:
        if string is not None:
            listify = eval(string)

            for hashtag in listify:
                html.append(hashtag)
            return html
        else:
            return ["No Tags"]
    except:
        return ["No Tags"]

#Function that runs the home page
@main.route("/")
@main.route("/index")
def index():
    return render_template('index.html')

#Function that runs the feed page
@main.route("/feed")
def feed():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('feed.html', posts=posts, evalify=evalify)


#Function that runs the about us page
@main.route("/about")
def about():
    return render_template('about.html')


#Function that is no longer used
@main.route("/contact", methods = ["GET"])
def contact():
    return render_template('contact.html')

@main.route("/play")
def play():
#Just playing with new styles for a better about me page
    return render_template('about.html')

@main.route("/about#contact")
def aboutContact():
    return render_template('about.html#contact')

#Function to test
@main.route("/test")
def test():
    abort(500)


#Function that sends contact form to livexpress.help@gmail.com account
@main.route("/email", methods = ["POST"])
def email():
    msg = Message(request.form["reason"], sender = "livexpress.help@gmail.com",
                  recipients = ["livexpress.help@gmail.com"])

    msg.body = "Support Ticket" + "\n\n" + "Users Name: " + request.form["lastname"] + ", " + request.form["firstname"] + \
               "\n" + "Email: " + request.form['email']  + "\n" + "Contact Reason: " + request.form['reason'] + "\n" \
               + "Subject: " + request.form['subject']

    ml.send(msg)
    flash('Your message has been submitted successfully!', 'success')
    return render_template('about.html')