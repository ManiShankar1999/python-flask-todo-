import logging
from model.model import table, db
from flask import Flask, render_template, url_for, request, redirect

logging.basicConfig(filename="log.csv", 
					format='%(asctime)s,%(levelname)s,%(message)s', datefmt='%d-%b-%y %H:%M:%S' ,
					filemode='+w')
logger=logging.getLogger() 

#Now we are going to Set the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG)

class NoHealth(logging.Filter):
    def filter(self, record):
        return 'GET /' not  in record.getMessage()

        

class NoHealth1(logging.Filter):
    def filter(self, record):
        return 'POST /' not in record.getMessage()

logging.getLogger("werkzeug").addFilter(NoHealth1())
logging.getLogger("werkzeug").addFilter(NoHealth())

def read():
        tasks = table.query.order_by(table.date_created).all()
        return render_template('index.html', tasks=tasks)

def create():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = table(content=task_content)
        db.session.add(new_task)
        db.session.commit()
        logger.debug("{},{} ".format('task added',(new_task)))
        return redirect('/')
    else:
        return 'There was an issue adding your task'


def delete(id):
    task_to_delete=table.query.get_or_404(id)


    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        logger.debug("{},{} ".format('task deleted',(task_to_delete)))
        return redirect('/')
    except:
        return 'There was an issue while deleting your task'


def update(id):
    task=table.query.get_or_404(id)
    if request.method == 'POST':
        task.content=request.form['content']
    else:
        return render_template('update.html',task=task)

    try:
        db.session.commit()
        logger.debug("{},{} ".format('updated added',(task)))       
        return redirect('/')
    except:
        return 'There was an issue while updating your task'