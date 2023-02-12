from flask import Flask, render_template, request, redirect
from datetime import datetime
import encoding
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(400),nullable=False)
    date = db.Column(db.DateTime,default = datetime.utcnow)
    def __repr__(self):
        return f"{self.sno}-{self.title}"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)


@app.route('/login')
def login():
    try:
        user = User(username="mrtechnostart",email="rambpandey238@gmail.com",password=encoding.make_hashes("rambpandey238@gmail.com"))
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    except IntegrityError:
        return "Badd Dublicate Credentials"
with app.app_context():
    db.create_all()

@app.route('/',methods=["GET","POST"])
def hello_world():
    if request.method == "POST":
        todo = Todo(title=request.form["title"],desc = request.form["desc"])
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html',todo = allTodo)

@app.route('/root')
def admin():
    return '<h1>Admin Page</h1>'
@app.route('/delete/<int:sno>')
def delete(sno):
    delete = Todo.query.filter_by(sno=sno).first()
    db.session.delete(delete)
    db.session.commit()
    return redirect("/")
@app.route('/update/<int:sno>',methods=["GET","POST"])
def update(sno):
    if request.method == "POST":
        record = Todo.query.filter_by(sno=sno).first()
        record.title = request.form["title"]
        record.desc = request.form["desc"]
        db.session.add(record)
        db.session.commit()
        return redirect("/")
    record = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",record=record)
def admin():
    return '<h1>Admin Page</h1>'
if __name__ == "__main__":
    app.run(debug=True)