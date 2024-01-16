from flask import Flask, request, render_template, redirect, url_for
from flask_alembic import Alembic
from func import Readers, Books, db, get_books
from app import app
import datetime

@app.route("/")
def index():
    with app.app_context():
        db.create_all()
        if Books.query.count() == 0:
            get_books()
    books = Books.query.all()
    return render_template("index.html", books=books)

@app.route("/borrow_book", methods=["POST"])
def borrow_book():
    book_id = request.form.get("book_id")
    reader_fullname = request.form.get("reader_fullname")
    if book_id and reader_fullname:
        book = Books.query.get(book_id)
        reader = Readers.query.filter_by(fullname=reader_fullname).first()
        if book and not book.is_borrowed and reader:
            book.is_borrowed = True
            book.borrowed_at = datetime.datetime.now().date()
            book.return_by = book.borrowed_at + datetime.timedelta(days=30)
            book.reader_id = reader.id
            db.session.commit()
    return redirect(url_for("readers_page"))


@app.route("/return_book", methods=["POST"])
def return_book():
    book_id = request.form.get("book_id")
    reader_fullname = request.form.get("reader_fullname")
    if book_id and reader_fullname:
        book = Books.query.get(book_id)
        reader = Readers.query.filter_by(fullname=reader_fullname).first()
        if book and book.is_borrowed and reader and book.reader_id == reader.id:
            book.is_borrowed = False
            book.return_by = book.borrowed_at + datetime.timedelta(days=30)
            book.reader_id = None
            db.session.commit()
    return redirect(url_for("readers_page"))


@app.route("/readers.html", methods=["GET"])
def readers_page():
    readers = Readers.query.all()
    books = Books.query.all()
    return render_template("readers.html", readers=readers, books=books)

@app.route("/add_reader", methods=["POST"])
def add_reader():
    fullname = request.form.get("fullname")
    if fullname:
        new_reader = Readers(fullname=fullname)
        db.session.add(new_reader)
        db.session.commit()
    return redirect("/readers.html")


alembic = Alembic()
alembic.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
