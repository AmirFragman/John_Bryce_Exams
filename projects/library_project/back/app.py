import json
import flask
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime, date
from flask_cors import CORS
import os

app = Flask(__name__, static_url_path="", static_folder="static")
app.config['SECRET_KEY'] = "SECRET_KEY_CODE"

script_path = os.path.realpath(__file__)
script_directory = os.path.dirname(script_path)
db_path = os.path.join(script_directory, 'library.db')

app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///' + db_path
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
        return f"Customer: ('{self.id}', '{self.name}','{self.city}','{self.age}', {self.active})"

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
        return f"Books('{self.id}', '{self.name}','{self.author}','{self.year}','{self.book_type}', {self.active})"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'year': self.year,
            'book_type': self.book_type,
            'active': self.active
        }
# Loans table - columns: id(PK), cust_id(FK), book_id(FK), loan_date, return_date, active. relationships: customer, book
class Loans(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key= True)
    cust_id = db.Column(db.Integer, db.ForeignKey(Customers.id))
    book_id = db.Column(db.Integer, db.ForeignKey(Books.id))
    loan_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
   
    customer = db.relationship("Customers", backref="custLoans")
    book = db.relationship("Books", backref="bookLoans")

    def __init__(self, cust_id, book_id, loan_date, return_date):
        self.cust_id = cust_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.return_date = return_date

    def __repr__(self):
        return f"Loans('{self.id}, {self.cust_id}, {self.book_id}', '{self.loan_date}','{self.return_date}', {self.active})"
    
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

#Customers
#http://127.0.0.1:5000/allcustomers 
@app.route('/customers', methods = ['GET'])
def get_all_customers():
    customers = Customers.query.all()
    return flask.jsonify([customer.to_dict() for customer in customers])

#Customer addition
#http://127.0.0.1:5000/newcustomer
@app.route('/customers', methods = ['POST'])
def new_customer():
    data = request.get_json()
    name= data["name"]
    city= data["city"]
    age= data["age"]

    if not name or not city or not age:
        return flask.jsonify({'error': 'Missing required fields'})

    newCustomer = Customers(name, city, age)
    db.session.add(newCustomer)
    db.session.commit()

    return flask.jsonify({'message': 'Customer created successfully'})

#Customer update
#http://127.0.0.1:5000/updateCustomer/<id>
@app.route('/customers/<id>', methods = ['POST'])
def update_customer(id):
    data = request.get_json()
    updated_row = Customers.query.filter_by(id=id).first()
    if updated_row:
        updated_row.name =data["name"]
        updated_row.city =data["city"]
        updated_row.age =data["age"]
        db.session.commit()
        return f"Customer ID:{id}, Name: {updated_row.name} got updated"
    return "The customer does not exist"

#Customer deletion
#http://127.0.0.1:5000/deleteCustomer/<id>
@app.route('/customers/<id>', methods = ['DELETE'])
def delete_customer(id):
    delete_row = Customers.query.filter_by(id=id).first()
    if delete_row:
        delete_row.active = False
        db.session.commit()
        return f"Customer ID number:{delete_row.id} got deleted"
    return "The customer does not exist"

#Books
#http://127.0.0.1:5000/allbooks 
@app.route("/allBooks", methods = ['GET','POST'])
def show_books():
    books = Books.query.all()
    return flask.jsonify([book.to_dict() for book in books])
#Book addition
#http://127.0.0.1:5000/newbook
@app.route('/newBook', methods = ['POST'])
def new_book():
    data = request.get_json()
    name= data["name"]
    author= data["author"]
    year= data["year"]
    book_type = data["book_type"]

    if not name or not author or not year or not book_type:
        return flask.jsonify({'error': 'Missing required fields'})

    newBook = Books(name = name, author = author, year = year, book_type = book_type)
    db.session.add(newBook)
    db.session.commit()

    return flask.jsonify({'message': 'Book created successfully'})

#Book update
#http://127.0.0.1:5000/updateBook/<id>
@app.route('/updateBook/<id>', methods = ['GET', 'PUT'])
@app.route('/updateBook/', methods = ['PUT'])
def update_book(id):
    data = request.get_json()
    updated_row = Books.query.filter_by(id=id).first()
    if updated_row:
        updated_row.name = data['name']
        updated_row.author = data["author"]
        updated_row.year = data["year"]
        updated_row.book_type = data["book_type"]
        updated_row.active = data["active"]
        db.session.commit()
        return f"Book ID:{id}, Name: {updated_row.name} got updated"
    return "The book does not exist"

#Book deletion
#http://127.0.0.1:5000/deleteBook/<id>
@app.route('/deleteBook/<id>', methods = ['PUT'])
@app.route('/deleteBook/', methods = ['PUT'])
def delete_book(id):
    data = request.get_json()
    delete_row = Books.query.filter_by(id=id).first()
    if delete_row:
        delete_row.active = data["active"]
        db.session.commit()
        return f"Book ID:{id} got deleted"
    return "The book does not exist"

#Loans
#http://127.0.0.1:5000/allLoans 
@app.route("/allLoans", methods=['GET','POST'])
def show_loans():
    loans = Loans.query.all()
    return flask.jsonify([loan.to_dict() for loan in loans])

#http://127.0.0.1:5000/newLoan
@app.route('/newLoan', methods = ['POST'])
def new_loan():
    data = request.get_json()
    cust_id = data["cust_id"]
    book_id = data["book_id"]
    loan_date = data.get('loan_date')
    return_date = data.get('return_date')

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

#Loan update
#http://127.0.0.1:5000/updateLoan/<id>
@app.route('/updateLoan/<id>', methods = ['PUT'])
@app.route('/updateLoan/', methods = ['PUT'])
def update_loan(id):
    data = request.get_json()
    updated_row = Loans.query.filter_by(id=id).first()
    if updated_row:
        updated_row.cust_id = data["cust_id"]
        updated_row.book_id = data["book_id"]
        updated_row.loan_date = data["loan_date"]
        updated_row.return_date = data["return_date"]
        updated_row.active = data["active"]
        db.session.commit()
        return f"Loan ID:{id}, loaned by Customer: {updated_row.cust_id} got updated"
    return "The loan does not exist"

#Return book
#http://127.0.0.1:5000/returnBook/<id>
@app.route('/returnBook/<id>', methods = ['PUT'])
@app.route('/returnBook/', methods = ['PUT'])
def delete_loan(id):
    data = request.get_json()
    delete_row = Loans.query.filter_by(id=id).first()
    if delete_row:
        delete_row.active = data["active"]
        db.session.commit()
        return f"Loan ID:{id} got deleted"
    return "The loan does not exist"


# <---------------------------------END of server routes and methods-------------------------------------------------------------------> 

if __name__ == '__main__':
    app.run(debug=True)