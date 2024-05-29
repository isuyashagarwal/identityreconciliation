from flask import render_template, request, Blueprint,jsonify
from flask_cors import CORS, cross_origin
from core.models import *

main = Blueprint('main', __name__)

@main.route("/",methods=['GET','POST'])
@cross_origin()
def home():
    return render_template('index.html')


@main.route('/identity',methods=['POST'])
@cross_origin()
def identity():
    data = request.json
    email = data.get('email')
    phone_number = data.get('phoneNumber')

    new_contact = create_contact(email,phone_number)

    return jsonify({"status":"added contact"})


def create_contact(email=None, phoneNumber=None,linkedId=None,link_precedence="primary"):
    new_contact = Contact(
        phoneNumber=phoneNumber,
        email=email,
        linkedId=linkedId,
        linkPrecedence=link_precedence,
    )
    db.session.add(new_contact)
    db.session.commit()
    return new_contact
