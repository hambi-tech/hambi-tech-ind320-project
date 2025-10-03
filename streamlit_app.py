import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data from the file
data = pd.read_csv('open-meteo-subset.csv')  

# Convert 'time' column to datetime format
data['time'] = pd.to_datetime(data['time'])

# Extract month from the 'time' column
data['month'] = data['time'].dt.month_name()

# Sidebar for navigation
st.sidebar.title("Dashboard Navigation")
page = st.sidebar.radio("Choose Page", ["Home", "Data", "Plot"])

# Home Page
if page == "Home":
    st.title("Welcome to the IND320 Data Dashboard")
    st.write("This is a simple Streamlit app for visualizing and exploring the data.")
    st.write("Use the sidebar to navigate between pages.")

# Data Page: Show the imported data
if page == "Data":
    st.title("Data Preview")
    st.write("Here is the data loaded from the `open-meteo-subset.csv` file:")
    st.dataframe(data)

# Plot Page: Show the plots
if page == "Plot":
    st.title("Data Plotting")
    
    # Dropdown for selecting a column or all columns
    column_choice = st.selectbox("Select a column to plot", ["All"] + list(data.columns[1:]))

    # Selection slider to select a subset of months (default to the first month)
    months = data['month'].unique()
    selected_month = st.select_slider(
        "Select a month range",
        options=months,
        value=(months[0], months[0])  # Default to the first month
    )

    # Filter the data based on the selected month range
    filtered_data = data[(data['month'] >= selected_month[0]) & (data['month'] <= selected_month[1])]
    
    # Plotting logic based on column selection
    if column_choice == "All":
        # Plot all columns together
        st.write("Plotting all columns together:")
        filtered_data.plot(x='time', figsize=(10, 6))
        plt.title('All Columns Plot')
        plt.xlabel('Time')
        plt.ylabel('Values')
        st.pyplot()

    else:
        # Plot the selected column
        st.write(f"Plotting the column: {column_choice}")
        plt.figure(figsize=(10, 6))
        plt.plot(filtered_data['time'], filtered_data[column_choice])
        plt.title(f'{column_choice} Plot')
        plt.xlabel('Time')
        plt.ylabel(f'{column_choice} Values')
        st.pyplot()
