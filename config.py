from dotenv import dotenv_values

config_values = dotenv_values('.env')

geonames_username = config_values['GEONAMES_USERNAME']
api_key = config_values['API_KEY']
flask_secret_key = config_values['FLASK_SECRET_KEY']
sql_database_uri = config_values['SQL_DATABASE_URI']
flask_jwt_secret_key = config_values['FLASK_JWT_SECRET_KEY']
flask_jwt_access_token_minutes = int(
    config_values['FLASK_JWT_ACCESS_TOKEN_MINUTES'])
flask_jwt_refresh_token_days = int(
    config_values['FLASK_JWT_REFRESH_TOKEN_DAYS'])
flask_jwt_token_location = config_values['FLASK_JWT_TOKEN_LOCATION']