from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:passowrd@localhost:3306/数据库名称'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()

class Student(db.Model):

    s_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    s_name = db.Column(db.String(20), unique=True)
    s_age = db.Column(db.Integer, default=18)

    __tablename__ = 'student'


    def __init__(self, name, age):
        self.s_name = name
        self.s_age = age

SQLAlchemy(app=app)