from datetime import timedelta

import markdown
import requests
from flask import Flask, render_template, request, jsonify, Response
from weasyprint import HTML

from ai.services import generate_ai_response
from config import (
    geonames_username,
    flask_secret_key,
    flask_jwt_secret_key,
    flask_jwt_access_token_minutes,
    flask_jwt_refresh_token_days,
    flask_jwt_token_location
)
from database import Base, engine
from extensions import bcrypt, jwt
from services import save_response_to_db, get_plan_from_db, generate_markdown
from users.routes import users_bp

app = Flask(__name__)
app.register_blueprint(users_bp)

app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = flask_secret_key
app.config['JWT_SECRET_KEY'] = flask_jwt_secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(
    minutes=flask_jwt_access_token_minutes)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(
    days=flask_jwt_refresh_token_days)
app.config['JWT_TOKEN_LOCATION'] = [flask_jwt_token_location]

Base.metadata.create_all(engine)

jwt.init_app(app)
bcrypt.init_app(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify([])

    url = f'http://api.geonames.org/searchJSON?q={query}&featureClass=P&maxRows=5&username={geonames_username}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        results = [
            f'{city["name"]}, {city["countryName"]}'
            for city in data.get('geonames', [])
        ]
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return jsonify([])

    return jsonify(results)


@app.route('/validate-destination', methods=['GET'])
def validate_destination():
    destination = request.args.get('destination', '').strip()

    if not destination:
        return jsonify({'valid': False})

    url = f'http://api.geonames.org/searchJSON?q={destination}&featureClass=P&maxRows=1&username={geonames_username}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get('geonames'):
            return jsonify({'valid': True})
        else:
            return jsonify({'valid': False})
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return jsonify({'valid': False})


@app.route('/plans', methods=['POST', 'GET'])
def get_plans():
    if request.method == 'POST':
        destination = request.form['destination']
        travel_days = request.form['travel_days']
        budget = request.form['budget']
        interests = request.form.getlist('interests')
        interests_str = ', '.join(
            interests) if interests else 'General sightseeing'

        response = generate_ai_response(travel_days, destination,
                                        budget, interests_str)
        plans = save_response_to_db(response)

        return render_template('plans.html', plans=plans)


@app.route('/plans/<int:plan_id>/download')
def download_pdf(plan_id: int):
    plan = get_plan_from_db(plan_id)
    plan_md = generate_markdown(plan)
    plan_html = markdown.markdown(plan_md)
    pdf = HTML(string=plan_html).write_pdf()

    return Response(
        pdf,
        mimetype='application/pdf',
        headers={
            'Content-Disposition': f'attachment; filename=plan_{plan_id}.pdf'
        }
    )


@app.route('/is-authenticated')
def is_authenticated():
    if request.cookies.get('access_token_cookie'):
        return jsonify({'authenticated': True})
    return jsonify({'authenticated': False})


if __name__ == '__main__':
    app.run(debug=True)
