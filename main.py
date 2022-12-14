# Press Shift+F10 to execute it or replace it with your code.
# Press Ctrl+F8 to toggle the breakpoint.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask, request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


app.config.update(
    SECRET_KEY='topsecret',
    #SQLALCHEMY_DATABASE_URI='<database>://<user_id>:<password>@<server>/<database_name>',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:Spyro979@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)

@app.route('/index')  # homepage
@app.route('/')  # homepage
def hello_flask():
    return 'Hello flask!'


@app.route('/new/')
def query_strings(greeting='hello!'):
    query_val = request.args.get('greeting', greeting)  # tomo el query value del string que pone el user
    return '<h1> the greeting is: {0} </h1>'.format(query_val)  # lo muestro


# no query strings
@app.route('/user')
@app.route('/user/<name>')
def no_query_strings(name='mina'):
    return '<h1> hello there ! {} </h1>'.format(name)


# STRINGS
@app.route('/test/<string:name>')
def working_with_strings(name):
    return '<h1> here is a string: ' + name + '</h1>'


# NUMBERS
@app.route('/numbers/<int:num>')
def working_with_numbers(num):
    return '<h1> the number you pick is: ' + str(num) + '</h1>'

# NUMBERS
@app.route('/add/<int:num1>/<int:num2>')
def adding_integers(num1, num2):
    return '<h1> the sum is: {}'.format(num1 + num2) + '</h1>'


# FLOATS
@app.route('/product/<float:num1>/<float:num2>')
def product_two_numbers(num2, num1):
    return '<h1> the product is: {}'.format(num2 + num1) + '</h1>'

# USING TEMPLATES
@app.route('/temp')
def using_templates():
    return render_template('hello.html')

@app.route('/watch')
def top_movies():
    movie_list = ['autopsy of jane doe',
                  'neon demon',
                  'ghost in a shell',
                  'kong: skull island',
                  'john wick 2',
                  'spiderman - homecoming']
    return render_template('movies.html',
                           movies=movie_list,
                           name='Harry'
                           )

@app.route('/tables')
def movies_plus():
    movie_list = {'autopsy of jane doe': 02.14,
                  'neon demon': 3.20,
                  'ghost in a shell:': 1.50,
                  'kong: skull island': 3.50,
                  'john wick 2': 02.52,
                  'spiderman - homecoming': 1.48}
    return render_template('table_data.html',
                           movies=movie_list,
                           name='Sally'
                           )

@app.route('/filters')
def filter_data():
    movie_dict = {'autopsy of jane doe': 02.14,
                  'neon demon': 3.20,
                  'ghost in a shell:': 1.50,
                  'kong: skull island': 3.50,
                  'john wick 2': 02.52,
                  'spiderman - homecoming': 1.48}
    return render_template('filter_data.html',
                           movies=movie_dict,
                           name=None,
                           film='a christmas carol'
                           )

@app.route('/macros')
def jinja_macros():
    movie_dict = {'autopsy of jane doe': 02.14,
                  'neon demon': 3.20,
                  'ghost in a shell:': 1.50,
                  'kong: skull island': 3.50,
                  'john wick 2': 02.52,
                  'spiderman - homecoming': 1.48}
    return render_template('using_macros.html',
                           movies=movie_dict,
                           )


# class Publication(db.Model):
#     __tablename__ = "publication"
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#
#     def __init__(self, id, name):
#         self.id = id
#         self.name = name
#
#     def __repr__(self):
#         return "The id is {}, Name is {}".format(self.id, self.name)

class Publication(db.Model):
    __tablename__ = "publication"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Publisher is {}".format(self.name)


class Book(db.Model):
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    # Relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
