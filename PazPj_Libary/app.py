import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime, date
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library2.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)
CORS(app)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


app.json_encoder = CustomJSONEncoder


class Customer(db.Model):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    age = Column(Integer)

    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', city='{self.city}', age={self.age})>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'age': self.age,
        }


@app.route('/')
def hello():
    return '<h1>Paz Library home page</h1>'


@app.route("/customers")
def cust_show():
    cust_list = [customer.to_dict() for customer in Customer.query.all()]
    json_data = json.dumps(cust_list)
    return json_data


@app.route('/customers/new', methods=['POST'])
def newcust():
    data = request.get_json()
    name = data['name']
    city = data['city']
    age = data['age']

    new_customer = Customer(name=name, city=city, age=age)
    db.session.add(new_customer)
    db.session.commit()
    return "A new Library Customer was created."


@app.route('/customers/delete/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)

    Loan.query.filter_by(cust_id=id).delete()

    db.session.delete(customer)
    db.session.commit()

    return {"message": "Customer deleted successfully."}


class Book(db.Model):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    bookname = Column(String)
    writer = Column(String)
    year_published = Column(Integer)
    book_loan = Column(Integer)

    def __repr__(self):
        return f"<Book(id={self.id}, name='{self.bookname}', author='{self.writer}', year_published={self.year_published}, type={self.book_loan})>"

    def to_dict(self):
        return {
            'id': self.id,
            'bookname': self.bookname,
            'writer': self.writer,
            'year_published': self.year_published,
            'book_loan': self.book_loan,
        }

##book start
@app.route("/books")
def book_show():
    book_list = [book.to_dict() for book in Book.query.all()]
    json_data = json.dumps(book_list)
    return json_data


@app.route('/books/new', methods=['POST'])
def newbook():
    data = request.get_json()
    bookname = data['bookname']
    writer = data['writer']
    year_published = data['year_published']
    book_loan = data['book_loan']

    new_book = Book(bookname=bookname, writer=writer, year_published=year_published, book_loan=book_loan)
    db.session.add(new_book)
    db.session.commit()
    return "A new book record was created."


@app.route('/books/delete/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return {"message": "Book deleted successfully."}


##books 


class Loan(db.Model):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    cust_id = Column(Integer, ForeignKey('customers.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    loan_date = Column(Date)
    return_date = Column(Date)

    customer = relationship("Customer", backref="loans")
    book = relationship("Book", backref="loans")

    def __repr__(self):
        return f"<id={self.id}cust_id={self.cust_id}, book_id={self.book_id}, loan_date='{self.loan_date}', return_date='{self.return_date}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'cust_id': self.cust_id,
            'book_id': self.book_id,
            'loan_date': self.loan_date,
            'return_date': self.return_date,
        }


@app.route("/loans")
def loan_show():
    loan_list = [loan.to_dict() for loan in Loan.query.all()]
    json_data = json.dumps(loan_list, default=str)
    return json_data


@app.route('/loans/new', methods=['POST'])
def new_loan():
    data = request.get_json()
    cust_id = int(data['cust_id'])
    book_id = int(data['book_id'])
    loan_date = datetime.strptime(data['loan_date'], '%d/%m/%Y').date()
    return_date = datetime.strptime(data['return_date'], '%d/%m/%Y').date()

    new_loan = Loan(cust_id=cust_id, book_id=book_id, loan_date=loan_date, return_date=return_date)
    db.session.add(new_loan)
    db.session.commit()
    return "A new loan record was created."


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
