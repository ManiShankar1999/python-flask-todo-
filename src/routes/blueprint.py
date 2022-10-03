from flask import Blueprint
from controller.controller import create, update, delete ,read

blueprint = Blueprint('blueprint', __name__)
blueprint.route('/')(read)
blueprint.route('/', methods=['POST', 'GET'])(create)
blueprint.route('/delete/<int:id>')(delete)
blueprint.route('/update/<int:id>', methods=['POST','GET'])(update)