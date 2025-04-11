from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy import String, Integer , Float

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False


all_books = []


db = SQLAlchemy(app)


class Library(db.Model):
    __tablename__="library"

    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    title : Mapped[str] = mapped_column(String(40),unique=True,nullable=True)
    author : Mapped[str] = mapped_column(String(50),unique=False,nullable=True)
    rating : Mapped[float]=mapped_column(Float,unique=False,nullable=True)



@app.route('/')
def home():
    all_books = Library.query.all()
    return render_template("index.html",all_books=all_books)


@app.route("/add",methods=["POST","GET"])
def add():
    if request.method == "POST":
        new_books= {
            "title": request.form["book_name"],
            "author": request.form["author_name"],
            "rating":request.form["rating"]
        }
        all_books.append(new_books)
        print(new_books)

        title = request.form.get("book_name")
        author = request.form.get("author_name")
        rating = request.form.get("rating")

        entry = Library(title=title,author=author,rating=rating)
        db.session.add(entry)
        db.session.commit()

        return redirect(url_for("home",all_books=all_books))


    return render_template("add.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

