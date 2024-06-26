from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as data
import yfinance as yf
from keras.models import load_model
import streamlit as st
from datetime import date


start = '2010-01-01'
end = date.today()

st.title("CRYPTOCURRENCY FUTURE PRICE PREDICTION")

user_input = st.text_input("Enter Crypto Ticker", "BTC-INR")

df = yf.download(user_input, start, end)


# Raw Data
st.subheader("Raw Data upto Present Day")
st.write(df)


# Describing Data

st.subheader("Short Analysis of the Data")
st.write(df.describe())


# Visualisations

st.subheader("Closing Price v/s Time Chart")
fig0 = plt.figure(figsize=(12, 6))
plt.plot(df.Close)
plt.xlabel("Time")
plt.ylabel("Price ($)")
st.pyplot(fig0)


st.subheader("Closing Price v/s Time Chart with 100MA")
ma100 = df.Close.rolling(100).mean()
fig1 = plt.figure(figsize=(12, 6))
plt.plot(df.Close)
plt.plot(ma100, color="red", label="100MA")
plt.xlabel("Time")
plt.ylabel("Price ($)")
plt.legend()
st.pyplot(fig1)


st.subheader("Closing Price v/s Time Chart with 100MA and 200MA")
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig2 = plt.figure(figsize=(12, 6))
plt.plot(df.Close)
plt.plot(ma100, color="red", label="100MA")
plt.plot(ma200, color="green", label="200MA")
plt.xlabel("Time")
plt.ylabel("Price ($)")
plt.legend()
st.pyplot(fig2)


# Splitting Data for training

data_training = pd.DataFrame(df["Close"][0:int(len(df)*0.80)])
data_testing = pd.DataFrame(df["Close"][int(len(df)*0.80):int(len(df))])

# Scalling the data between 0 and 1

scaler = MinMaxScaler(feature_range=(0, 1))

data_training_array = scaler.fit_transform(data_training)

# Loading my ML Model

model = load_model("cryptocurrency_future_price_prediction")

# Testing Part

past_100_days = data_training.tail(100)
final_df = pd.concat([past_100_days, data_testing])
input_data = scaler.fit_transform(final_df)

x_test = []
y_test = []

for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i, 0])

x_test, y_test = np.array(x_test), np.array(y_test)
y_predicted = model.predict(x_test)

y_test = pd.DataFrame(y_test)

y_predicted = scaler.inverse_transform(y_predicted)
y_test = scaler.inverse_transform(y_test)


# Visualisation Final

df = df.reset_index()
new_date = df.loc[int(len(df)*0.80):int(len(df)), "Date"]

st.subheader("Original Price v/s Predicted Price")
fig3 = plt.figure(figsize=(12, 6))
plt.plot(new_date, y_test, "blue", label="Original Price")
plt.plot(new_date, y_predicted, "green", label="Prediction")
plt.xlabel("Time")
plt.ylabel("Price ($)")
plt.legend()
st.pyplot(fig3)
