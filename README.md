# Meteo Viator - The Virtual Weather Time Traveler

Meteo Viator (Latin for "Weather Traveler") is a simple and minimalist Python web application designed to provide retrospective weather data for any specified location and time period. Developed as a project for the first MiniHackathon organized by Kevin Chromik, this tool enables users to explore and compare historical weather data with ease.

## Project Overview

Meteo Viator allows users to input a city, postal code, start date, and end date, and in return, it provides a comprehensive summary of the weather during that period. The application fetches historical weather data from the Open-Meteo API, displaying the following key metrics:

- **Average Temperature**
- **Average Wind Speed**
- **Average Daily Sunshine Duration**

In addition to these summaries, the application presents a detailed table of hourly weather data and a line chart showing temperature trends over the selected period.

### Key Features

- **Retrospective Weather Analysis:** Unlike traditional weather applications focused on forecasts, Meteo Viator allows users to explore and compare past weather conditions.
- **Interactive User Interface:** Developed using Streamlit, the application features an intuitive interface with animations, including a fun "raining sun-clouds" effect when fetching data.
- **Data Visualization:** The app provides both tabular data and a visually appealing line chart to illustrate temperature variations.

## Getting Started

### Prerequisites

Before running the application, ensure that you have the following Python libraries installed:

```bash
pip install streamlit pandas requests numpy altair requests-cache streamlit-extras
```

### Running the Application

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/meteo-viator.git
   cd meteo-viator
   ```

2. **Run the application using Streamlit:**

   ```bash
   streamlit run app.py
   ```

   By default, the application is set to fetch weather data for Freiburg, Germany, since the Geocoder API is not supported on Streamlit Cloud. However, you can input any city and postal code as needed.

3. **Explore the App:**
   
   Visit the local Streamlit server in your browser to interact with the application. Enter your desired city, postal code, start date, and end date, then click on the "Fetch Weather Data" button to retrieve and visualize historical weather data.

### Key Components of the Application

- **City and Date Input:** Users can specify the location and time range for which they want to retrieve weather data.
- **Weather Summary:** Displays the average temperature, wind speed, and daily sunshine duration for the specified period.
- **Data Table and Line Chart:** The app presents a detailed table with hourly weather data and a temperature trend line chart for easy visualization.

## Example Output

Below is an example of the application in action:


## Deployment

You can also explore the application directly via Streamlit without setting up a local environment:

➡️ [Try it on Streamlit](https://minihackathon-meteoviator.streamlit.app/)

## Acknowledgements

- **Open-Meteo API:** This project uses historical weather data provided by the Open-Meteo API.
- **Streamlit:** The application is built using the Streamlit framework for interactive data visualization.
- **Flaticon:** The sun-cloud icon used in the app was sourced from Flaticon, created by [@iconixar](https://www.flaticon.com/authors/iconixar).

