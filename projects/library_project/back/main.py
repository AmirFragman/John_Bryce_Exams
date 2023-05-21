from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

class Customer(db.Model):
    cust_ID = db.Column(db.Integer, primary_key=True)
    cust_name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    age = db.Column(db.String(50), nullable=False)

    def __init__(self, cust_ID, cust_name, city, age):
        self.cust_ID = cust_ID
        self.cust_name = cust_name
        self.city = city
        self.age = age

    # def _repr_(self):
    #     return f"Customer('{self.cust_ID}', '{self.cust_name}','{self.city}','{self.age}')"

class Books(db.Model):
    book_ID = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    authur = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    book_type = db.Column(db.Integer, nullable=False)

    def __init__(self, book_ID, book_name, authur, year, book_type):
        self.book_ID = book_ID
        self.book_name = book_name
        self.authur = authur
        self.year = year
        self.book_type = book_type

    # def _repr_(self):
    #     return f"Books('{self.book_ID}', '{self.book_name}','{self.authur}','{self.year}','{self.book_type}')"

class Loans(db.Model):
    cust_ID = db.Column(db.Integer, db.ForeignKey(Customer.cust_ID), primary_key=True)
    book_ID = db.Column(db.Integer, db.ForeignKey(Books.book_ID), primary_key=True)
    loan_date = db.Column(db.String(10), nullable=False)
    return_date = db.Column(db.String(10), nullable=False)

    def __init__(self, cust_ID, book_ID, loan_date, return_date):
        self.cust_ID = cust_ID
        self.book_ID = book_ID
        self.loan_date = loan_date
        self.return_date = return_date

    # def _repr_(self):
    #     return f"Loans('{self.cust_ID}, {self.book_ID}', '{self.loan_date}','{self.return_date}')"
@app.route("/")
def homepage():
    return "Hello"
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)