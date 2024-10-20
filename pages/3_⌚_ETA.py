import streamlit as st
import pandas as pd
import numpy as np
import matplotlib as plt
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="ETA", page_icon="⌚")
st.logo(image='assets/logo.png', size='large')
st.title('Delay Prediction')
st.write('Enter user input and predict delays')

Data = pd.read_csv('pages/data/New_Airline.csv')
st.write(Data.head())

#traintestsplit
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

class FlightDelayPredictor:
    def __init__(self, max_depth=10):
        self.model = DecisionTreeRegressor(max_depth=max_depth, random_state=42)
        self.scaler = StandardScaler()
        
    def preprocess_features(self, X):
        """
        Preprocess features for the model.
        Expected features:
        - scheduled_departure_time (in minutes since midnight)
        - distance (in miles)
        - day_of_week (0-6)
        - month (1-12)
        - aircraft_age (years)
        - weather_condition (encoded: 0-clear, 1-light rain, 2-heavy rain, etc.)
        - is_holiday (0 or 1)
        """
        # Convert categorical variables to numeric if needed
        # Scale numerical features
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled
    
    def train(self, X, y):
        """
        Train the model on the given data.
        y should contain both delay time and original ETA
        """
        # Preprocess features
        X_processed = self.preprocess_features(X)
        
        # Split data into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(
            X_processed, y, test_size=0.2, random_state=42
        )
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Calculate and print metrics
        train_pred = self.model.predict(X_train)
        val_pred = self.model.predict(X_val)
        
        print("Training Metrics:")
        print(f"MSE: {mean_squared_error(y_train, train_pred):.2f}")
        print(f"R2 Score: {r2_score(y_train, train_pred):.2f}")
        
        print("\nValidation Metrics:")
        print(f"MSE: {mean_squared_error(y_val, val_pred):.2f}")
        print(f"R2 Score: {r2_score(y_val, val_pred):.2f}")
        
        return self
    
    def predict(self, X):
        """
        Predict delay and adjusted ETA for new data
        """
        X_processed = self.preprocess_features(X)
        predictions = self.model.predict(X_processed)
        return predictions
    
    def feature_importance(self, feature_names):
        """
        Plot feature importance
        """
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        plt.figure(figsize=(10, 6))
        plt.title("Feature Importances for Flight Delay Prediction")
        plt.bar(range(len(importances)), importances[indices])
        plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45)
        plt.tight_layout()
        return plt

# Example usage:
if __name__ == "__main__":
    # Sample data
    sample_data = pd.DataFrame({
        'scheduled_departure_time': np.random.randint(0, 1440, 1000),  # minutes since midnight
        'distance': np.random.randint(100, 3000, 1000),
        'day_of_week': np.random.randint(0, 7, 1000),
        'month': np.random.randint(1, 13, 1000),
        'aircraft_age': np.random.randint(0, 20, 1000),
        'weather_condition': np.random.randint(0, 4, 1000),
        'is_holiday': np.random.randint(0, 2, 1000)
    })
    
    # Sample delays (in minutes)
    sample_delays = np.random.exponential(30, 1000)  # Most delays are short, with some longer ones
    
    # Initialize and train model
    predictor = FlightDelayPredictor(max_depth=8)
    predictor.train(sample_data, sample_delays)
    try:
        scheduledDeparture = st.number_input("Enter Scheduled Departure Time")
        Distance = st.slider("Enter Distance of Flight (Nautical Miles)", min_value=0,max_value=10000)
        dayofWeek = st.text_input("Enter day (ex. Monday)")
        if dayofWeek.lower() == "sunday":
            Day_ofWeek = 0
        if dayofWeek.lower() == "monday":
            Day_ofWeek = 1
        if dayofWeek.lower() == "tuesday":
            Day_ofWeek = 2
        if dayofWeek.lower() == "wednesday":
            Day_ofWeek = 3
        if dayofWeek.lower() == "thursday":
            Day_ofWeek = 4
        if dayofWeek.lower() == "friday":
            Day_ofWeek = 5
        if dayofWeek.lower() == "saturday":
            Day_ofWeek = 6
        
        Month = st.text_input("Enter Month: (Ex. January)")
        if Month.lower() == "january":
            user_Month = 0
        if Month.lower() == "febuary":
            user_Month = 1
        if Month.lower() == "march":
            user_Month = 2
        if Month.lower() == "april":
            user_Month = 3
        if Month.lower() == "may":
            user_Month = 4
        if Month.lower() == "june":
            user_Month = 5
        if Month.lower() == "july":
            user_Month = 6
        if Month.lower() == "august":
            user_Month = 7
        if Month.lower() == "september":
            user_Month = 8
        if Month.lower() == "october":
            user_Month = 9
        if Month.lower() == "november":
            user_Month = 10
        if Month.lower() == "december":
            user_Month = 11

        Aircraft_Age = st.slider("Enter Age of Aircraft",min_value=0,max_value=30)
        weather = st.selectbox("Select Weather Condition", ["Light Rain"])
        if weather == "Light Rain":
            weatherint = 1
        Holiday = st.radio("Is it a holiday?",["Yes", "No"])
        if Holiday == 'Yes':
            boolholiday = 1
        else:
            boolholiday = 0
        # Make predictions for new flights
        new_flight = pd.DataFrame({
            'scheduled_departure_time': [scheduledDeparture],  # noon
            'distance': [Distance],
            'day_of_week': [Day_ofWeek],  # Tuesday
            'month': [user_Month],  # July
            'aircraft_age': [Aircraft_Age],
            'weather_condition': [weatherint],  # light rain
            'is_holiday': [boolholiday]  # not a holiday
        })
    except Exception as ERROR:
        st.error("Some Unknown Error Occured")

    def PredictDelay():
        predicted_delay = predictor.predict(new_flight)
        st.sidebar.write(f"\nPredicted delay for new flight: {predicted_delay[0]:.1f} minutes")
    st.button('PREDICT DELAY', on_click=PredictDelay)

