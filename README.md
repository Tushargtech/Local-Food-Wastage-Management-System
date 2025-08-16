# 🍎 Local Food Wastage Management System

A data-driven web application built with Python and Streamlit to manage and analyze local food donations, connecting surplus food providers with those in need to reduce waste and combat food insecurity.

---

## 📋 Table of Contents
- [Problem Statement](#-problem-statement)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Setup & Installation](#-setup--installation)
- [How to Use](#-how-to-use)
- [Future Enhancements](#-future-enhancements)

---

## 🎯 Problem Statement

A significant amount of edible food is discarded daily by restaurants and grocery stores, while many people in our communities face food insecurity. This project aims to bridge that gap by providing a simple, centralized platform for the efficient redistribution of surplus food.

---

## ✨ Features

- **Analytics Dashboard:** An interactive dashboard with 15+ pre-defined SQL queries to analyze trends in food donations, claims, and provider contributions. Each analysis displays the SQL query for transparency.
- **Dynamic Food Listings:** A real-time view of all available food donations, with provider contact details to facilitate direct coordination.
- **Advanced Filtering:** Users can easily filter food listings by City, Provider Type, Food Category, and Meal Type to find exactly what they need.
- **Full CRUD Functionality:** A secure administrative page to perform Create, Read, Update, and Delete operations on the database records directly from the user interface.

---

## 🛠️ Tech Stack

- **Backend:** Python
- **Web Framework:** Streamlit
- **Database:** SQLite
- **Data Manipulation:** Pandas

---

## 🏗️ System Architecture

The application follows a simple and efficient data flow:

1.  **Data Ingestion:** A Python script (`load_data.py`) reads raw data from four CSV files and populates a self-contained SQLite database (`food_wastage.db`).
2.  **Backend Logic:** The main Streamlit application (`app.py`) connects to the SQLite database to execute SQL queries for fetching, analyzing, and modifying data.
3.  **Frontend Interface:** The Streamlit framework renders the user interface in the browser, allowing users to interact with the data through intuitive widgets and visualizations.

---

## 🚀 Setup & Installation

To run this project locally, please follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YourUsername/Local-Food-Wastage-Management-System.git](https://github.com/YourUsername/Local-Food-Wastage-Management-System.git)
    cd Local-Food-Wastage-Management-System
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create the Database:**
    Ensure your four CSV data files (`providers_data.csv`, etc.) are in the project folder. Then, run the data loading script:
    ```bash
    python load_data.py
    ```
    This will create the `food_wastage.db` file.

5.  **Run the Streamlit App:**
    ```bash
    streamlit run app.py
    ```
    The application will open in your web browser.

---

## 📖 How to Use

- **Navigate** between the three main pages using the sidebar menu.
- On the **Analytics Dashboard**, use the dropdown to select an analytical question and view the results.
- On the **Find Food** page, use the filters in the sidebar to narrow down the food listings.
- On the **Manage Data** page, use the tabs to add, update, or delete records.

---

## 🔮 Future Enhancements

- **User Authentication:** Create separate login systems for providers and receivers.
- **Live Map Integration:** Use geolocation to display food availability on an interactive map.
- **Automated Notifications:** Send alerts to receivers when new food is listed in their area.
- **Cloud Deployment:** Deploy the app to a service like Streamlit Community Cloud for public access.

---

_This project was created as part of a data analytics curriculum._
