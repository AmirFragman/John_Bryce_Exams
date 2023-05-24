from flask import Flask
import flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__, static_url_path="", static_folder="static")
CORS(app)

app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\Amir\\coding\\John_Bryce_Exams\\projects\\library_project\\back\\library.db'
db = SQLAlchemy(app)

class Customers(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    # def __init__(self, cust_name, city, age):
    #     self.cust_name = cust_name
    #     self.city = city
    #     self.age = age

    def __repr__(self):
        return f"Customer('{self.id}', '{self.name}','{self.city}','{self.age}', '{self.active}')"
    
    def __str__(self):
        return self.__repr__()
    
    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "age": self.age,
            "active": self.active
        }
  
# class Books(db.Model):
#     book_ID = db.Column(db.Integer, primary_key=True)
#     book_name = db.Column(db.String(100), nullable=False)
#     authur = db.Column(db.String(50), nullable=False)
#     year = db.Column(db.Integer, nullable=False)
#     book_type = db.Column(db.Integer, nullable=False)

#     def __init__(self, book_name, authur, year, book_type):
#         self.book_name = book_name
#         self.authur = authur
#         self.year = year
#         self.book_type = book_type

#     # def _repr_(self):
#     #     return f"Books('{self.book_ID}', '{self.book_name}','{self.authur}','{self.year}','{self.book_type}')"

# class Loans(db.Model):
#     id = db.Column(db.Integer, db.ForeignKey(Customers.id), primary_key=True)
#     book_ID = db.Column(db.Integer, db.ForeignKey(Books.book_ID), primary_key=True)
#     loan_date = db.Column(db.String(10), nullable=False)
#     return_date = db.Column(db.String(10), nullable=False)
#     loan_active = db.Column(db.Boolean, default = True)


#     def __init__(self, loan_date, return_date):
#         self.loan_date = loan_date
#         self.return_date = return_date

    # def _repr_(self):
    #     return f"Loans('{self.id}, {self.book_ID}', '{self.loan_date}','{self.return_date}')"
@app.route("/")
def homepage():
    return flask.redirect("/index.html")

@app.route("/customers")
def show_customers():
    results = Customers.query.all()
    return flask.jsonify([customer.as_dict() for customer in results])
    
if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)