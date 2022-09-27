from distutils.command.build_scripts import first_line_re
from asyncio import tasks
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from flask.logging import logging
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(filename="log.csv", 
					format='%(asctime)s,%(levelname)s,%(funcName)s,%(message)s', datefmt='%d-%b-%y %H:%M:%S' ,
					filemode='+w')


class NoHealth(logging.Filter):
    def filter(self, record):
        return 'GET /' not  in record.getMessage()

        

class NoHealth1(logging.Filter):
    def filter(self, record):
        return 'POST /' not in record.getMessage()

logging.getLogger("werkzeug").addFilter(NoHealth1())
logging.getLogger("werkzeug").addFilter(NoHealth())
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '%r' % self.id

class controller():
    @app.before_first_request
    def create_tables():
        db.create_all()

    @app.route('/')
    def read():
            tasks = Model.query.order_by(Model.date_created).all()
            return render_template('index.html', tasks=tasks)

    @app.route('/', methods=['POST', 'GET'])
    def create():
        if request.method == 'POST':
            task_content = request.form['content']
            new_task = Model(content=task_content)
            db.session.add(new_task)
            db.session.commit()
            app.logger.debug("{},{} ".format('task added',(new_task)))
            return redirect('/')
        else:
            return 'There was an issue adding your task'

    @app.route('/delete/<int:id>')
    def delete(id):
        task_to_delete=Model.query.get_or_404(id)


        try:
            db.session.delete(task_to_delete)
            db.session.commit()
            app.logger.debug("{},{} ".format('task deleted',(task_to_delete)))
            return redirect('/')
        except:
            return 'There was an issue while deleting your task'

    @app.route('/update/<int:id>', methods=['POST','GET'])
    def update(id):
        task=Model.query.get_or_404(id)
        if request.method == 'POST':
            task.content=request.form['content']
        else:
            return render_template('update.html',task=task)

        try:
            db.session.commit()
            app.logger.debug("{},{} ".format('updated added',(task)))       
            return redirect('/')
        except:
            return 'There was an issue while updating your task'
if __name__=="__main__":
    app.run(debug=True,host='127.0.0.1')