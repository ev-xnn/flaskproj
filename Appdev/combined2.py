from flask import Flask, render_template, request, redirect, url_for, session, flash
import shelve
import random
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'

SHELVE_DB = "auditions.db"
APPLICANTS_DB = "applicants.db"
SHOP_DB = "shop_data.db"
COMPETITIONS_DB = "competitions.db"
APP_DATA = "app_data"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/gig_signup')
def gig_form():
    return render_template('gig_signup.html', applicant=None)

@app.route('/add', methods=['POST'])
def add_applicant():
    with shelve.open(APPLICANTS_DB, writeback=True) as db:
        applicant_id = str(uuid.uuid4())
        db[applicant_id] = {
            'id': applicant_id,
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'birth_date': request.form['birth_date'],
            'gender': request.form['gender'],
            'email': request.form['email'],
            'username': request.form['username'],
            'phone': request.form['phone'],
            'city': request.form['city'],
            'state': request.form['state'],
            'zip': request.form['zip'],
            'country': request.form['country']
        }
    flash('Application added successfully!')
    return redirect(url_for('view_applicants'))

@app.route('/applicants')
def view_applicants():
    with shelve.open(APPLICANTS_DB) as db:
        applicants = list(db.values())
    return render_template('view_applicants.html', applicants=applicants)

@app.route('/edit/<applicant_id>', methods=['GET', 'POST'])
def edit_applicant(applicant_id):
    with shelve.open(APPLICANTS_DB, writeback=True) as db:
        applicant = db[applicant_id]
        if request.method == 'POST':
            applicant.update({
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'birth_date': request.form['birth_date'],
                'gender': request.form['gender'],
                'email': request.form['email'],
                'username': request.form['username'],
                'phone': request.form['phone'],
                'city': request.form['city'],
                'state': request.form['state'],
                'zip': request.form['zip'],
                'country': request.form['country']
            })
            flash('Application updated successfully!')
            return redirect(url_for('view_applicants'))
    return render_template('gig_signup.html', applicant=applicant)

@app.route('/delete/<applicant_id>')
def delete_applicant(applicant_id):
    with shelve.open(APPLICANTS_DB, writeback=True) as db:
        del db[applicant_id]
    flash('Application deleted successfully!')
    return redirect(url_for('view_applicants'))

@app.route('/shop')
def shop():
    with shelve.open(SHOP_DB) as db:
        products = db.get('products', [])
    return render_template('shop.html', products=products)

@app.route('/competition')
def competition():
    return render_template('facilitate.html')

@app.route('/artist_contract', methods=['GET', 'POST'])
def artist_contract():
    with shelve.open(APP_DATA) as db:
        contracts = db.get('contracts', [])
        if request.method == 'POST':
            new_contract = {
                'id': len(contracts) + 1,
                'name': request.form['contract_name'],
                'email': request.form['email'],
                'venue_location': request.form['venue_location'],
                'country': request.form['country'],
                'phone_number': request.form['phone_number']
            }
            contracts.append(new_contract)
            db['contracts'] = contracts
    return render_template('artist_contract.html', contracts=contracts)

@app.route('/live_calendar', methods=['GET', 'POST'])
def live_calendar():
    with shelve.open(APP_DATA) as db:
        events = db.get('events', [])
        if request.method == 'POST':
            new_event = {
                'id': len(events) + 1,
                'name': request.form['event_name'],
                'event_date': request.form['event_date'],
                'start_time': request.form['start_time'],
                'end_time': request.form['end_time']
            }
            events.append(new_event)
            db['events'] = events
    return render_template('live_calendar.html', events=events)

if __name__ == '__main__':
    app.run(debug=True)
