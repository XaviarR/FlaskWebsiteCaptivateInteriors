from flask import Flask, render_template, redirect, request

from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#create flask instance
app = Flask(__name__)
#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#secret key
app.config['SECRET_KEY'] = "secret"
#init database
db = SQLAlchemy(app)

#create model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Name %r>' % self.name
    
with app.app_context():
    # create the database tables
    db.create_all()
    
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")
    

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/shop")
def shop():
    return render_template("shop.html")
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
    name = form.name.data
    form.name.data = ''
    form.email.data = ''
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name,our_users=our_users)
@app.route("/user/update/<int:id>", methods=["GET", "POST"])
def update(id):
    user_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        user_to_update.name = request.form["name"]
        user_to_update.email = request.form["email"]
        try:
            db.session.commit()
            return redirect("/user/add")
        except:
            return "There was an error"
    else:
        return render_template("update_user.html", user_to_update=user_to_update)
@app.route("/user/delete/<int:id>")
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect("/user/add")
    except:
        return "There was an error"
        

if __name__ == "__main__":
    app.run(debug=True)
