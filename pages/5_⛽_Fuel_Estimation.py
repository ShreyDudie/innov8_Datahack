import streamlit as st

st.set_page_config(page_title="Fuel Estimation", page_icon="⛽")
st.title("Aircraft Fuel Estimation Tool")


aircraft_type = st.selectbox("Select Aircraft Type", options=["Jet", "Plane", "Helicopter", "Glider"])

distance = st.slider("Flight Distance (Nautical Miles)", min_value=0, max_value=10000)
average_speed = st.slider("Average Speed (Knots)", min_value=0, max_value=1000)
if aircraft_type == 'Jet':
    sfc = 0.336
if aircraft_type == 'Plane':
    sfc = 5000
if aircraft_type == 'Helicopter':
    sfc = 1.1
if aircraft_type == 'Glider':
    sfc = 0.5

reserve_time = st.slider("Reserve Time (Minutes)", min_value=0, max_value=120)

if average_speed > 0:
    flight_duration_hours = distance / average_speed
else:
    flight_duration_hours = 0


if sfc > 0:
    total_fuel_required = flight_duration_hours * sfc
else:
    total_fuel_required = 0

reserve_fuel = (reserve_time / 60) * sfc if sfc > 0 else 0
total_fuel_needed = total_fuel_required + reserve_fuel

st.subheader("Estimated Fuel Calculations")
st.write(f"Flight Duration: {flight_duration_hours:.2f} hours")
st.write(f"Total Fuel Required: {total_fuel_required:.2f} pounds")
st.write(f"Reserve Fuel: {reserve_fuel:.2f} pounds")
st.write(f"*Total Fuel Needed: {total_fuel_needed:.2f} pounds*")

st.sidebar.header("Example Inputs")
st.sidebar.write("Aircraft Type: Jet")
st.sidebar.write("Distance: 100 Nautical Miles")
st.sidebar.write("Average Speed: 120 Knots")
st.sidebar.write("Reserve Time: 30 Minutes")