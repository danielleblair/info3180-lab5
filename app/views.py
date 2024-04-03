import os
from app import app, db
from flask import render_template, request, jsonify, send_file, redirect, url_for, flash, session, abort, send_from_directory
from werkzeug.utils import secure_filename
from app.models import Movie
from app.forms import MovieForm
from flask_wtf.csrf import generate_csrf


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")



@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route('/api/v1/movies', methods=['POST'])
def movies():
    """displaying the form to add a new movie."""
    mform = MovieForm()

    if mform.validate_on_submit():

        p_title = mform.title.data
        p_description = mform.description.data

        p_poster = mform.poster.data

        filename = secure_filename(p_poster.filename)
        p_poster.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        movie = Movie(title= p_title, description=p_description, poster=filename)
        db.session.add(movie)
        db.session.commit()

        flash('Movie Created and Saved', 'success')
        return jsonify({
                "message": "Movie Successfully added",
                "title": movie.title,
                "poster": movie.poster,
                "description": movie.description
        })

    else:
        return jsonify({'errors': form_errors(mform)})
    
@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


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

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
