from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from datetime import datetime
from models import db, Booking, AvailableBookings, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning
CORS(app, resources={r"/api/*": {"origins": "*"}})
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/setAvailableBookings', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def setAvailableBookings():
    data = request.get_json()
    location = data['location']
    date = data['date']
    time = data['time']
    availableBooking = AvailableBookings(location=location, date=date, time=time)
    if not location or not date or not time:
        return jsonify({'message': 'Missing Data'})

    alreadyExistsAvailable = AvailableBookings.query.filter_by(date=date, time=time, location=location).first()
    if alreadyExistsAvailable:
        return jsonify({'message': 'Booking already exists'})

    alreadyExistsBooking = Booking.query.filter_by(date=date, time=time, location=location).first()
    if alreadyExistsBooking:
        return jsonify({'message': 'Booking already exists'})

    db.session.add(availableBooking)
    db.session.commit()
    return jsonify({'message': 'Available Booking Created'})

@app.route('/getAvailableBookings', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getAvailableBookings():
    availableBookings = AvailableBookings.query.all()
    output = []
    for availableBooking in availableBookings:
        availableBooking_data = {}
        availableBooking_data['location'] = availableBooking.location
        availableBooking_data['date'] = availableBooking.date
        availableBooking_data['time'] = availableBooking.time
        output.append(availableBooking_data)
    return jsonify({'availableBookings': output})

@app.route('/setBooking', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def setBooking():
    data = request.get_json()
    name = data['name']
    email = data['email']
    phone_number = data['phoneNumber']
    date = data['date']
    time = data['time']
    location = data['location']

    if not name or not email or not date or not time or not location:
        return jsonify({'message': 'Missing Data'}),412
    
    booking = Booking.query.filter_by(date=date, time=time, location=location).first()
    if booking:
        return jsonify({'message': 'Booking already exists'}), 409
    availableBooking = AvailableBookings.query.filter_by(date=date, time=time, location=location).first()
    if not availableBooking:
        return jsonify({'message': 'Booking not available'}),400

    booking = Booking(name=name, email=email, phone_number=phone_number, date=date, time=time, location=location)
    db.session.add(booking)

    db.session.delete(availableBooking)
    db.session.commit()
    return jsonify({'message': 'Booking Created'})

@app.route('/getCraigmillarBookings', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getCraigmillarBookings():
    bookings = Booking.query.filter_by(location='Craigmillar').all()
    output = []
    for booking in bookings:
        booking_data = {}
        booking_data['name'] = booking.name
        booking_data['email'] = booking.email
        booking_data['phone_number'] = booking.phone_number
        booking_data['date'] = booking.date
        booking_data['time'] = booking.time
        booking_data['location'] = booking.location
        output.append(booking_data)
    return jsonify({'bookings': output})

@app.route('/getMusselburghBookings', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getMusselburghBookings():
    bookings = Booking.query.filter_by(location='Musselburgh').all()
    output = []
    for booking in bookings:
        booking_data = {}
        booking_data['name'] = booking.name
        booking_data['email'] = booking.email
        booking_data['phone_number'] = booking.phone_number
        booking_data['date'] = booking.date
        booking_data['time'] = booking.time
        booking_data['location'] = booking.location
        output.append(booking_data)
    return jsonify({'bookings': output})

@app.route('/getSuggestedBookings', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getSuggestedBookings():
    available_bookings = AvailableBookings.query.order_by(AvailableBookings.date.desc()).all()
    output = []
    count = 0
    for booking in available_bookings:
        if count == 3:
            break
        count += 1
        booking_data = {}
        booking_data['date'] = booking.date
        booking_data['time'] = booking.time
        booking_data['location'] = booking.location
        output.append(booking_data)
    return jsonify({'bookings': output})

@app.route('/getAvailableBookingOnDayAtLocation', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getAvailableBookingOnDay():
    date = request.args.get('date')
    location = request.args.get('location')
    available_bookings = AvailableBookings.query.filter_by(date=date, location=location).all()
    output = []
    for booking in available_bookings:
        output.append(booking.time)
    return jsonify({'bookings': output})

@app.route('/removeAvailableBooking', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def removeAvailableBooking():
    data = request.get_json()
    date = data['date']
    time = data['time']
    location = data['location']
    booking = Booking.query.filter_by(date=date, time=time, location=location).first()
    if not booking:
        return jsonify({'message': 'Booking not found'})
    availableBooking = AvailableBookings(location=location, date=date, time=time)
    db.session.add(availableBooking)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Available Booking Removed'})

@app.route('/removeBooking', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def removeBooking():
    name = request.args.get('name')
    email = request.args.get('email')
    date = request.args.get('date')
    time = request.args.get('time')
    location = request.args.get('location')
    booking = Booking.query.filter_by(date=date, time=time, location=location, name=name, email=email).first()
    if not booking:
        return jsonify({'message': 'Booking not found'}), 404
    availableBooking = AvailableBookings(location=location, date=date, time=time)
    db.session.add(availableBooking)
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking Removed'})

@app.route('/getBookings', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getBookings():
    bookings = Booking.query.all()
    output = []
    for booking in bookings:
        booking_data = {}
        booking_data['name'] = booking.name
        booking_data['email'] = booking.email
        booking_data['phone_number'] = booking.phone_number
        booking_data['date'] = booking.date
        booking_data['time'] = booking.time
        booking_data['location'] = booking.location
        output.append(booking_data)
    return jsonify({'bookings': output})

@app.route('/getAvailableDates', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getAvailableDates():
    availableDates = AvailableBookings.query.all()
    output = []
    for date in availableDates:
        if date.date in output:
            continue
        output.append(date.date)

        
    return jsonify({'dates': output})

@app.route('/findBooking', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def findBooking():
    id = request.args.get('id')
    booking = Booking.query.filter_by(id=id).first()
    if not booking:
        return jsonify({'message': 'Booking not found'}), 404
    booking_data = {}
    booking_data['name'] = booking.name
    booking_data['email'] = booking.email
    booking_data['time'] = booking.time
    booking_data['date'] = booking.date
    booking_data['location'] = booking.location
    return jsonify(booking_data)

@app.route('/register', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def register():
    username = request.args.get('username')
    password = request.args.get('password')
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'})








if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

