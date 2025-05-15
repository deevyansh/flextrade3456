import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
from datetime import datetime, time



def preprocess_data(data_1):

    data = data_1.copy()

    # Add time-related features
    data['hour'] = data.index.hour
    data['dayofweek'] = data.index.dayofweek
    data['quarter'] = data.index.quarter
    data['month'] = data.index.month
    data['year'] = data.index.year
    data['dayofyear'] = data.index.dayofyear
    data['dayofmonth'] = data.index.day
    data['weekofyear'] = data.index.isocalendar().week

    # Drop unnecessary columns
    data = data.drop(columns=[
        'SpotPriceDKK', 'ImbalancePriceEUR',
        'ImbalancePriceDKK',
        'mFRRUpActBal', 'mFRRDownActBal', 'year'
    ])
    return data

def train_and_predict(data, start_date, start_time, end_date, end_time,target_column):
    # Combine date and time into a single datetime object
    start_datetime = pd.to_datetime(f"{start_date} {start_time}")
    end_datetime = pd.to_datetime(f"{end_date} {end_time}")

    # Split data into train and test sets
    train = data.loc[data.index < start_datetime]
    test = data.loc[(data.index >= start_datetime) & (data.index <= end_datetime)]

    FEATURES = data.columns.drop(['BalancingPowerPriceUpEUR','BalancingPowerPriceDownEUR' ]).tolist()
    TARGET = target_column

    X_train = train[FEATURES]
    y_train = train[TARGET]
    X_test = test[FEATURES]
    y_test = test[TARGET]

    # Train the model
    reg = xgb.XGBRegressor(
        base_score=0.5, booster='gbtree',
        n_estimators=1000, early_stopping_rounds=50,
        objective='reg:squarederror', max_depth=3,
        learning_rate=0.01
    )
    reg.fit(X_train, y_train, eval_set=[(X_train, y_train), (X_test, y_test)], verbose=100)

    # Feature importance plot
    fi = pd.DataFrame(data=reg.feature_importances_, index=reg.feature_names_in_, columns=['importance'])
    st.subheader("Feature Importance")
    st.bar_chart(fi.sort_values('importance'))

    # Forecast on Test Set
    test = test.copy()  # Ensure test is a standalone copy
    test['prediction'] = reg.predict(X_test)

    # Merge predictions for visualization
    data = data.merge(test[['prediction']], how='left', left_index=True, right_index=True)
    filtered_data = data.loc[(data.index >= start_datetime) & (data.index <= end_datetime), 'BalancingPowerPriceUpEUR']
    # Display predicted values in a table if the range contains 5 or fewer data points
    if len(test) <= 5:
        st.subheader("Predicted Values for Selected Date Range")
        predictions_df = test[['prediction']]
        st.write(predictions_df)
    else:
        # Plot actual vs predicted if range has more than 5 data points
        st.subheader("Predictions vs Actual Data")
        fig, ax = plt.subplots(figsize=(15, 5))
        #data['BalancingPowerPriceUpEUR'].plot(ax=ax, label='Truth Data')
        filtered_data.plot(ax=ax, label='Truth Data')
        test['prediction'].plot(ax=ax, style='.', label='Predictions')
        plt.legend()
        ax.set_title('Raw Data and Predictions')
        st.pyplot(fig)

    # Evaluate model performance
    mae = mean_absolute_error(y_test, test['prediction'])
    mape = np.mean(np.abs((y_test - test['prediction']) / y_test)) * 100
    rmse = np.sqrt(mean_squared_error(y_test, test['prediction']))
    numerator = np.sum((y_test - test['prediction']) ** 2)
    denominator = np.sum(y_test ** 2)
    u2 = numerator / denominator

    # Display metrics as a table
    st.subheader("Model Evaluation Metrics")

    # Create a DataFrame with the evaluation metrics
    metrics = {
        'Metric': ['Mean Absolute Error (MAE)', 'Mean Absolute Percentage Error (MAPE)',
                   'Root Mean Square Error (RMSE)', 'Theil\'s U²'],
        'Value': [mae, f"{mape:.2f}%", rmse, u2]
    }

    metrics_df = pd.DataFrame(metrics)

    # Display the table
    st.write(metrics_df)

def display():
    st.title("Prediction Section")

    # Check if data exists in session state
    if "uploaded_data_1" not in st.session_state:
        st.warning("No data available. Please upload data on the Home page first.")
        return

    # Retrieve the data from session state
    data = st.session_state["uploaded_data_1"]

    # Preprocess the data
    data = preprocess_data(data)

    # Display the data preview
    st.subheader("Data Preview")
    st.dataframe(data)
    # Dropdown for selecting the target column, restricted to ID1, ID2, ID3
    st.subheader("Select Target Column")
    target_column = st.selectbox(
        "Choose the target column for prediction:",
        options=[col for col in ['BalancingPowerPriceUpEUR','BalancingPowerPriceDownEUR'] if col in data.columns],
        index=0
    )
    # Select a start date and time
    start_date = st.date_input("Select Start Date", value=datetime(2024, 10, 1))
    start_time = st.time_input("Select Start Time", value=time(0, 0))

    # Select an end date and time
    end_date = st.date_input("Select End Date", value=datetime(2024, 10, 6))
    end_time = st.time_input("Select End Time", value=time(0, 0))

    # Trigger prediction
    if st.button("Run Prediction"):
        train_and_predict(data, start_date, start_time, end_date, end_time, target_column)

display()