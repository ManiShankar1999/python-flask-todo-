from flask import Flask, render_template, url_for, request, redirect
from flask_migrate import Migrate
from routes.blueprint import blueprint
from model.model import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(blueprint, url_prefix='/')

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True,host='127.0.0.1',port=5000)