# Core packages
import os
import re

# External packages
import flask

# Local packages
import routing


app = flask.Flask(__name__)

permanent_redirect_map = routing.UrlMap("permanent-redirects.yaml")
redirect_map = routing.UrlMap("redirects.yaml")


@app.before_request
def apply_redirects():
    """
    Process the two mappings defined above
    of permanent and temporary redirects to target URLs,
    to send the appropriate redirect responses
    """

    permanent_redirect_url = permanent_redirect_map.get_target(
        flask.request.path
    )
    if permanent_redirect_url:
        return flask.redirect(permanent_redirect_url, code=301)

    redirect_url = redirect_map.get_target(flask.request.path)
    if redirect_url:
        return flask.redirect(redirect_url)


@app.before_request
def find_file_or_redirect():
    """
    If a file doesn't exist at the requested path, see if it exists at one
    of the other paths, and redirect there if necessary
    """

    request_path = flask.request.path

    url_match = re.match(r'^(|.*[^/])(/(index(.html)?)?)?$', request_path)
    minimal_url = url_match.group(1)
    directory_url = minimal_url + '/'
    filepath = minimal_url + '.html'
    index_filepath = directory_url + 'index.html'
    file_exists = os.path.isfile(app.template_folder + filepath)
    index_exists = os.path.isfile(app.template_folder + index_filepath)

    if request_path == minimal_url:
        if file_exists:
            return flask.render_template(filepath)
        elif index_exists:
            return flask.redirect(app.template_folder + directory_url)

    if request_path == directory_url:
        if index_exists:
            return flask.render_template(index_filepath)
        elif file_exists:
            return flask.redirect(app.template_folder + minimal_url)

    if request_path > directory_url and index_exists:
        return flask.redirect(app.template_folder + directory_url)


@app.route('/')
@app.route('/place/two')
@app.route('/place/one')
def homepage():
    return "Hello world"
