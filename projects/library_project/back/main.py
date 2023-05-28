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
    active = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Customer: ('{self.id}', '{self.name}','{self.city}','{self.age}', '{self.active}')"

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

    def _repr_(self):
        return f"Books('{self.id}', '{self.name}','{self.author}','{self.year}','{self.book_type}', '{self.active})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'year': self.year,
            'book_type': self.book_type,
            'active': self.active
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

    def _repr_(self):
        return f"Loans('{self.id}, {self.cust_id}, {self.book_id}', '{self.loan_date}','{self.return_date}')"
    
    def to_dict(self):
        return {
            'id': self.id,
            'cust_id': self.cust_id,
            'book_id': self.book_id,
            'author': self.author,
            'year': self.year,
            'book_type': self.book_type,
            'active': self.active
        }
    
# <---------------------------------END of creating tables-------------------------------------------------------------->    

# <---------------------------------server routes----------------------------------------------------------------------->   
# MY_SERVER = http://127.0.0.1:5000

@app.route("/")
def homepage():
    return flask.redirect("/index.html")

# @app.route("/customers")
# def show_customers():
#     results = Customers.query.all()
#     return flask.jsonify([customer.to_dict() for customer in results])

# MY_SERVER = http://127.0.0.1:5000 + /allcustomers 

@app.route('/allcustomers', methods = ['GET', 'POST'])
def get_all_cutomers():
    res=[]
    for customer in Customers.query.all():
        res.append({"id":res.id,"name":res.name, "city":res.city, "age": res.age, "active":res.active})
    return  (json.dumps(res))

# MY_SERVER = http://127.0.0.1:5000 + /allbooks 

@app.route("/allbooks")
def show_books():
    res=[]
    for book in Books.query.all():
        res.append({"id": res.id,"name": res.name, "author": res.author,"year": res.year, "book_type": res.book_type, "active": res.active})
    return  (json.dumps(res))

# MY_SERVER = http://127.0.0.1:5000 + /allLoans 
@app.route("/allLoans")
def show_loans():
    res=[]
    for loan in Loans.query.all():
        res.append({"id": res.id, "cust_id": res.cust_id, "book_id": res.book_id, "loan_date": res.loan_date, "return_date": res.return_date, "active": res.active})
    return  (json.dumps(res))

# <---------------------------------END of server routes-----------------------------------------------------------------------> 

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)