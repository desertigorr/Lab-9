import flask
import sqlalchemy.sql
from flask_sqlalchemy import SQLAlchemy


app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:8000@localhost/db'
db = SQLAlchemy(app)


class Review(db.Model):
    post_id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(512), nullable=False)
    rate = db.Column(db.Integer(), nullable=False)


# Рендер страницы
@app.route('/', methods=['GET'])
def render():
    return flask.render_template('index.html', review=Review.query.all())

# Добавление отзыва
@app.route('/add_review', methods=['POST'])
def add_review():
    post_id = flask.request.form['id']
    text = flask.request.form['text']
    rate = flask.request.form['rate']
    if text not in Review.query.all():
        db.session.add(Review(post_id=post_id, text=text, rate=rate))
        db.session.commit()
    else:
        print('Err')
    return flask.redirect(flask.url_for('render'))


# Очистка
@app.route('/clear', methods=['POST'])
def clear():
    db.session.execute(sqlalchemy.sql.text('clear'))
    db.session.commit()
    return flask.redirect(flask.url_for('render'))


with app.app_context():
    db.create_all()
app.run()