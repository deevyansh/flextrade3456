import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
def display():
    # Title of the app
    st.title("Data Parameters - Home")
    st.subheader("Grid Data Parameters")
    # File uploader widget for the first file
    uploaded_file_1 = st.file_uploader("Upload a CSV file (Grid Data)", type=["csv"])
    st.subheader("Factory Data Parameters")
    # File uploader widget for the second file (e.g., factory data)
    uploaded_file_2 = st.file_uploader("Upload a CSV file (Factory Data)", type=["csv"])

    if uploaded_file_1:
        # Read the uploaded first CSV file (Grid Data)
        data_1 = pd.read_csv(uploaded_file_1)
        data_1 = data_1.drop(columns=[
            'Unnamed: 0', 'Unnamed: 0.1'])
        st.session_state["uploaded_data_1"] = data_1  # Save the first data in session state
        st.success("Grid Data file successfully uploaded and saved!")

        # Show the dataframe for Grid Data
        st.subheader("Grid Data Preview")
        st.dataframe(data_1)

        # Select columns to plot for Grid Data
        numeric_columns_1 = data_1.select_dtypes(include=["number"]).columns.tolist()

        if numeric_columns_1:
            st.subheader("Select Columns to Plot for Grid Data")

            # Select the date/time column if available
            datetime_columns_1 = data_1.select_dtypes(include=["datetime", "object"]).columns.tolist()
            if datetime_columns_1:
                selected_datetime_column_1 = st.selectbox("Select a Date/Time Column for Grid Data", datetime_columns_1)
                try:
                    # Convert to datetime and set as index
                    data_1[selected_datetime_column_1] = pd.to_datetime(data_1[selected_datetime_column_1])
                    data_1.set_index(selected_datetime_column_1, inplace=True)
                except Exception as e:
                    st.error(f"Error converting column to datetime: {e}")

            selected_columns_1 = st.multiselect("Choose numeric columns to plot for Grid Data", numeric_columns_1)

            if selected_columns_1:
                st.subheader("Generated Plot for Grid Data")
                fig, ax = plt.subplots()

                # Plot numeric columns for Grid Data
                data_1[selected_columns_1].plot(ax=ax)

                # Add formatting for the x-axis to show dates clearly
                ax.set_xlabel("Date/Time")
                plt.xticks(rotation=45)
                st.pyplot(fig)
            else:
                st.warning("Please select at least one column to generate a plot for Grid Data.")
        else:
            st.warning("No numeric columns found in the uploaded Grid Data CSV.")

    else:
        st.info("Awaiting Grid Data CSV file upload.")

    # Handle the second file (Factory Data)
    if uploaded_file_2:
        # Read the uploaded second CSV file (Factory Data)
        data_2 = pd.read_csv(uploaded_file_2)
        st.session_state["uploaded_data_2"] = data_2  # Save the second data in session state
        st.success("Factory Data file successfully uploaded and saved!")

        # Show the dataframe for Factory Data
        st.subheader("Factory Data Preview")
        st.dataframe(data_2)



        # Select columns to plot for Factory Data
        numeric_columns_2 = data_2.select_dtypes(include=["number"]).columns.tolist()

        if numeric_columns_2:
            st.subheader("Select Columns to Plot for Factory Data")

            # Select the date/time column if available
            datetime_columns_2 = data_2.select_dtypes(include=["datetime", "object"]).columns.tolist()
            if datetime_columns_2:
                selected_datetime_column_2 = st.selectbox("Select a Date/Time Column for Factory Data",
                                                          datetime_columns_2)
                try:
                    # Convert to datetime and set as index
                    data_2[selected_datetime_column_2] = pd.to_datetime(data_2[selected_datetime_column_2])
                    data_2.set_index(selected_datetime_column_2, inplace=True)
                except Exception as e:
                    st.error(f"Error converting column to datetime: {e}")

            selected_columns_2 = st.multiselect("Choose numeric columns to plot for Factory Data", numeric_columns_2)

            if selected_columns_2:
                st.subheader("Generated Plot for Factory Data")
                fig, ax = plt.subplots()

                # Plot numeric columns for Factory Data
                data_2[selected_columns_2].plot(ax=ax)

                # Add formatting for the x-axis to show dates clearly
                ax.set_xlabel("Date/Time")
                plt.xticks(rotation=45)
                st.pyplot(fig)
            else:
                st.warning("Please select at least one column to generate a plot for Factory Data.")
        else:
            st.warning("No numeric columns found in the uploaded Factory Data CSV.")

    else:
        st.info("Awaiting Factory Data CSV file upload.")
display()
