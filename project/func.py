from flask_sqlalchemy import SQLAlchemy
from app import app
import datetime
import random
import requests
import json

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

class Books(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable=False)
	author = db.Column(db.String(150), nullable=False)
	is_borrowed = db.Column(db.Boolean, default=False)
	reader_id = db.Column(db.Integer, db.ForeignKey("readers.id"))
	borrowed_at = db.Column(db.DateTime)
	return_by = db.Column(db.DateTime)

class Readers(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	fullname = db.Column(db.String(200), nullable=False)
	books = db.relationship("Books", backref="reader", lazy=True)


def get_books(max_results=20):
	genres = ["fantastyka", "kryminał", "romans", "biografia", "historyczna", "naukowa", "horror",
			  "thriller", "dramat", "komedia", "poemat", "bajka", "satyra", "tragedia", "młodzieżowa", "dla dzieci"]
	query = random.choice(genres)
	url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults={max_results}"
	response = requests.get(url)
	data = json.loads(response.text)
	print(data)
	for item in data["items"]:
		title = item["volumeInfo"]["title"]
		authors = ",".join(item["volumeInfo"].get("authors", []))
		book = Books(title=title, author=authors)
		db.session.add(book)
	db.session.commit()


class Reader:
	def __init__(self, fullname):
		self.fullname = fullname
class Book:
	def __init__(self, id, title):
		self.id = id
		self.title = title
		self.borrowed = False
		self.reader = None
		self.borrow_date = None
		self.return_date = None
		self.borrow_history = []

class Library:
	def __init__(self):
		self.books = []
		self.readers = []

	def add_reader(self, fullname):
		self.readers.append(Reader(fullname))

	def borrow_book(self, id, fullname, days=30):
		book = Books.query.get(id)
		if book and not book.reader_id:
			reader = Readers.query.filter_by(fullname=fullname).first()
			if reader:
				book.reader_id = reader.id
				book.borrowed_at = datetime.datetime.now()
				book.return_by = book.borrowed_at + datetime.timedelta(days=days)
				db.session.commit()
				return True
		return False

	def return_book(self, id, fullname):
		book = Books.query.get(id)
		reader = Readers.query.filter_by(fullname=fullname).first()
		if book and book.reader_id == reader.id:
			book.reader_id = None
			book.borrowed_at = None
			book.return_by = None
			db.session.commit()
			return True
		return False

	def display_borrow_history(self, title):
		for book in self.books:
			if book.title == title:
				for history in book.borrow_history:
					print(f"{history[0]} borrowed {title} on {history[1]} and returned on {history[2]}")



