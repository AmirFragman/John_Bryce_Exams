from datetime import datetime, timedelta
from library_150523.sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    year_published = Column(Integer)
    book_type = Column(Integer)


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    age = Column(Integer)


class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    cust_id = Column(Integer, ForeignKey('customers.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    loan_date = Column(DateTime)
    return_date = Column(DateTime)


class BooksDB:
    def __init__(self):
        self.engine = create_engine('sqlite:///books.db')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_book(self, name, author, year_published, book_type):
        book = Book(name=name, author=author, year_published=year_published, book_type=book_type)
        self.session.add(book)
        self.session.commit()

    def get_books(self):
        return self.session.query(Book).all()

    def add_customer(self, name, city, age):
        customer = Customer(name=name, city=city, age=age)
        self.session.add(customer)
        self.session.commit()

    def get_customers(self):
        return self.session.query(Customer).all()

    def add_loan(self, cust_id, book_id, loan_date):
        loan_period = None
        book_type = self.get_book_type(book_id)
        if book_type == 1:
            loan_period = timedelta(days=10)
        elif book_type == 2:
            loan_period = timedelta(days=5)
        elif book_type == 3:
            loan_period = timedelta(days=2)

        due_date = loan_date + loan_period

        loan = Loan(cust_id=cust_id, book_id=book_id, loan_date=loan_date)
        self.session.add(loan)
        self.session.commit()

        loan_id = loan.id
        return due_date, loan_id

    def return_loan(self, loan_id):
        loan = self.session.query(Loan).filter_by(id=loan_id).first()
        loan.return_date = datetime.now()
        self.session.commit()

    def get_book_type(self, book_id):
        book = self.session.query(Book).filter_by(id=book_id).first()
        return book.book_type


class TestBooksDB:
    def setup_method(self):
        self.db = BooksDB()
        self.book1 = Book(name='Book1', author='Author1', year_published=2020, book_type=1)
        self.book2 = Book(name='Book2', author='Author2', year_published=2019, book_type=2)
        self.customer1 = Customer(name='Customer1', city='City1', age=30)
        self.customer2 = Customer(name='Customer2', city='City2', age=25)

        self.loan1 = Loan(cust_id=1, book_id=1, loan_date=datetime.now())
        self.loan2 = Loan(cust_id=2, book_id=2, loan_date=datetime.now())

    def test_add_book(self):
        self.db.add_book(name='Book1', author='Author1', year_published=2020, book_type=1)
        books = self.db.get_books()
        assert len(books) == 1
        assert books[0].name == 'Book1'

    def test_add_customer(self):
        self.db.add_customer(name='Customer1', city='City1', age=30)
        customers = self.db.get_customers()
        assert len(customers) == 1
        assert customers[0].name == 'Customer1'

    def test_add_loan(self):
        self.db.add_book(name='Book2', author='Author2', year_published=2019, book_type=2)
        self.db.add_customer(name='Customer2', city='City2', age=25)
        due_date, loan_id = self.db.add_loan(cust_id=2, book_id=2, loan_date=datetime.now())
        assert isinstance(due_date, datetime)
        assert isinstance(loan_id, int)

    def teardown_method(self):
        self.db.session.query(Book).delete()
        self.db.session.query(Customer).delete()
        self.db.session.query(Loan).delete()
        self.db.session.commit()


if __name__ == '__main__':
    db = BooksDB()

    db.add_book(name='Book1', author='Author1', year_published=2020, book_type=1)
    db.add_book(name='Book2', author='Author2', year_published=2019, book_type=2)
    db.add_customer(name='Customer1', city='City1', age=30)
    db.add_customer(name='Customer2', city='City2', age=25)

    due_date1, loan_id1 = db.add_loan(cust_id=1, book_id=1, loan_date=datetime.now())
    due_date2, loan_id2 = db.add_loan(cust_id=2, book_id=2, loan_date=datetime.now())

    db.return_loan(loan_id1)

    books = db.get_books()
    customers = db.get_customers()

    print('Books:')
    for book in books:
        print(book.name)

    print('Customers:')
    for customer in customers:
        print(customer.name)

    print('Loans:')
    loans = db.session.query(Loan).all()
    for loan in loans:
        print(f'CustId: {loan.cust_id}, BookId: {loan.book_id}, LoanDate: {loan.loan_date}, ReturnDate: {loan.return_date}')