"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file, send_from_directory
import os
from werkzeug.utils import secure_filename
from app.forms import MovieForm
from app.models import Movie
from flask_wtf.csrf import generate_csrf


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/movies', methods=['POST'])
def movies():
    form = MovieForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        poster = form.poster.data

        # Save the movie to the database
        movie = Movie(title=title, description=description, poster=poster)
        db.session.add(movie)
        db.session.commit()

        # Save the file to an uploads folder (assuming the poster is a file upload)
        poster_filename = secure_filename(poster.filename)
        poster.save(os.path.join(app.config['UPLOAD_FOLDER'], poster_filename))

        # Return success message and movie details in JSON format
        response_data = {
            "message": "Movie Successfully added",
            "title": movie.title,
            "poster": poster_filename,
            "description": movie.description
        }
        return jsonify(response_data), 201
    else:
        # Return validation errors in JSON format
        errors = form_errors(form)
        response_data = {"errors": errors}
        return jsonify(response_data), 400
    
@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
 return jsonify({'csrf_token': generate_csrf()})

@app.route("/api/v1/movies", methods=['GET'])
def add_movies():
    if request.method == 'GET':
        moveies_all=Movie.query.all()
        movies_lst =[]
        for m in moveies_all:
            movies={
                "id": m.id,
                "title": m.title,
                "description": m.description,
                "poster": "/api/v1/posters/"+ m.poster
            }
            movies_lst.append(movies)
        return jsonify({'movies': movies_lst})
    

@app.route("/api/v1/posters/<filename>", methods=['GET'])
def get_movieposter(filename):
    return send_from_directory(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER']), filename)
    

def get_uploaded_images():
    import os
    rootdir = os.getcwd()
    fileslst = []
    for subdir, dirs, files in os.walk(rootdir + '/uploads'):
        for file in files:
            #print os.path.join(subdir, file)
            fileslst.append(file)
    return fileslst
###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404