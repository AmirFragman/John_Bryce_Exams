import json
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
# CORS(app)
db = SQLAlchemy(app)
 
# model
class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))
 
    def __init__(self, name, city, addr,pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin


@app.route('/')
def index():
    return render_template("index.html")

# views
@app.route('/showall')
def show_all():
    # res=[]
    # for student in students.query.all():
    #     res.append({"addr":student.addr,"city":student.city,"id":student.id,"name":student.name,"pin":student.pin})
    # return  (json.dumps(res))
    return render_template("showAll.html",res =students.query.all())
   
 
@app.route('/add', methods = ['GET', 'POST'])
def new():
    if request.method == 'POST':
        # city = request.json["city"]

        data = request.get_json()
        city = data["city"]
        name= data["name"]
        addr= data["addr"]
        pin= data["pin"]
        print(pin)
        newStudent= students(name,city,addr,pin)
        db.session.add (newStudent)
        db.session.commit()
        return "a new rcord was create"
    # return "test"
    return render_template("showAll.html",res =students.query.all(),msg="")


@app.route('/del/<id>', methods = ['DELETE'])
@app.route('/del/', methods = ['DELETE'])
def delete(id=-1):
    del_row = students.query.filter_by(id=id).first()
    if del_row:
        db.session.delete(del_row)
        db.session.commit()
        return "a row was delete"
    return "no such student...."    
   


@app.route('/upd/<id>', methods = ['PUT'])
@app.route('/upd/', methods = ['PUT'])
def update_stu(id=-1):
    request_data = request.get_json()
    upd_row = students.query.filter_by(id=id).first()
    if upd_row:
        upd_row.city =request_data['city']
        upd_row.name =request_data["name"]
        upd_row.addr =request_data["addr"]
        upd_row.pin =request_data["pin"]
        db.session.commit()
        return "a row was update"
    return "no such student...."
   




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)


