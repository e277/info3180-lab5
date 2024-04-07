"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from app.forms import Movieform
from app.models import Movie
from flask import render_template, request, jsonify, send_file, url_for, send_from_directory
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import secure_filename
import os


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")



@app.route('/api/v1/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'POST': 
        form = Movieform()
        if form.validate_on_submit():
            title = form.title.data
            description = form.description.data
            poster = form.poster.data
            
            filename = secure_filename(poster.filename)
            poster.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            movie = Movie(title=title, description=description, poster=filename)
            db.session.add(movie)
            db.session.commit()

            movie = {
                'title': title,
                'description': description,
                'poster': filename,
            }
            return jsonify(message="Movie added successfully", movie=movie), 201
        else:
            return jsonify(errors=form_errors(form)), 400
    elif request.method == 'GET':
        movies = Movie.query.all()
        posters = get_uploaded_posters()
        movies_list = []
        for movie in movies:
            if movie.poster in posters:
                movie.poster = url_for('uploaded_poster', poster=movie.poster)
            
            movies_list.append({
                'id': movie.id,
                'title': movie.title,
                'description': movie.description,
                'poster': movie.poster,
            })
        return jsonify(movies=movies_list), 200


@app.route('/uploads/<poster>')
def uploaded_poster(poster):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), poster)

def get_uploaded_posters():
    rootdir = os.getcwd()
    # print(rootdir)
    image_list = []
    for subdir, dirs, files in os.walk(os.path.join(rootdir, app.config['UPLOAD_FOLDER'])):
        for file in files:
            # print(os.path.join(subdir, file))
            if file.endswith(('.jpg', '.png', '.jpeg')):
                full_path = os.path.join(subdir, file)
                relative_path = os.path.relpath(full_path, os.path.join(rootdir, app.config['UPLOAD_FOLDER']))
                image_list.append(relative_path)
    return image_list

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()}), 200



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
