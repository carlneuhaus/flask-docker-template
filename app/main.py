from flask import Blueprint, render_template, request, Response
import ldap

main = Blueprint('main', __name__)

@main.route('/')
def landing():
    return render_template('index.html')

@main.route('/data', methods = ['POST', 'GET'])
def process_request():
    if request.method != 'POST':
        return Response("Method not supported", status=405)
    form_data = request.form
    return render_template('data.html', form_data=form_data)