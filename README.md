Real-Time Weather Information & Data Logger
-------------------------------------------------------------------------------------------
A Python application that fetches real-time weather data from OpenWeatherMap API, displays detailed weather information, and automatically logs all data with timestamps to SQLite database and text files.

Features
-------------------------------------------------------------------------------------------
* Real-Time Weather Data: Fetches current weather data from OpenWeatherMap API with real-time updates.
* Multi-City Support & Comparison: View weather differences between various locations simultaneously.
* Data Management & Persistence: Maintain complete weather history for trend analysis and pattern recognition.
* Application Architecture: Easily extensible architecture for adding new features and data sources.

Project Structure
-------------------------------------------------------------------------------------------
WEATHER.LOGGER/
├── requirements.txt      
├── weather_app.py       
└── weather_data.db

Data Storage & Logging
-------------------------------------------------------------------------------------------
* SQLite Relational Database: Lightweight, file-based database for efficient data storage
* Complete API Response Storage: Store full JSON responses for audit trails and debugging
* Error Tracking: Separate error logging with stack traces and contextual information
* Performance Metrics: Log response times and API performance for optimization
* Automatic File Backups

user Experience
-------------------------------------------------------------------------------------------
* User Assistance Features: User-friendly explanations when problems occur
* Workflow Optimization:Complete multiple tasks without restarting the application
* Data Presentation:Consistent formatting for easy data comprehension
* Input Handling & Validation:Handle various city name formats and international characters

Error Handling
-------------------------------------------------------------------------------------------
* Connection Timeouts
* API Rate Limiting
* Input Boundary Checking
* Invalid API Responses
* Service Unavailability
