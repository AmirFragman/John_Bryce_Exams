from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

class Customer(db.Model):
    custID = db.Column(db.Integer, primary_key=True)
    custname = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    age = db.Column(db.String(50), nullable=False)

    def __init__(self, custID, custname, city, age):
        self.custID = custID
        self.custname = custname
        self.city = city
        self.age = age

    # def __repr__(self):
    #     return f"Customer('{self.custID}', '{self.custname}','{self.city}','{self.age}')"

class Books(db.Model):
    bookID = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.String(100), nullable=False)
    authur = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    book_type = db.Column(db.Integer, nullable=False)

    def __init__(self, bookID, bookname, authur, year, book_type):
        self.bookID = bookID
        self.bookname = bookname
        self.authur = authur
        self.year = year
        self.book_type = book_type

    # def __repr__(self):
    #     return f"Books('{self.bookID}', '{self.bookname}','{self.authur}','{self.year}','{self.book_type}')"

class Loans(db.Model):
    custID = db.Column(db.Integer, db.ForeignKey(Customer.custID), primary_key=True)
    bookID = db.Column(db.Integer, db.ForeignKey(Books.bookID), primary_key=True)
    loan_date = db.Column(db.String(10), nullable=False)
    return_date = db.Column(db.String(10), nullable=False)

    def __init__(self, custID, bookID, loan_date, return_date):
        self.custID = custID
        self.bookID = bookID
        self.loan_date = loan_date
        self.return_date = return_date

    # def __repr__(self):
    #     return f"Loans('{self.custID}, {self.bookID}', '{self.loan_date}','{self.return_date}')"

@app.route('/')
def index():
    return "Noam and Amir's Library"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    