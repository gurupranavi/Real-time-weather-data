import requests
import sqlite3
import json
from datetime import datetime
import os

class WeatherDataLogger:
    """Main class to handle weather data fetching and logging"""
    
    def __init__(self, api_key='a3d3fef27cb501298da52a0b344b7ce8', db_name='weather_data.db'):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.db_name = db_name
        self.setup_database()  # Create database and tables on initialization
    
    def setup_database(self):
        """Initialize SQLite database with required tables"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weather_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city_name TEXT NOT NULL,
                    temperature REAL NOT NULL,
                    humidity INTEGER NOT NULL,
                    weather_condition TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    api_response TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            print(f"Database '{self.db_name}' initialized successfully!")
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
    
    def fetch_weather_data(self, city_name):
        """Fetch weather data from OpenWeatherMap API"""
        try:
            # API parameters
            params = {
                'q': city_name, # City name
                'appid': self.api_key,  # API key
                'units': 'metric'  # For Celsius temperature
            }
            
            # Make API request
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return None
    
    def parse_weather_data(self, data):
        """Extract relevant information from API response"""
        if not data or data.get('cod') != 200:
            return None
        
        try:
            weather_info = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'weather_condition': data['weather'][0]['description'],
                'country': data['sys']['country']
            }
            return weather_info
            
        except KeyError as e:
            print(f"Error parsing weather data: Missing key {e}")
            return None
    
    def log_to_database(self, city_name, weather_info, api_response):
        """Log weather data to SQLite database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            cursor.execute('''
                INSERT INTO weather_logs 
                (city_name, temperature, humidity, weather_condition, timestamp, api_response)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                city_name,
                weather_info['temperature'],
                weather_info['humidity'],
                weather_info['weather_condition'],
                timestamp,
                json.dumps(api_response)
            ))
            
            conn.commit()
            conn.close()
            print("Data logged to database successfully!")
            return True
            
        except sqlite3.Error as e:
            print(f"Database logging error: {e}")
            return False
    
    def display_weather_info(self, weather_info):
        """Display weather information in a formatted way"""
        if not weather_info:
            return
        
        print("\n" + "="*50)
        print(" WEATHER INFORMATION")
        print("="*50)
        print(f" City: {weather_info['city']}, {weather_info['country']}")
        print(f"  Temperature: {weather_info['temperature']}°C")
        print(f" Humidity: {weather_info['humidity']}%")
        print(f"  Condition: {weather_info['weather_condition'].title()}")
        print("="*50 + "\n")
    
    def get_weather_history(self, city_name=None, limit=10):
        """Retrieve weather history from database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            if city_name:
                cursor.execute('''
                    SELECT * FROM weather_logs 
                    WHERE city_name = ? 
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (city_name, limit))
            else:
                cursor.execute('''
                    SELECT * FROM weather_logs 
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
            
            records = cursor.fetchall()
            conn.close()
            return records
            
        except sqlite3.Error as e:
            print(f"Error retrieving history: {e}")
            return []
    
    def display_history(self, city_name=None):
        """Display weather query history"""
        records = self.get_weather_history(city_name)
        
        if not records:
            print("No history records found.")
            return
        
        print(f"\n{'='*80}")
        print(" WEATHER QUERY HISTORY")
        if city_name:
            print(f"Filtered by: {city_name}")
        print(f"{'='*80}")
        
        for record in records:
            print(f"ID: {record[0]} | City: {record[1]} | Temp: {record[2]}°C")
            print(f"Humidity: {record[3]}% | Condition: {record[4]}")
            print(f"Time: {record[5]}")
            print("-" * 80)
    
    def get_city_statistics(self, city_name):
        """Get statistics for a specific city"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_queries,
                    AVG(temperature) as avg_temp,
                    AVG(humidity) as avg_humidity,
                    MIN(temperature) as min_temp,
                    MAX(temperature) as max_temp
                FROM weather_logs 
                WHERE city_name = ?
            ''', (city_name,))
            
            stats = cursor.fetchone()
            conn.close()
            
            return stats
            
        except sqlite3.Error as e:
            print(f"Error retrieving statistics: {e}")
            return None

class WeatherApp:
    """Main application class to handle user interactions"""
    
    def __init__(self):
        # Use the default API key directly
        self.api_key = 'a3d3fef27cb501298da52a0b344b7ce8'
        self.weather_logger = WeatherDataLogger(self.api_key)
    
    def validate_city_name(self, city_name):
        """Validate city name input"""
        if not city_name or not city_name.strip():
            return False, "City name cannot be empty."
        
        if not all(c.isalpha() or c.isspace() or c in ".-', " for c in city_name):
            return False, "City name contains invalid characters."
        
        return True, "Valid"
    
    def main_menu(self):
        """Display main menu and handle user choices"""
        while True:
            print("\n" + "="*50)
            print("  REAL-TIME WEATHER DATA LOGGER")
            print("="*50)
            print("1. Get Current Weather")
            print("2. View Query History")
            print("3. View History for Specific City")
            print("4. Get City Statistics")
            print("5. Clear Database")
            print("6. Exit")
            print("="*50)
            
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                self.get_weather()
            elif choice == '2':
                self.weather_logger.display_history()
            elif choice == '3':
                city = input("Enter city name: ").strip()
                self.weather_logger.display_history(city)
            elif choice == '4':
                self.show_city_statistics()
            elif choice == '5':
                self.clear_database()
            elif choice == '6':
                print("Thank you for using Weather Data Logger! Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1-6.")
    
    def get_weather(self):
        """Get and display weather for a city"""
        city_name = input("\nEnter city name: ").strip()
        
        # Validate input
        is_valid, message = self.validate_city_name(city_name)
        if not is_valid:
            print(f"Error: {message}")
            return
        
        print(f"\nFetching weather data for {city_name}...")
        
        # Fetch data from API
        api_response = self.weather_logger.fetch_weather_data(city_name)
        
        if not api_response:
            print("Failed to fetch weather data. Please check the city name and try again.")
            return
        
        # Check for API errors
        if api_response.get('cod') != 200:
            error_message = api_response.get('message', 'Unknown error')
            print(f"API Error: {error_message}")
            return
        
        # Parse and display data
        weather_info = self.weather_logger.parse_weather_data(api_response)
        
        if weather_info:
            self.weather_logger.display_weather_info(weather_info)
            
            # Log to database
            if self.weather_logger.log_to_database(city_name, weather_info, api_response):
                print("Data successfully logged!")
            else:
                print("Data fetched but logging failed!")
        else:
            print("Failed to parse weather data.")
    
    def show_city_statistics(self):
        """Display statistics for a specific city"""
        city_name = input("\nEnter city name for statistics: ").strip()
        
        is_valid, message = self.validate_city_name(city_name)
        if not is_valid:
            print(f"Error: {message}")
            return
        
        stats = self.weather_logger.get_city_statistics(city_name)
        
        if not stats or stats[0] == 0:
            print(f"No data found for city: {city_name}")
            return
        
        print(f"\n{'='*50}")
        print(f" STATISTICS FOR {city_name.upper()}")
        print(f"{'='*50}")
        print(f"Total Queries: {stats[0]}")
        print(f"Average Temperature: {stats[1]:.2f}°C")
        print(f"Average Humidity: {stats[2]:.2f}%")
        print(f"Minimum Temperature: {stats[3]:.2f}°C")
        print(f"Maximum Temperature: {stats[4]:.2f}°C")
        print(f"{'='*50}")
    
    def clear_database(self):
        """Clear all data from the database"""
        confirm = input("\nAre you sure you want to clear all weather data? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            try:
                conn = sqlite3.connect(self.weather_logger.db_name)
                cursor = conn.cursor()
                cursor.execute('DELETE FROM weather_logs')
                conn.commit()
                conn.close()
                print("All weather data has been cleared!")
            except sqlite3.Error as e:
                print(f"Error clearing database: {e}")
        else:
            print("Operation cancelled.")

def main():
    """Main function to run the application"""
    try:
        print("Initializing Weather Data Logger...")
        app = WeatherApp()
        app.main_menu()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
