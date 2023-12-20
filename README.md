# HVAC System Control via Building Occupancy Prediction

## Overview
This project revolves around predicting building occupancy levels using environmental data (humidity, CO2) to control HVAC systems accordingly. A Flask-based application hosts the predictive model, and it's interfaced through user authentication, control point registration, data submission, and retrieval of occupancy predictions via REST API endpoints.

## Files and Folders
### Main Files
- **`main.py`**: Contains the Flask application and API endpoints for user interaction, model prediction, and data handling.
- **`generator.py`**: Generates UUIDs for users.
- **`plot.py`**: Provides functionality to create visualizations of historical CO2 and humidity data.

### Folders
- **`static/`**: Stores static resources like images or stylesheets.
- **`templates/`**: Consists of HTML templates for user interfaces.
- **`.env`**: Environment file storing sensitive configurations (e.g., secret key).

### Supporting Scripts
- **`Data.py`**: Manages database interactions, including user authentication, data storage, and retrieval.
- **`form.py`**: Defines forms for user registration.

## Functionality
- **User Management**:
    - User registration and login are handled securely.
    - Each user can register multiple control points through a user-friendly interface.
- **Predictive Model**:
    - Trained model (stored in `ensa.h5`) predicts occupancy based on CO2 and humidity inputs.
    - Occupancy predictions are categorized as 'low,' 'medium,' or 'high.'
- **Data Handling**:
    - Data submission for CO2 and humidity values per control point via REST API endpoints.
    - Storage and retrieval of historical data for visualization and monitoring.

## Deployment and Usage
1. **Setup**:
    - Install dependencies listed in `requirements.txt`.
    - Configure a PostgreSQL database for data storage.
    - Set up necessary environmental variables in `.env`.

2. **Running the Application**:
    - Execute `main.py` to start the Flask application.
    - Access the provided routes for user registration, login, control point management, and data visualization.

3. **Visualizations and Monitoring**:
    - Use the UI to visualize historical CO2 and humidity data for selected control points.
    - Monitor the latest data and predicted occupancy levels for HVAC system control.

## Technology Stack
- **Flask**: Web framework for application deployment.
- **Plotly** and **Matplotlib**: Libraries for creating data visualizations.
- **PostgreSQL**: Database for storing user information and environmental data.
- **TensorFlow**: Powering the occupancy prediction model.

## Note
- **Database**: This project utilizes PostgreSQL for data storage and retrieval.
- **Security**: Secure storage of user passwords is ensured through hashing.
- **Model Deployment**: TensorFlow is used for model deployment within the Flask app.
