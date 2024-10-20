import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pytz
import pyowm
from datetime import datetime
import os
import warnings

st.set_page_config(page_title="Safety Predictions", page_icon="⚠️")


if 'show_weather' not in st.session_state:
    st.session_state.show_weather = False

# Display logo and title
try:
    st.image('assets/logo.png')
except:
    st.warning("Logo image not found")
st.title('Safety Predictions')


if st.button('Use Weather', key='weather_button'):
    st.session_state.show_weather = not st.session_state.show_weather


if st.session_state.show_weather:
    
    API_KEY = 'd771edcecc8137cb7df3ef306e84068d'
    if not API_KEY:
        st.error("API_KEY not found")
        st.stop()
    
    owm = pyowm.OWM(API_KEY)
    mgr = owm.weather_manager()
    degree_sign = u'\N{DEGREE SIGN}'
    
    
    place = st.text_input("NAME OF THE CITY:", "")
    
    if place:  
        place = place.lower()
        
       
        unit = st.selectbox("Select Temperature Unit", ("Celsius", "Fahrenheit"))
        g_type = st.selectbox("Select Graph Type", ("Line Graph", "Bar Graph"))
        
        unit_c = 'celsius' if unit == 'Celsius' else 'fahrenheit'
        
        try:
            
            observation = mgr.weather_at_place(place)
            weather = observation.weather
            
            # Display current weather
            temperature = weather.temperature(unit_c)
            st.write(f"Temperature: {temperature['temp']}{degree_sign} {unit}")
            st.write(f"Feels Like: {temperature['feels_like']}{degree_sign} {unit}")
            st.write(f"Humidity: {weather.humidity}%")
            st.write(f"Wind Speed: {weather.wind()['speed']} m/s")
            st.write(f"Weather: {weather.status}")
            
            # Get data
            weather_data = {
                'Metric': ['Temperature', 'Feels Like', 'Humidity', 'Wind Speed'],
                'Value': [temperature['temp'], temperature['feels_like'], 
                         weather.humidity, weather.wind()['speed']]
            }
            df = pd.DataFrame(weather_data)
            
            # Create plot 
            if g_type == "Line Graph":
                fig = px.line(df, x='Metric', y='Value', 
                            title=f'Weather Metrics for {place.title()}')
            else:  # Bar Graph
                fig = px.bar(df, x='Metric', y='Value',
                            title=f'Weather Metrics for {place.title()}')
            
            st.plotly_chart(fig)
            
        except pyowm.commons.exceptions.NotFoundError:
            st.error("City not found! Please check the spelling and try again.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    try:
        windSpeed = weather.wind()
        windSpeed = st.slider("Enter Wind Speed in knots")
        def windType():
            if windSpeed < 1:
                st.write('Calm Wind')
            if windSpeed in range(1,3) or windSpeed == 3:
                st.write('Light Air')
            if windSpeed in range(4,6) or windSpeed == 6:
                st.write('Light Breeze')
            if windSpeed in range(7,10) or windSpeed == 10:
                st.write('Gentle Breeze')
            if windSpeed in range(11,16) or windSpeed == 16:
                st.write('Moderate Breeze')
            if windSpeed in range(17,21) or windSpeed == 21:
                st.write('Fresh Breeze')
            if windSpeed in range(22,27) or windSpeed == 27:
                st.write('Strong Breeze')
            if windSpeed in range(28,33) or windSpeed == 33:
                st.write('Moderate or Real Gale')
            if windSpeed in range(34,40) or windSpeed == 40:
                st.write('Gale or Fresh Gale')
            if windSpeed in range(41,47) or windSpeed == 47:
                st.write('Strong Gale')
            if windSpeed in range(48,55) or windSpeed == 55:
                st.write('Whole Gale or Storm')
            if windSpeed in range(56,63) or windSpeed == 63:
                st.write('Violent Storm')
            if windSpeed >= 64:
                st.write('Hurricane')
            
        if st.button('Submit'):
            windType()
    except Exception as e:
        print(e)


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

data = pd.read_csv(r"pages/data/airline_weather.csv", 
                   dtype={
                       'Airline ID': 'float64',
                       'Airline Code': 'str',
                       'Flight Number': 'float64',
                       'Departure Airport Code': 'str',
                       'Arrival Airport code': 'str',
                       'Air Time': 'float64',
                       'Scheduled Departure': 'str',
                       'Actual Departure': 'str',
                       'Scheduled Arrival': 'str',
                       'Actual Arrival': 'str',
                       'Delay In Minutes': 'float64',
                       'Unnamed: 11': 'float64',
                       'weather': 'str'
                   })

# Drop rows with NaN in the specified columns
data.dropna(subset=['Actual Departure', 'Actual Arrival', 'Delay In Minutes'], inplace=True)

# Convert datetime columns
data['Actual Departure'] = pd.to_datetime(data['Actual Departure'], errors='coerce')
data['Actual Arrival'] = pd.to_datetime(data['Actual Arrival'], errors='coerce')

# Check if there are NaT values after conversion
data.dropna(subset=['Actual Departure', 'Actual Arrival'], inplace=True)

# Select features and target
X = data[['Airline ID', 'Flight Number', 'Air Time', 'Delay In Minutes']]
y = data['weather']  # or another target variable

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and fit the model
model = RandomForestClassifier(n_estimators=100, random_state=42)  # Adjust n_estimators if needed
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
st.success("Accuracy:", accuracy_score(y_test, y_pred))
st.write("Classification Report:\n", classification_report(y_test, y_pred))
st.dataframe("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
