from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key ="Secret"
Bootstrap(app)

app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Art(db.Model):
    id = db.Column('art_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(10000))
    price = db.Column(db.Float)
    image = db.Column(db.LargeBinary)

def __init__(self, name, price):
    self.name = name
    self.price = price

# db.create_all()

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

new_art = Art(id=1, name="Miss Spring", description="A painting of Miss Spring, aquarell and paper items", price=24.50, image=convertToBinaryData('static/images/painting.jpg'))
db.session.add(new_art)
db.session.commit()

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)