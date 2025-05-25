import os
import pymysql
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
import mysql.connector
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'key'  # For flash messages and session management

API_URL = 'https://gemini-api-endpoint.com/query'
API_KEY = 'AIzaSyDsfh2f2zJd8pWzLBBhNz9VrBTbAU7bG-4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:koushikkrish@22@localhost/philatelist_db'


# MySQL connection details for Philatelists database
philatelists_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="koushikkrish@22",
    database="philatelists_db"
)

# MySQL connection details for Postal Circles database
postalcircles_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="koushikkrish@22",
    database="postalcircles_db"
)
@app.route('/home')
def home():
    cursor = postalcircles_db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM events ORDER BY date DESC')
    events = cursor.fetchall()
    cursor.close()

    if 'username' in session:
        return render_template('landing.html', events=events, username=session['username'], email=session['email'])
    else:
        return render_template('landing.html', events=events)

@app.route('/myprofile')
def myprofile():
    if 'username' in session:
        return render_template('myprofile.html', username=session['username'], email=session['email'])
    else:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard-1.html', username=session['username'], email=session['email'])
    else:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))
@app.route('/dashboard2')
def dashboard2():
    if 'username' in session:
        return render_template('dashboard-2.html', username=session['username'], email=session['email'])
    else:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))


@app.route('/create-npda')
def create_npda():
    return render_template('create_npda.html')

@app.route('/my-collection')
def my_collection():
    return render_template('my_collection.html')



@app.route('/help-support')
def help_support():
    return render_template('help_support.html')

@app.route('/stamp_store')
def stamp_store():
    return render_template('stamp_store.html')

@app.route('/forums')
def forums():
    return render_template('forums.html')

@app.route('/philately_crash_course')
def philately_crash_course():
    return render_template('philately_crash_course.html')

@app.route('/stamp_mela')
def stamp_mela():
    return render_template('index.html')

@app.route('/stamp_museum')
def stamp_museum():
    return render_template('stamp_museum.html')
@app.route('/pre_book', defaults={'stamp': None})
@app.route('/pre_book/<stamp>')
def pre_book(stamp):
    return render_template('pre_book.html', stamp=stamp)


@app.route('/postal-circle-dashboard')
def postal_circle_dashboard():
    return render_template('dashboard-2.html')



@app.route('/stamps')
def stamps():
    return render_template('stamps.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/settings2')
def settings2():
    return render_template('settings2.html')


# Route for login page
@app.route('/')
@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    session.pop('email', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# Philatelists Login Route
@app.route('/login_philatelists', methods=['POST'])
def login_philatelists():
    username = request.form['username']
    password = request.form['password']

    cursor = philatelists_db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        session['username'] = user[1]  # Adjust index based on your user table structure
        session['email'] = user[2]     # Adjust index based on your user table structure
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))

# Postal Circles Login Route
@app.route('/login_postalcircles', methods=['POST'])
def login_postalcircles():
    postal_circle = request.form['postal_circle']
    username = request.form['username']
    password = request.form['password']

    cursor = postalcircles_db.cursor()
    cursor.execute("SELECT * FROM users WHERE postal_circle = %s AND username = %s AND password = %s", 
                   (postal_circle, username, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        session['username'] = user[1]  # Adjust index based on your user table structure
        session['email'] = user[2]     # Adjust index based on your user table structure
        flash('Login successful!', 'success')
        return redirect(url_for('postal_circle_dashboard'))
    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))

# Route for registration page
@app.route('/register')
def register():
    return render_template('register.html')

# Philatelists Registration Route
@app.route('/register_philatelist', methods=['POST'])
def register_philatelist():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if username and email and password:
        cursor = philatelists_db.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', 
                       (username, email, password))
        philatelists_db.commit()
        cursor.close()
        session['username'] = username
        session['email'] = email
        flash('Philatelist registered successfully!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('All fields are required.', 'error')
        return redirect(url_for('register'))

# Postal Circles Registration Route
@app.route('/register_postalcircle', methods=['POST'])
def register_postalcircle():
    postal_circle = request.form.get('postal_circle')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if postal_circle and username and email and password:
        cursor = postalcircles_db.cursor()
        cursor.execute('INSERT INTO users (postal_circle, username, email, password) VALUES (%s, %s, %s, %s)', 
                       (postal_circle, username, email, password))
        postalcircles_db.commit()
        cursor.close()
        session['username'] = username
        session['email'] = email
        flash('Postal Circle user registered successfully!', 'success')
        return redirect(url_for('postal_circle_dashboard'))
    else:
        flash('All fields are required.', 'error')
        return redirect(url_for('register'))



@app.route('/add_event', methods=['POST'])
def add_event():
    event_name = request.form['eventName']
    event_date = request.form['eventDate']
    event_location = request.form['eventLocation']
    event_description = request.form['eventDescription']

    cursor = postalcircles_db.cursor()
    cursor.execute('INSERT INTO events (name, date, location, description) VALUES (%s, %s, %s, %s)',
                   (event_name, event_date, event_location, event_description))
    postalcircles_db.commit()
    cursor.close()

    return ("event added successfully")
    return redirect(url_for('events'))


# @app.route('/get_events')
# def get_events():
#     cursor = postalcircles_db.cursor(dictionary=True)
#     cursor.execute('SELECT * FROM events ORDER BY date DESC')
#     events = cursor.fetchall()
#     cursor.close()
#     return render_template('landing.html', events=events)

@app.route('/get-events', methods=['GET'])
def get_events():
    cursor = postalcircles_db.cursor()
    cursor.execute("SELECT id, name FROM events")  # Adjust your query based on your table structure
    events = cursor.fetchall()  # Fetch all event records
    cursor.close()

    # Convert the result into a list of dictionaries
    events_list = [{'id': event[0], 'event_name': event[1]} for event in events]

    return jsonify(events_list)  # Return as JSON



@app.route('/update_event', methods=['POST'])
def update_event():
    event_id = request.form['existingEvents']
    event_name = request.form['updateEventName']
    event_date = request.form['updateEventDate']
    event_location = request.form['updateEventLocation']
    event_description = request.form['updateEventDescription']

    cursor = postalcircles_db.cursor()
    cursor.execute('UPDATE events SET name=%s, date=%s, location=%s, description=%s WHERE id=%s',
                   (event_name, event_date, event_location, event_description, event_id))
    postalcircles_db.commit()
    cursor.close()

    flash('Event updated successfully!', 'success')
    return redirect(url_for('events'))

@app.route('/delete_event', methods=['POST'])
def delete_event():
    event_id = request.form.get('eventId')  # Get 'eventId' from the form
    print(f"Received event ID: {event_id}")
    
    if event_id:
        try:
            cursor = postalcircles_db.cursor()
            cursor.execute('DELETE FROM events WHERE id = %s', (event_id,))
            postalcircles_db.commit()
            cursor.close()
            flash('Event deleted successfully.', 'success')
        except Exception as e:
            postalcircles_db.rollback()  # Rollback in case of error
            flash(f'Error deleting event: {str(e)}', 'error')
    else:
        flash('Event ID is missing.', 'warning')

    return redirect(url_for('events'))


@app.route('/update_profile', methods=['POST'])
def update_profile():
    email = request.form['email']
    # Update the email in the database for the current user here
    flash('Profile updated successfully', 'success')
    return redirect(url_for('settings'))

@app.route('/update_password', methods=['POST'])
def update_password():
    current_password = request.form['currentPassword']
    new_password = request.form['newPassword']
    confirm_password = request.form['confirmPassword']

    if new_password == confirm_password:
        # Validate current password and update to new password in the database here
        flash('Password updated successfully', 'success')
    else:
        flash('Passwords do not match', 'error')

    return redirect(url_for('settings'))


# Route to handle chatbot input
@app.route('/ask', methods=['POST'])
def ask_gemini():
    user_message = request.json.get('message')

    # Prepare the request for Gemini API
    payload = {
        'input': user_message,
        'key': API_KEY
    }

    try:
        # Send request to Gemini API
        response = requests.post(API_URL, json=payload)
        response_data = response.json()

        # Extract the response from the API
        api_response = response_data.get('response', 'I am not sure how to answer that.')

        return jsonify({'response': api_response})

    except Exception as e:
        return jsonify({'response': 'Error contacting the API. Please try again later.'})

@app.route('/submit_order', methods=['POST'])
def submit_order():
    stamp_type = request.form.get('stampType')
    name = request.form.get('name')
    email = request.form.get('email')
    quantity = request.form.get('quantity')
    
    return redirect(url_for('payment', stampType=stamp_type, name=name, email=email, quantity=quantity))

@app.route('/payment')
def payment():
    stamp_type = request.args.get('stampType')
    name = request.args.get('name')
    email = request.args.get('email')
    quantity = request.args.get('quantity')
    total_amount = int(quantity) * 10
    
    return render_template('payment.html', stamp_type=stamp_type, name=name, email=email, quantity=quantity, total_amount=total_amount)




db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'koushikkrish@22',
    'database': 'postalcircles_db'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/manage_stamps', methods=['GET', 'POST'])
def manage_stamps():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        if request.method == 'POST':
            if 'addStampForm' in request.form:
                # Add new stamp
                stamp_name = request.form.get('stampName')
                stamp_year = request.form.get('stampYear')
                stamp_price = request.form.get('stampPrice')
                print(stamp_name)
                
                # Handle file upload
                if 'stampImage' in request.files:
                    image_file = request.files['stampImage']
                    if image_file and allowed_file(image_file.filename):
                        image_url = f"/path/to/images/{image_file.filename}"
                        image_file.save(image_url)
                    else:
                        image_url = ''
                else:
                    image_url = ''

                cursor.execute(
                    "INSERT INTO carousel_items (image_url, title, description, price) VALUES (%s, %s, %s, %s)",
                    (image_url, stamp_name, '', stamp_price)
                )
                conn.commit()

            elif 'updateStampForm' in request.form:
                # Update stamp
                stamp_id = request.form.get('existingStamps')
                update_name = request.form.get('updateStampName')
                update_year = request.form.get('updateStampYear')
                update_price = request.form.get('updateStampPrice')
                cursor.execute(
                    "UPDATE carousel_items SET title=%s, price=%s WHERE id=%s",
                    (update_name, update_price, stamp_id)
                )
                conn.commit()

            elif 'deleteStamp' in request.form:
                # Delete stamp
                stamp_id = request.form.get('deleteStampId')
                cursor.execute("DELETE FROM carousel_items WHERE id=%s", (stamp_id,))
                conn.commit()

        cursor.execute("SELECT * FROM carousel_items")
        stamps = cursor.fetchall()
        return render_template('stamps.html', stamps=stamps)

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        flash('An error occurred. Please try again.', 'error')
    
    finally:
        cursor.close()
        conn.close()



#raga's app
# Ensure pymysql works as MySQLdb
pymysql.install_as_MySQLdb()


app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Initialize the database
db = SQLAlchemy(app)

# Define Stamp model
class Stamp(db.Model):
    __tablename__ = 'stamp'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year_of_manufacture = db.Column(db.Integer, nullable=False)
    coated_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo_filename = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Stamp {self.name}>'

# Define Purchase model
class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stamp_id = db.Column(db.Integer, db.ForeignKey('stamp.id'), nullable=False)  # Reference to Stamp
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    stamp = db.relationship('Stamp', backref='purchases')  # This links to the Stamp table

    def __repr__(self):
        return f'<Purchase {self.name}>'


@app.route('/orders')
def orders():
    purchases = Purchase.query.all()  # Fetch all purchase data including related stamps
    return render_template('orders.html', purchases=purchases)


@app.route('/purchase/<int:stamp_id>', methods=['GET', 'POST'])
def purchase(stamp_id):
    stamp = Stamp.query.get_or_404(stamp_id)  # Fetch the stamp from the database

    if request.method == 'POST':
        # Collect form data and create a new purchase
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        
        # Create a new Purchase instance
        new_purchase = Purchase(
            stamp_id=stamp_id,  # Associate the stamp with the purchase
            name=name,
            email=email,
            phone=phone,
            address=address
        )

        # Add the purchase to the database
        db.session.add(new_purchase)
        db.session.commit()

        return redirect(url_for('purchase_success'))

    return render_template('purchase.html', stamp=stamp)  # Pass the stamp object to the template


@app.route('/submit_purchase', methods=['POST'])
def submit_purchase():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']

    # Create a new purchase instance
    new_purchase = Purchase(name=name, email=email, phone=phone, address=address)

    # Add to the database
    db.session.add(new_purchase)
    db.session.commit()

    return redirect(url_for('purchase_success'))  # Redirect to a thank you page


@app.route('/success', methods=['GET'])
def purchase_success():
    return "Purchase completed successfully!"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_type = request.form['user_type']
    if user_type == 'buyer':
        return redirect(url_for('buyer_home'))
    elif user_type == 'seller':
        return redirect(url_for('seller_home'))

@app.route('/buyer_home')
def buyer_home():
    try:
        stamps = Stamp.query.all()  # Use SQLAlchemy to query the stamps
        print(stamps)  # Debug print statement
    except Exception as e:
        print(f"Error connecting to database: {e}")
        stamps = []

    return render_template('buyer_home.html', stamps=stamps)

@app.route('/seller_home')
def seller_home():
    return render_template('seller_home.html')
@app.route('/sell_stamp')
def sell_stamp():
    return render_template('seller.html')  # Render the seller.html template


@app.route('/submit_stamp', methods=['POST'])
def submit_stamp():
    stamp_name = request.form['stamp_name']
    year_of_manufacture = request.form['year_of_manufacture']
    coated_price = request.form['coated_price']
    description = request.form['description']
    file = request.files['stamp_photo']
    
    if file and file.filename:
        filename = secure_filename(file.filename)  # Secure the filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the file
        file.save(file_path)

        new_stamp = Stamp(
            name=stamp_name,
            year_of_manufacture=year_of_manufacture,
            coated_price=coated_price,
            description=description,
            photo_filename=filename
        )
        db.session.add(new_stamp)
        db.session.commit()
        return redirect(url_for('success'))
    
    return 'Failed to upload stamp'

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('search', '').strip()  # Get search term from query parameter
    
    if query:
        stamps = Stamp.query.filter(Stamp.name.ilike(f'%{query}%')).all()
        return render_template('search.html', stamps=stamps) if stamps else render_template('search.html', stamps=[], message="No stamps found matching your search.")
    return redirect(url_for('buyer_home'))

@app.route('/wishlist')
def wishlist():
    wishlist_items = session.get('wishlist', [])
    return render_template('wishlist.html', wishlist_items=wishlist_items)

@app.route('/success')
def success():
    return 'Stamp uploaded successfully!'


if __name__ == '__main__':

#    with app.app_context():
#         db.create_all()
        app.run(debug=True)
