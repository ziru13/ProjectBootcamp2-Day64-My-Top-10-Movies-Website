from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# TODO 1-1. Create an SQLite database with SQLAlchmey
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie_collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ---------------------------------------------------Part 1 ------------------------------------------------------- 
# TODO 1-2. Create a "Movie" Table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)


# TODO 1-3. 3.0 version needs this active flask application context
with app.app_context():
    db.create_all()


# TODO 1-4. Add a entry for the "Movie" Table for each new movie
# After adding the new_movie the code needs to be commented out/deleted.
# So you are not trying to add the same movie twice.
# new_movie = Movie(
#     title='Phone Booth',
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review='My favourite character was the caller.',
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# with app.app_context():
#     db.session.add(new_movie)
#     db.session.commit()
# ---------------------------------------------------Part 1 -------------------------------------------------------
# ---------------------------------------------------Part 2 -------------------------------------------------------
# Be Able to Edit a Movie's Rating and Review with WTForms to create the RateMovieForm
# TODO 2-1. Use what you have learnt about WTForms to create the RateMovieForm
class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out Of 10 e.g.7.5")
    review = StringField("Your Review")
    submit = SubmitField("DONE")


# TODO 2-2 Use this to create a Quick Form to be rendered in edit.html.
@app.route('/edit', methods=["GET", "POST"])
def rate_movie():
    form = RateMovieForm()
    movie_id = request.form.get("id")
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commmit()
        return redirect(url_for("home"))
    return render_template("edit.html", movie=movie, form=form)
# ---------------------------------------------------Part 2 -------------------------------------------------------


# ---------------------------------------------------Part 3 -------------------------------------------------------
# TODO 3. Delete Movies from the Database
@app.route("/delete")
def delete_movie():
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("home"))
# ---------------------------------------------------Part 3 -------------------------------------------------------


# ---------------------------------------------------Part 4 -------------------------------------------------------
# TODO 4-1: Create a AddMovieForm for adding new movie
class AddMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


# TODO 4-2: Add the "add_movie" entry
@app.route("/add", methods=["Get", "POST"])
def add_movie():
    form = AddMovieForm()
    return render_template("add.html", form=form)


# ---------------------------------------------------Part 4 -------------------------------------------------------


@app.route("/")
def home():
    all_movies = Movie.query.all()
    return render_template("index.html", movies=all_movies)


if __name__ == '__main__':
    app.run(debug=True)


# @app.route("/add", methods=["Get", "POST"])
# def add_movie():
#     if request.method == "POST":
#         title = request.form.get("title")
#         year = request.form.get("year")
#         description = request.form.get("description")
#         rating = request.form.get("rating")
#         ranking = request.form.get("ranking")
#         review = request.form.get("review")
#         img_url = request.form.get("img_url")
# 
#         new_movie = Movie(title=title,
#                           year=year,
#                           description=description,
#                           rating=rating,
#                           ranking=ranking,
#                           review=review,
#                           img_url=img_url)
#         with app.app_context():
#             db.session.add(new_movie)
#             db.session.commit()
#             return redirect(url_for("home"))
#     return render_template("add.html")