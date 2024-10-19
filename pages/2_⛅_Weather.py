import streamlit as st

st.set_page_config(page_title='Weather',page_icon=':cloud:')
st.title('Current Weather Forecast')
import pytz
import pyowm
import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

# Fetch the API key 
API_KEY = 'd771edcecc8137cb7df3ef306e84068d'
if not API_KEY:
    st.error("API_KEY not found")
    st.stop()

# Initialize OpenWeatherMap API
owm = pyowm.OWM(API_KEY)
mgr = owm.weather_manager()

degree_sign = u'\N{DEGREE SIGN}'

# Streamlit UI
st.write("Write the name of a City and select the Temperature Unit and Graph Type from the sidebar")

place = st.text_input("NAME OF THE CITY :", "")
place.lower()
if not place:  # Check for empty input
    st.error("Valid city not detected")
else:
    unit = st.selectbox("Select Temperature Unit", ("Celsius", "Fahrenheit"))
    g_type = st.selectbox("Select Graph Type", ("Line Graph", "Bar Graph"))

    unit_c = 'celsius' if unit == 'Celsius' else 'fahrenheit'
    try:
        def get_temperature():
            days = []
            temp_min = []
            temp_max = []
            forecaster = mgr.forecast_at_place(place, '3h')
            forecast = forecaster.forecast
            for weather in forecast:
                day = datetime.utcfromtimestamp(weather.reference_time())
                date = day.date()
                if date not in days:
                    days.append(date)
                    temp_min.append(None)
                    temp_max.append(None)
                temperature = weather.temperature(unit_c)['temp']
                if temp_min[-1] is None or temperature < temp_min[-1]:
                    temp_min[-1] = temperature
                if temp_max[-1] is None or temperature > temp_max[-1]:
                    temp_max[-1] = temperature
            return days, temp_min, temp_max

        def plot_temperatures(days, temp_min, temp_max):
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Minimum Temperatures', x=days, y=temp_min))
            fig.add_trace(go.Bar(name='Maximum Temperatures', x=days, y=temp_max))
            fig.update_layout(barmode='group', title='Temperature Forecast', xaxis_title='Day', yaxis_title=f'Temperature ({degree_sign}{unit[0]})')
            return fig

        def plot_temperatures_line(days, temp_min, temp_max):
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=days, y=temp_min, name='Minimum Temperatures'))
            fig.add_trace(go.Scatter(x=days, y=temp_max, name='Maximum Temperatures'))
            fig.update_layout(title='Temperature Forecast', xaxis_title='Day', yaxis_title=f'Temperature ({degree_sign}{unit[0]})')
            return fig

        def draw_chart():
            days, temp_min, temp_max = get_temperature()
            if g_type == 'Line Graph':
                fig = plot_temperatures_line(days, temp_min, temp_max)
            else:
                fig = plot_temperatures(days, temp_min, temp_max)
            st.plotly_chart(fig)
            st.title("Minimum and Maximum Temperatures")
            for i in range(len(temp_min)):
                st.write(f"### {temp_min[i]}{degree_sign} --- {temp_max[i]}{degree_sign}")

        def display_other_updates():
            forecaster = mgr.forecast_at_place(place, '3h')
            st.title("Impending Weather Alerts:")
            alerts = {
                "will_have_fog": "FOG Alert!",
                "will_have_rain": "Rain Alert",
                "will_have_storm": "Storm Alert!",
                "will_have_snow": "Snow Alert!",
                "will_have_tornado": "Tornado Alert!",
                "will_have_hurricane": "Hurricane Alert!",
                "will_have_clouds": "Cloudy Skies",
                "will_have_clear": "Clear Weather!"
            }
            for key, message in alerts.items():
                if getattr(forecaster, key)():
                    st.write(f"### {message}")

        def display_cloud_and_wind():
            obs = mgr.weather_at_place(place)
            weather = obs.weather
            st.title("Cloud Coverage and Wind Speed")
            st.write(f'### The current cloud coverage for {place} is {weather.clouds}%.')
            st.write(f'### The current wind speed for {place} is {weather.wind()["speed"]} mph.')

        def display_sunrise_and_sunset():
            obs = mgr.weather_at_place(place)
            weather = obs.weather
            st.title("Sunrise and Sunset Times:")
            sr = datetime.fromtimestamp(weather.sunrise_time()).astimezone(pytz.timezone("Asia/Kolkata"))
            ss = datetime.fromtimestamp(weather.sunset_time()).astimezone(pytz.timezone("Asia/Kolkata"))
            st.write(f"### Sunrise time in {place} is {sr.strftime('%Y-%m-%d %H:%M:%S')} IST.")
            st.write(f"### Sunset time in {place} is {ss.strftime('%Y-%m-%d %H:%M:%S')} IST.")

        if st.button("SUBMIT"):
            draw_chart()
            display_other_updates()
            display_cloud_and_wind()
            display_sunrise_and_sunset()
    
    except Exception as ERROR:
        st.error(ERROR)