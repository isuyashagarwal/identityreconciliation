from flask import render_template, request, Blueprint,jsonify
from flask_cors import CORS, cross_origin
from core.models import *

main = Blueprint('main', __name__)

@main.route('/identity',methods=['POST'])
@cross_origin()
def identity():
    data = request.json
    email = data.get('email')
    phone_number = data.get('phoneNumber')

    if email and phone_number:
        contact = db.session.query(Contact).filter((Contact.phoneNumber == phone_number) | (Contact.email == email)).first()
    elif email:
        contact = Contact.query.filter_by(email=email).first()
    elif phone_number:
        contact = Contact.query.filter_by(phoneNumber=phone_number).first()
    else:
        return jsonify({"response": "null"})

    #Create a new contact if nothing exists
    if not contact:
        primary_contact = create_contact(email=email,phoneNumber=phone_number,linkedId=None,linkPrecedence='primary')
        secondary_contacts = []

    #If a contact exists, then find the primary contact
    else:
        primary_contact = None
        if contact.linkPrecedence == "primary":
            primary_contact = contact

        else:
            primary_contact = Contact.query.filter_by(id=contact.linkedId).first()

        #Find all secondary_contacts linked to the primary contact
        secondary_contacts = Contact.query.filter_by(linkedId = primary_contact.id).all()

        # A primary contact can turn into a secondary contact if an existing primary contact has it's number changed to a number that
        # already exists as a secondary contact

        if primary_contact.email == email and primary_contact.phoneNumber != phone_number:
            secondary_contacts = Contact.query.filter_by(phoneNumber = phone_number).all()
            for contact in secondary_contacts:
                contact.linkedId = primary_contact.id
                db.session.commit()

        else:

            ##Check if the given email and phone numbers exist in database in a single record. If not, create a secondary contact
            if email and phone_number and (primary_contact.email != email or primary_contact.phoneNumber != phone_number):
                existing_contact = None
                for contact in secondary_contacts:
                    if contact.email == email and contact.phoneNumber == phone_number:
                        existing_contact = contact
                        break

                if not existing_contact:
                    new_secondary_contact = create_contact(email=email, phoneNumber=phone_number,linkedId=primary_contact.id, linkPrecedence='secondary')
                    secondary_contacts.append(new_secondary_contact)

    # Construct response
    response = {
        "contact": {
            "primaryContactId": primary_contact.id,
            "emails": list(set([primary_contact.email] + [contact.email for contact in secondary_contacts if contact.email])),
            "phoneNumbers": list(set([primary_contact.phoneNumber] + [contact.phoneNumber for contact in secondary_contacts if contact.phoneNumber])),
            "secondaryContactIds": [contact.id for contact in secondary_contacts]
        }
    }

    return jsonify(response)

def create_contact(email=None, phoneNumber=None,linkedId=None,linkPrecedence="primary"):
    if email and phoneNumber:
        new_contact = Contact(
            phoneNumber=phoneNumber,
            email=email,
            linkedId=linkedId,
            linkPrecedence=linkPrecedence,
        )
        db.session.add(new_contact)
        db.session.commit()
        return new_contact
    else:
        pass
