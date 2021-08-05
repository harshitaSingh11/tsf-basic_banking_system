from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/grip_bank'
db = SQLAlchemy(app)
app.secret_key = 'dont'


class Transactions(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(20), unique=False, nullable=False)
    receiver = db.Column(db.String(20), unique=False, nullable=False)
    amount = db.Column(db.String(10), unique=False, nullable=False)


class Users(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    balance = db.Column(db.String(10), unique=False, nullable=False)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/users", methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        result = Users.query.all()
        print(result)
    return render_template('users.html', result=result)


@app.route("/transaction", methods=['GET', 'POST'])
def transaction():
    trans = Users.query.all()
    if request.method == 'POST':
        sender = request.form.get('sender')
        receiver = request.form.get('receiver')
        amount = request.form.get('amount')
        entry = Transactions(sender=sender, receiver=receiver, amount=amount)
        if receiver != sender:
            edited = db.session.query(Users).filter_by(name=receiver).one()
            edited.balance += int(amount)
            edited3 = db.session.query(Users).filter_by(name=sender).one()

            # if balance is greater than amount to be transferred only then transaction occurs
            if edited3.balance >= int(amount):
                edited3.balance -= int(amount)
                db.session.add(entry)
                db.session.commit()
                result = Transactions.query.all()
                print(result)
                return render_template('history.html', result=result)
    return render_template('transaction.html', trans=trans)


@app.route("/history", methods=['GET', 'POST'])
def history():
    if request.method == 'GET':
        result = Transactions.query.all()
        print(result)
    return render_template('history.html', result=result)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
