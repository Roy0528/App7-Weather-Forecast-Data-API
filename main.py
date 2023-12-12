import streamlit as st
import plotly.express as px
from backend import get_data

# Add title, text input, slider, selectbox, and subheader
st.title("Weather Forecast for the Next Days")

place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")
option = st.selectbox("Select data to view",
                      ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} days in {place}")

if place:
    try:
        # Get the temperature/sky data
        filtered_data = get_data(place, days)

        if option == "Temperature":
            temperatures = [data["main"]["temp"] - 273.15 for data in filtered_data]
            dates = [data["dt_txt"] for data in filtered_data]
            # Create a temperature plot
            fig = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (°C)"})
            st.plotly_chart(fig)

        if option == "Sky":
            sky_condition = [data["weather"][0]["main"] for data in filtered_data]
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png", "Snow": "images/snow.png"}
            image_path = [images[condition] for condition in sky_condition]
            st.image(image_path, width=115)
    except KeyError:
        st.warning("That place does not exist")