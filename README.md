# AI-Powered Travel Itinerary Planner

## Overview

The **AI-Powered Travel Itinerary Planner** is a Flask-based web application that generates personalized travel plans using AI. Users can enter trip details, and the system suggests an itinerary, which can be viewed and downloaded as a PDF.

## Features

- AI-powered travel plan generation
- User authentication using JWT tokens
- Plan storage and retrieval from the database
- PDF download for travel plans
- Docker support for containerized deployment

## Installation
### Prerequisites

- Python 3.10+
- Docker
- Docker Compose
- A valid API key from [Google Gemini API](https://ai.google.dev/gemini-api/docs/api-key)
- A registered account on [GeoNames](https://www.geonames.org) to obtain a username

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/AmalSultanov/trip_planner.git
   cd trip_planner
   ```

2. **Set Up Environment Variables:**

   - Copy the example environment file:
     ```bash
     cp .env.example .env
     ```
   - Open the `.env` file and fill in the required values:
     ```ini
     GEONAMES_USERNAME=
     API_KEY=

     FLASK_SECRET_KEY=

     POSTGRES_DB=
     POSTGRES_USER=
     POSTGRES_PASSWORD=
     POSTGRES_HOST=
     POSTGRES_PORT=
     SQL_DATABASE_URI=

     FLASK_JWT_SECRET_KEY=
     FLASK_JWT_ACCESS_TOKEN_MINUTES=
     FLASK_JWT_REFRESH_TOKEN_DAYS=
     FLASK_JWT_TOKEN_LOCATION=
     ```
    - Visit [GeoNames](https://www.geonames.org) to register and obtain your username, which will be the value for `GEONAMES_USERNAME`.
    - Visit [Google Gemini API](https://ai.google.dev/gemini-api/docs/api-key) to get your API Key, which will be the value for `API_KEY`.
    - The values for `FLASK_SECRET_KEY` and `FLASK_JWT_SECRET_KEY` can be generated using `secrets.token_bytes([nbytes=None])`.
    - The value for `SQL_DATABASE_URI` should be in the format:  
      ```
      postgresql://user:password@host:port/db_name
      ```
   - Values for `FLASK_JWT_ACCESS_TOKEN_MINUTES` and `FLASK_JWT_REFRESH_TOKEN_DAYS` should be numeric.

3. **Run the Application with Docker Compose:**

    ```bash
    docker compose up --build
    ```
   
   **Or, install manually:**
   
   If you prefer to run the application without Docker, follow these steps:

   - **Create a Virtual Environment:**
     ```bash
     python3 -m venv venv
     ```
   - **Activate the Virtual Environment:**
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```
   - **Install Dependencies:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Your Local PostgreSQL Server**
   - **Run the Application:**
     ```bash
     flask run
     ```

4. **Access the Application:**

   The app will be available at **[http://127.0.0.1:5001/](http://localhost:5001/)**.

## API Endpoints

| Method | Endpoint               | Description                |
|--------|------------------------|----------------------------|
| `GET`  | `/`                    | Home page                  |
| `POST` | `/plans`               | Generate a new travel plan |
| `GET`  | `/plans/<id>/download` | Download plan as PDF       |
| `POST` | `/login`               | User login                 |
| `POST` | `/register`            | User registration          |
| `GET`  | `/logout`              | User logout                |

## Contributing

Contributions are welcome! Feel free to fork this repository and submit a pull request.