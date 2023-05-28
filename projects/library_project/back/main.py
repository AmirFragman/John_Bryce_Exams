import json
import flask
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime, date
from flask_cors import CORS

app = Flask(__name__, static_url_path="", static_folder="static")
app.config['SECRET_KEY'] = "SECRET_KEY_CODE"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)
CORS(app)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

app.json_encoder = CustomJSONEncoder

# <---------------------------------creating tables-------------------------------------------------------------->

# Customers table - columns: id (PK), name, city, age, active
class Customers(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, name, city, age):
        self.name = name
        self.city = city
        self.age = age

    def __repr__(self):
        return f"Customer: ('{self.id}', '{self.name}','{self.city}','{self.age}')"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "age": self.age,
            "active": self.active
        }
    
# Books table - columns: id(PK), name, author, year, book_type, active
class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    book_type = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default = True)

    def __init__(self, name, author, year, book_type):
        self.name = name
        self.author = author
        self.year = year
        self.book_type = book_type

    def __repr__(self):
        return f"Books('{self.id}', '{self.name}','{self.author}','{self.year}','{self.book_type}',)"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'year': self.year,
            'book_type': self.book_type,
            
        }
# Loans table - columns: id(PK), cust_id(FK), book_id(FK), loan_date, return_date, active
class Loans(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key= True)
    cust_id = db.Column(db.Integer, db.ForeignKey(Customers.id))
    book_id = db.Column(db.Integer, db.ForeignKey(Books.id))
    loan_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    active = db.Column(db.Boolean, default = True)

    customer = db.relationship("Customers", backref="Loans")
    book = db.relationship("Books", backref="Loans")

    def __init__(self, cust_id, book_id, loan_date, return_date):
        self.cust_id = cust_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.return_date = return_date

    def __repr__(self):
        return f"Loans('{self.id}, {self.cust_id}, {self.book_id}', '{self.loan_date}','{self.return_date}')"
    
    def to_dict(self):
        return {
            'id': self.id,
            'cust_id': self.cust_id,
            'book_id': self.book_id,
            'loan_date': self.loan_date,
            'return_date': self.return_date
        }
    
# <---------------------------------END of creating tables-------------------------------------------------------------->    

# <---------------------------------server routes and methods----------------------------------------------------------->   
# MY_SERVER = http://127.0.0.1:5000

# Homepage
@app.route("/")
def homepage():
    return flask.redirect("/index.html")

#http://127.0.0.1:5000/allcustomers 
@app.route('/allcustomers', methods = ['GET'])
def get_all_customers():
    customers = Customers.query.all()
    return flask.jsonify([customer.to_dict() for customer in customers])

#http://127.0.0.1:5000/newcustomer
@app.route('/newcustomer', methods = ['POST'])
def new_customer():
    request_data = request.get_json()
    name= request_data["name"]
    city= request_data["city"]
    age= request_data["age"]

    if not name or not city or not age:
        return flask.jsonify({'error': 'Missing required fields'})

    newCustomer = Customers(name = name, city = city, age = age)
    db.session.add(newCustomer)
    db.session.commit()

    return flask.jsonify({'message': 'Customer created successfully'})

#http://127.0.0.1:5000/allbooks 
@app.route("/allbooks")
def show_books():
    books = Books.query.all()
    return flask.jsonify([book.to_dict() for book in books])

#http://127.0.0.1:5000/newbook
@app.route('/newbook', methods = ['POST'])
def new_book():
    request_data = request.get_json()
    name= request_data["name"]
    author= request_data["author"]
    year= request_data["year"]
    book_type = request_data["book_type"]

    if not name or not author or not year or not book_type:
        return flask.jsonify({'error': 'Missing required fields'})

    newBook = Books(name = name, author = author, year = year, book_type = book_type)
    db.session.add(newBook)
    db.session.commit()

    return flask.jsonify({'message': 'Book created successfully'})

#http://127.0.0.1:5000/allLoans 
@app.route("/allLoans", methods=["GET"])
def show_loans():
    loans = Loans.query.all()
    return flask.jsonify([loan.to_dict() for loan in loans])

#http://127.0.0.1:5000/newloan
@app.route('/newloan', methods = ['POST'])
def new_loan():
    request_data = request.get_json()
    cust_id= request_data["cust_id"]
    book_id= request_data["book_id"]
    loan_date = request_data.get('loan_date')
    return_date = request_data.get('return_date')

    if not cust_id or not book_id or not loan_date or not return_date:
        return flask.jsonify({'error': 'Missing required fields'})
    
    try:
        cust_id = int(cust_id)
        book_id = int(book_id)
        loan_date = datetime.strptime(loan_date, '%Y-%m-%d').date()
        return_date = datetime.strptime(return_date, '%Y-%m-%d').date()
    except ValueError:
        return flask.jsonify({'error': 'Invalid field values'})
    
    customer = Customers.query.get(cust_id)
    book = Books.query.get(book_id)

    if not customer or not book:
        return flask.jsonify({'error': 'Customer or book does not exist'})
    
    newLoan = Loans(cust_id=cust_id, book_id=book_id, loan_date=loan_date, return_date=return_date)
    db.session.add(newLoan)
    db.session.commit()

    return flask.jsonify({'message': 'Loan created successfully'})

# <---------------------------------END of server routes and methods-------------------------------------------------------------------> 

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)