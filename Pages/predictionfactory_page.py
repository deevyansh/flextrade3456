import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
from datetime import datetime, time


def preprocess_data(data_2):

    data = data_2.copy()

    # Add time-related features
    data['hour'] = data.index.hour
    data['dayofweek'] = data.index.dayofweek
    data['quarter'] = data.index.quarter
    data['month'] = data.index.month
    #data['year'] = data.index.year
    data['dayofyear'] = data.index.dayofyear
    data['dayofmonth'] = data.index.day
    data['weekofyear'] = data.index.isocalendar().week

    # Drop unnecessary columns
    #data = data.drop(columns=[
     #'ID2','ID3'])
    return data


def train_and_predict(data, start_date, start_time, end_date, end_time,target_column):
    # Combine date and time into a single datetime object
    start_datetime = pd.to_datetime(f"{start_date} {start_time}")
    end_datetime = pd.to_datetime(f"{end_date} {end_time}")

    # Split data into train and test sets
    train = data.loc[data.index < start_datetime]
    test = data.loc[(data.index >= start_datetime) & (data.index <= end_datetime)]

    FEATURES = data.columns.drop(['ID1','ID2','ID3']).tolist()
    TARGET = target_column

    X_train = train[FEATURES]
    y_train = train[TARGET]
    X_test = test[FEATURES]
    y_test = test[TARGET]

    # Train the model
    print("Training of the xgb started")
    reg = xgb.XGBRegressor(
        booster='gbtree',
        objective='reg:squarederror',
        n_estimators=1000,                # Fewer boosting rounds (faster)
        learning_rate=0.01,              # Faster convergence
        max_depth=3,                     # Controls complexity
        early_stopping_rounds=20,        # Stops early if no improvement
        n_jobs=1,                        # Avoid multi-threading overhead in Streamlit
        verbosity=0                      # Disable logging to avoid UI slowdown
    )
    
    reg.fit(
       X_train, y_train,
       eval_set=[(X_test, y_test)],     # Only monitor test loss
       verbose=False                    # No per-iteration output
    )

    # Feature importance plot
    print("Training finished")
    fi = pd.DataFrame(data=reg.feature_importances_, index=reg.feature_names_in_, columns=['importance'])
    st.subheader("Feature Importance")
    st.bar_chart(fi.sort_values('importance'))

    # Forecast on Test Set
    test = test.copy()  # Ensure test is a standalone copy
    test['prediction'] = reg.predict(X_test)

    # Merge predictions for visualization
    data['prediction'] = test['prediction']

    # Filter data to plot range and downsample if necessary
    filtered_data = data.loc[(data.index >= start_datetime) & (data.index <= end_datetime), 'ID1']
    #filtered_data = filtered_data.resample('h').mean()  # Resample to hourly data

    # Display predicted values in a table if the range contains 5 or fewer data points
    if len(test) <= 5:
        st.subheader("Predicted Values for Selected Date Range")
        predictions_df = test[['prediction']]
        st.write(predictions_df)
    else:
        # Plot actual vs predicted if range has more than 5 data points
        st.subheader("Predictions vs Actual Data")
        fig, ax = plt.subplots(figsize=(15, 5))

        # Plot with limited ticks
        filtered_data.plot(ax=ax, label='Truth Data')
        test['prediction'].plot(ax=ax, style='.', label='Predictions')
        #ax.set_xticks(filtered_data.index[::100])  # Adjust tick frequency
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
    metrics = {
        'Metric': ['Mean Absolute Error (MAE)', 'Mean Absolute Percentage Error (MAPE)',
                   'Root Mean Square Error (RMSE)', 'Theil\'s U²'],
        'Value': [mae, f"{mape:.2f}%", rmse, u2]
    }
    metrics_df = pd.DataFrame(metrics)
    st.write(metrics_df)


def display():
    print("Hello i am in the prediction section")
    st.title("Prediction Section")

    # Check if data exists in session state
    if "uploaded_data_2" not in st.session_state:
        st.warning("No data available. Please upload data on the Home page first.")
        return

    # Retrieve the data from session state
    data2 = st.session_state["uploaded_data_2"]

    # Preprocess the data
    print("Data preprocessing started")
    data2 = preprocess_data(data2)
    print("Data preprocessing finished")

    # Display the data preview
    st.subheader("Data Preview")
    st.dataframe(data2)


    # Dropdown for selecting the target column, restricted to ID1, ID2, ID3
    st.subheader("Select Target Column")
    target_column = st.selectbox(
        "Choose the target column for prediction:",
        options=[col for col in ['ID1', 'ID2', 'ID3'] if col in data2.columns],
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
        print("Button pressed")
        train_and_predict(data2, start_date, start_time, end_date, end_time, target_column)
        print("training done")
display()
