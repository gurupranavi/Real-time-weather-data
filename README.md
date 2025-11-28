Real-Time Weather Information & Data Logger
-------------------------------------------------------------------------------------------
A Python application that fetches real-time weather data from OpenWeatherMap API, displays detailed weather information, and automatically logs all data with timestamps to SQLite database and text files.

Project Structure
-------------------------------------------------------------------------------------------
WEATHER.LOGGER/
├── requirements.txt      
├── weather_app.py       
└── weather_data.db

Features
-------------------------------------------------------------------------------------------
* Real-Time Weather Data: Fetches current weather data from OpenWeatherMap API with real-time updates
  
* Multi-City Support & Comparison: View weather differences between various locations simultaneously
  
* Data Management & Persistence: Maintain complete weather history for trend analysis and pattern recognition

* Application Architecture: Easily extensible architecture for adding new features and data sources.

Requirements
-------------------------------------------------------------------------------------------
Python 3.6+
requests library

Installation
------------------------------------------------------------------------------------------
1. Clone or download the project files
2. Install required dependencies:
   bash
   pip install requests

Database Schema
-------------------------------------------------------------------------------------------
The apllication uses sql with the following table structure:
``` sql
CREATE TABLE weather_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT NOT NULL,
    temperature REAL NOT NULL,
    humidity INTEGER NOT NULL,
    weather_description TEXT NOT NULL,
    wind_speed REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```






