from flask import render_template, request, Blueprint, abort
import logging
from jinja2 import TemplateNotFound
from main.forms import Contact

main = Blueprint('main', __name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('error.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
# dummy data
articles = ["chess", "backgammon", "snake"]


@main.route("/")
@main.route("/home")
def home():
    return render_template('index.html')


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/contact", methods=['GET','POST'])
def contact():
    contact = Contact()
    return render_template('contact.html', form=contact)


@main.route("/machine-learning", methods=['GET', 'POST'])
def machine():
    return render_template('section.html', title='Machine Learning')


@main.route("/python-basics", methods=['GET', 'POST'])
def basics():
    if request.method == 'POST':
        logger.info('POST REQUEST: PYTHON BASICS')
        for article in articles:
            if request.form['view'] == article:
                render = 'articles/' + article + ".html"
                logger.info('Article requested: {}. File Provided: {}'.format(article, render))
                try:
                    return render_template(render, title=article)
                except TemplateNotFound as err:
                    logger.exception("Article Requested: {} does not exist".format(render))
                    # todo email error log to sys admin
                    abort(404)

    return render_template('section.html', title='Machine Learning')


@main.route("/flask-web-dev", methods=['GET', 'POST'])
def webdev():
    return render_template('flask-web-dev.html', title='Flash Web Development')
