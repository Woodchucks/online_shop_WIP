from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os
from base64 import b64encode
import io
from PIL import Image
import requests
import sqlite3

app = Flask(__name__)
app.secret_key ="Secret"
Bootstrap(app)

app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Art(db.Model):
    id = db.Column('art_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(10000))
    price = db.Column(db.Float)
    image = db.Column(db.LargeBinary)
    # image_url = db.Column(db.String(1000))

def __init__(self, name, price):
    self.name = name
    self.price = price

# db.create_all()

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

# new_art = Art(id=1, name="Miss Spring", description="A painting of Miss Spring, aquarell and paper items", price=24.50, image=convertToBinaryData('static/images/painting.jpg'))
# new_art_2 = Art(name="Rabbit Home", description="Family of Rabbits", price=32.80, image=convertToBinaryData('static/images/painting.jpg'))
# new_art_3 = Art(name="Heart", description="A big, red heart", price=20, image=convertToBinaryData('static/images/painting.jpg'))
# new_art_4 = Art(name="Power of Friendship", description="A carton model of two people holding hands", price=28.50, image=convertToBinaryData('static/images/painting.jpg'))
# db.session.add(new_art)
# db.session.add(new_art_2)
# db.session.add(new_art_3)
# db.session.add(new_art_4)
# db.session.commit()

@app.route('/')
@app.route('/index')
def home():
    # arts = Art.query.all()
    # ARTS_FOLDER = os.path.join('static', 'images')
    #
    # app = Flask(__name__)
    # app.config['UPLOAD_FOLDER'] = ARTS_FOLDER
    #
    # full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'painting.jpg')
    # return render_template("index.html", arts=arts, image=full_filename)

    def convert_blob_to_img(data, file_name):
        with open(file_name, 'wb') as file:
            file.write(data)

    ARTS_FOLDER = os.path.join('static', 'images')
    app.config['UPLOAD_FOLDER'] = ARTS_FOLDER
    arts = Art.query.all()

    try:
        images_filenames = []
        connection = sqlite3.connect('arts.db')
        query = "SELECT * FROM art"
        cursor = connection.cursor()
        cursor.execute(query)
        art_records = cursor.fetchall()
        for art in art_records:
            name = art[1]
            image = art[4]
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], f'{name}.jpg')
            images_filenames.append(full_filename)
            convert_blob_to_img(image, full_filename)
        if len(art_records) == 0:
            print("Database empty. Please insert data before using.")

    except sqlite3.Error as error:
        print(format(error))

    finally:
        if connection:
            connection.close()

    return render_template("index.html", arts=arts, images=images_filenames)


@app.route('/details/<int:id>')
def details(id):
    return render_template('details.html', art_id=id)

@app.route('/details/<int:id>/image')
def art_image(id):
    art = Art.query.get_or_404(id)
    return app.response_class(art.image_url, mimetype='application/octet-stream')

if __name__ == '__main__':
    app.run(debug=True)