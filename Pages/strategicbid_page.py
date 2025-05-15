import streamlit as st
import pandas as pd
import os

def display():
    st.title("Submit Strategic Bid")
    main_option = st.radio("How many bids you want to make", ["Single", "Multiple"])

    # Load data
    file_path = "Data/optimalhours_with_values.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        st.error(f"File '{file_path}' not found. Please make sure the file exists in the correct directory.")
        st.stop()

    # Preprocess data
    df['Hour_x'] = pd.to_datetime(df['Hour_x'])
    df['Date'] = df['Hour_x'].dt.date
    df['Hour'] = df['Hour_x'].dt.hour
    df['Month'] = df['Hour_x'].dt.month
    df['Year'] = df['Hour_x'].dt.year

    if main_option == "Single":
        input_date = st.date_input("Bidding Date")
        date = input_date.day
        year = input_date.year
        month = input_date.month

        price = st.number_input("Price")
        quantity = st.number_input("Quantity")

        filtered_df = df[(df['Year'] == year) & (df['Month'] == month) & (df['Date'] == input_date)]
        if filtered_df.empty:
            st.warning("No data available for the selected date.")
            st.stop()

        options = []
        for _, row in filtered_df.iterrows():
            options.append(
                f"Hour: {row['Hour']} | Decision: {row['Decision']} | Prescribed Quantity (kWh): {row['NewValue']} | Prescribed Price: {row['Price']}"
            )
        selected_option = st.radio("Select the Hour", options)

        if st.button("Final the Bid"):
            selected_hour = int(selected_option.split("Hour:")[1].split("|")[0].strip())

            # Extracting Prescribed Quantity and Price properly
            prescribed_quantity_str = selected_option.split("Prescribed Quantity (kWh):")[1].split("|")[0].strip()
            prescribed_price_str = selected_option.split("Prescribed Price:")[1].strip()

            # Converting to float for validation purposes
            prescribed_quantity = float(prescribed_quantity_str)
            # prescribed_price is used for internal validation only
            prescribed_price = float(prescribed_price_str)

            if quantity < 0 or quantity > prescribed_quantity:
                st.error("Please enter a valid quantity within the prescribed limit.")
            else:
                st.success("Bid Submitted Successfully")
                # Display only the required details
                st.write(f"Price: {price}, Quantity: {quantity}, Date: {date}/{month}/{year}, Hour: {selected_hour}")


    else:
        input_date = st.date_input("Bidding Date")
        date = input_date.day
        year = input_date.year
        month = input_date.month

        price1_widget, quantity1_widget = st.columns([1, 1])
        price2_widget, quantity2_widget = st.columns([1, 1])
        price3_widget, quantity3_widget = st.columns([1, 1])

        price1 = price1_widget.number_input("Price 1", min_value=0.0)
        price2 = price2_widget.number_input("Price 2", min_value=0.0)
        price3 = price3_widget.number_input("Price 3", min_value=0.0)
        quantity1 = quantity1_widget.number_input("Quantity 1", min_value=0.0)
        quantity2 = quantity2_widget.number_input("Quantity 2", min_value=0.0)
        quantity3 = quantity3_widget.number_input("Quantity 3", min_value=0.0)

        filtered_df = df[(df['Year'] == year) & (df['Month'] == month) & (df['Date'] == input_date)]
        if filtered_df.empty:
            st.warning("No data available for the selected date.")
            st.stop()

        options = []
        for _, row in filtered_df.iterrows():
            options.append(
                f"Hour: {row['Hour']} | Decision: {row['Decision']} | Prescribed Quantity (kWh): {row['NewValue']} | Prescribed Price: {row['Price']}"
            )

        selected_hours = []
        quantities = [quantity1, quantity2, quantity3]
        prices = [price1, price2, price3]
        for option in options:
            if st.checkbox(option):
                selected_hours.append(option)

        if st.button("Final the Bid"):
            valid = True
            for i in range(len(selected_hours)):
                selected_hour = int(selected_hours[i].split("Hour:")[1].split("|")[0].strip())

                # Extract and convert prescribed values
                prescribed_quantity_str = selected_hours[i].split("Prescribed Quantity (kWh):")[1].split("|")[0].strip()
                prescribed_price_str = selected_hours[i].split("Prescribed Price:")[1].strip()

                prescribed_quantity = float(prescribed_quantity_str)
                prescribed_price = float(prescribed_price_str)  # Used internally

                if quantities[i] < 0 or quantities[i] > prescribed_quantity:
                    valid = False
                    st.error(f"Please enter a valid quantity for Hour: {selected_hour}")

            if valid:
                st.success("Bid Submitted Successfully")
                # Display only required details for each bid
                for i in range(len(selected_hours)):
                    selected_hour = int(selected_hours[i].split("Hour:")[1].split("|")[0].strip())
                    st.write(
                        f"Price: {prices[i]}, Quantity: {quantities[i]}, Date: {date}/{month}/{year}, Hour: {selected_hour}")

display()
