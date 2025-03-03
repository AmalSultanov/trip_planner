import logging
from datetime import timedelta
from logging.config import dictConfig

from flask import Flask, render_template, request, jsonify, Response

from ai.services import generate_ai_response
from config import (
    flask_secret_key,
    flask_jwt_secret_key,
    flask_jwt_access_token_minutes,
    flask_jwt_refresh_token_days,
    flask_jwt_token_location
)
from database import Base, engine
from extensions import bcrypt, jwt
from services import (
    save_response_to_db,
    get_plan_from_db,
    extract_fields,
    fetch_autocomplete_results,
    fetch_destination_validation,
    generate_pdf
)
from users.routes import users_bp

dictConfig(
    {
        'version': 1,
        'formatters': {
            'default': {
                'format': '{levelname} | {asctime:s} | {name} | {message}',
                'style': '{'
            },
            'verbose': {
                'format': '{levelname} | {asctime:s} | {name} | '
                          '{module}.py (line {lineno:d}) | {funcName} | {message}',
                'style': '{'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter': 'default',
                'level': 'INFO'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/logs.log',
                'maxBytes': 5 * 1024 * 1024,
                'backupCount': 3,
                'formatter': 'verbose',
                'level': 'WARNING'
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        },
        'loggers': {
            'flask.app': {
                'level': 'WARNING',
                'handlers': ['file'],
                'propagate': False
            }
        }
    }
)

app = Flask(__name__)
app.register_blueprint(users_bp)
app.logger.setLevel(logging.DEBUG)

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

logger = logging.getLogger(__name__)


@app.route('/')
def home() -> str:
    return render_template('index.html')


@app.route('/autocomplete')
def autocomplete() -> Response:
    query = request.args.get('query', '').strip()

    if not query:
        return jsonify([])

    results = fetch_autocomplete_results(query)
    return jsonify(results)


@app.route('/validate-destination', methods=['GET'])
def validate_destination() -> Response:
    destination = request.args.get('destination', '').strip()

    if not destination:
        return jsonify({'valid': False})

    is_valid = fetch_destination_validation(destination)
    return jsonify({'valid': is_valid})


@app.route('/plans', methods=['POST', 'GET'])
def get_plans() -> str:
    if request.method == 'POST':
        response = generate_ai_response(*extract_fields(request))

        if 'error' in response:
            logger.error(f'Error: {response['error']}')
            return render_template('plans.html',
                                   error='Error occurred, try again')

        plans = save_response_to_db(response)
        return render_template('plans.html', plans=plans)


@app.route('/plans/<int:plan_id>/download')
def download_pdf(plan_id: int) -> Response:
    pdf = generate_pdf(get_plan_from_db(plan_id))

    return Response(
        pdf,
        mimetype='application/pdf',
        headers={
            'Content-Disposition': f'attachment; filename=plan_{plan_id}.pdf'
        }
    )


@app.route('/is-authenticated')
def is_authenticated() -> Response:
    is_auth = bool(request.cookies.get('access_token_cookie'))
    return jsonify({'authenticated': is_auth})


if __name__ == '__main__':
    app.run(debug=True)
