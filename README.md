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
   ```sql
   bash
   pip install requests
   ```
   
3. Get an API key from [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account
   - Generate an API key in your dashboard

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

Error Handling
-------------------------------------------------------------------------------------------
The application includes:

* API request timeout management

* Network failure retry logic

* Data validation before storage

* Graceful degradation when services are unavailable

Data Storage & Monitoring
--------------------------------------------------------------------------------------------
* SQLite Database Integration: structured storage with tables for weather metrics, timestamps, and city information

* Structured Schema Design: organizetable structure with columns for temperature, humidity, weather conditions, wind speed

* Application Activity Tracking: Logs API calls, data fetch operations

* Performance Metrics Collection: Tracks data retrieval times, storage performance

Database output
--------------------------------------------------------------------------------------------
``` sql
==================================================
  REAL-TIME WEATHER DATA LOGGER
==================================================
1. Get Current Weather
2. View Query History
3. View History for Specific City
4. Get City Statistics
5. Clear Database
6. Exit
==================================================
Enter your choice (1-6): 2

================================================================================
 WEATHER QUERY HISTORY
================================================================================
ID: 4 | City: guntur | Temp: 21.52°C
Humidity: 85% | Condition: overcast clouds
Time: 2025-11-26 21:49:30
--------------------------------------------------------------------------------
ID: 3 | City: guntur | Temp: 21.2°C
Humidity: 86% | Condition: few clouds
Time: 2025-11-25 22:00:29
--------------------------------------------------------------------------------
ID: 2 | City: vijayawada | Temp: 29.97°C
Humidity: 74% | Condition: scattered clouds
Time: 2025-11-02 19:07:04
--------------------------------------------------------------------------------
ID: 1 | City: bapatla | Temp: 27.16°C
Humidity: 80% | Condition: light rain
Time: 2025-11-02 19:06:48
--------------------------------------------------------------------------------
```





