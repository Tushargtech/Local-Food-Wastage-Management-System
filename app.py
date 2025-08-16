import streamlit as st
import sqlite3
import pandas as pd
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Local Food Wastage Management System",
    page_icon="🍎",
    layout="wide"
)

# --- DATABASE CONNECTION ---
def create_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect("food_wastage.db")
    return conn

def run_query(query):
    """Runs a SQL query that fetches data and returns a DataFrame."""
    conn = create_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def execute_query(query, params=()):
    """Executes a query that modifies the database (INSERT, UPDATE, DELETE)."""
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    finally:
        conn.close()

# --- APP HEADER ---
st.title("🍎 Local Food Wastage Management System")
st.markdown("A platform connecting surplus food from providers to those in need, reducing waste and fighting hunger.")

# --- SIDEBAR FOR NAVIGATION ---
st.sidebar.title("Navigation Menu")
page = st.sidebar.radio("Go to:", [
    "📈 Analytics Dashboard",
    "🔍 Find Food & View Listings",
    "📝 Manage Data (CRUD)"
])

# ==============================================================================
# PAGE 1: ANALYTICS DASHBOARD
# ==============================================================================
if page == "📈 Analytics Dashboard":
    st.header("📈 Analytics Dashboard")
    st.markdown("Select a question to run a SQL query and see the results.")

    query_dict = {
        # --- Food Providers & Receivers ---
        "1. How many food providers and receivers are there in each city?": """
            SELECT City, 'Providers' AS Type, COUNT(Provider_ID) AS Count FROM providers_data GROUP BY City
            UNION ALL
            SELECT City, 'Receivers' AS Type, COUNT(Receiver_ID) AS Count FROM receivers_data GROUP BY City
            ORDER BY City, Type;
        """,
        "2. Which type of food provider contributes the most food (by quantity)?": """
            SELECT p.Type, SUM(fl.Quantity) AS TotalQuantity
            FROM providers_data p
            JOIN food_listings_data fl ON p.Provider_ID = fl.Provider_ID
            GROUP BY p.Type ORDER BY TotalQuantity DESC;
        """,
        "3. Which receivers have claimed the most food items?": """
            SELECT r.Name, COUNT(c.Claim_ID) AS NumberOfClaims
            FROM receivers_data r JOIN claims_data c ON r.Receiver_ID = c.Receiver_ID
            GROUP BY r.Name ORDER BY NumberOfClaims DESC LIMIT 10;
        """,
        # --- Food Listings & Availability ---
        "4. What is the total quantity of all available food?": "SELECT SUM(Quantity) AS TotalAvailableFood FROM food_listings_data;",
        "5. Which city has the highest number of food listings?": "SELECT Location, COUNT(Food_ID) AS NumberOfListings FROM food_listings_data GROUP BY Location ORDER BY NumberOfListings DESC;",
        "6. What are the most commonly available food types?": "SELECT Food_Type, COUNT(Food_ID) AS Count FROM food_listings_data GROUP BY Food_Type ORDER BY Count DESC;",
        # --- Claims & Distribution ---
        "7. How many claims have been made for each food item?": """
            SELECT fl.Food_Name, COUNT(c.Claim_ID) AS NumberOfClaims
            FROM food_listings_data fl LEFT JOIN claims_data c ON fl.Food_ID = c.Food_ID
            GROUP BY fl.Food_Name ORDER BY NumberOfClaims DESC;
        """,
        "8. Which provider has the highest number of successful ('Completed') claims?": """
            SELECT p.Name AS Provider, COUNT(c.Claim_ID) AS SuccessfulClaims
            FROM claims_data c
            JOIN food_listings_data fl ON c.Food_ID = fl.Food_ID
            JOIN providers_data p ON fl.Provider_ID = p.Provider_ID
            WHERE c.Status = 'Completed'
            GROUP BY Provider ORDER BY SuccessfulClaims DESC;
        """,
        "9. What is the percentage distribution of claim statuses?": "SELECT Status, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims_data) AS Percentage FROM claims_data GROUP BY Status;",
        # --- Analysis & Insights ---
        "10. What is the average quantity of food claimed per receiver?": """
            SELECT r.Name, AVG(fl.Quantity) AS AvgQuantityClaimed
            FROM claims_data c
            JOIN receivers_data r ON c.Receiver_ID = r.Receiver_ID
            JOIN food_listings_data fl ON c.Food_ID = fl.Food_ID
            GROUP BY r.Name ORDER BY AvgQuantityClaimed DESC;
        """,
        "11. Which meal type is claimed the most?": """
            SELECT fl.Meal_Type, COUNT(c.Claim_ID) AS NumberOfClaims
            FROM claims_data c JOIN food_listings_data fl ON c.Food_ID = fl.Food_ID
            GROUP BY fl.Meal_Type ORDER BY NumberOfClaims DESC;
        """,
        "12. What is the total quantity of food donated by each provider?": """
            SELECT p.Name, SUM(fl.Quantity) AS TotalQuantityDonated
            FROM providers_data p JOIN food_listings_data fl ON p.Provider_ID = fl.Provider_ID
            GROUP BY p.Name ORDER BY TotalQuantityDonated DESC;
        """,
        "13. List all food items expiring in the next 3 days.": f"""
            SELECT Food_Name, Quantity, Expiry_Date, Location
            FROM food_listings_data
            WHERE Expiry_Date BETWEEN DATE('now') AND DATE('now', '+3 days')
            ORDER BY Expiry_Date ASC;
        """,
        "14. What is the busiest day of the week for making claims?": """
            SELECT CASE STRFTIME('%w', Timestamp)
                WHEN '0' THEN 'Sunday' WHEN '1' THEN 'Monday' WHEN '2' THEN 'Tuesday'
                WHEN '3' THEN 'Wednesday' WHEN '4' THEN 'Thursday' WHEN '5' THEN 'Friday'
                ELSE 'Saturday' END as DayOfWeek, COUNT(Claim_ID) AS NumberOfClaims
            FROM claims_data GROUP BY DayOfWeek ORDER BY NumberOfClaims DESC;
        """,
        "15. What is the contact info for all providers?": "SELECT Name, Type, Address, City, Contact FROM providers_data ORDER BY City, Name;"
    }

    selected_question = st.selectbox("Select a question to analyze:", list(query_dict.keys()))
    
    # Get the SQL query string for the selected question
    sql_query = query_dict[selected_question]

    # **NEW FEATURE**: Display the SQL query in an expander
    with st.expander("View the SQL Query for this analysis"):
        st.code(sql_query, language='sql')
    
    # Execute the query and display the results
    df = run_query(sql_query)
    st.dataframe(df, use_container_width=True)
    
    if len(df.columns) == 2 and df.shape[0] > 1:
        st.bar_chart(df.set_index(df.columns[0]))

# ==============================================================================
# PAGE 2: FIND FOOD & VIEW LISTINGS (with Filters)
# ==============================================================================
elif page == "🔍 Find Food & View Listings":
    st.header("🔍 Find Food Donations")
    st.markdown("Filter available food listings to find what you need.")

    st.sidebar.header("Apply Filters")
    
    cities = run_query("SELECT DISTINCT City FROM providers_data ORDER BY City;")['City'].tolist()
    provider_types = run_query("SELECT DISTINCT Type FROM providers_data ORDER BY Type;")['Type'].tolist()
    food_types = run_query("SELECT DISTINCT Food_Type FROM food_listings_data WHERE Food_Type IS NOT NULL ORDER BY Food_Type;")['Food_Type'].tolist()
    meal_types = run_query("SELECT DISTINCT Meal_Type FROM food_listings_data WHERE Meal_Type IS NOT NULL ORDER BY Meal_Type;")['Meal_Type'].tolist()

    selected_city = st.sidebar.selectbox("City", ["All"] + cities)
    selected_provider_type = st.sidebar.selectbox("Provider Type", ["All"] + provider_types)
    selected_food_type = st.sidebar.selectbox("Food Category", ["All"] + food_types)
    selected_meal_type = st.sidebar.selectbox("Meal Type", ["All"] + meal_types)

    base_query = """
        SELECT fl.Food_Name, fl.Quantity, fl.Expiry_Date, p.Name AS Provider, 
               p.Type AS ProviderType, p.City, p.Address, p.Contact, fl.Meal_Type, fl.Food_Type
        FROM food_listings_data fl
        JOIN providers_data p ON fl.Provider_ID = p.Provider_ID
    """
    
    conditions = []
    if selected_city != "All": conditions.append(f"p.City = '{selected_city}'")
    if selected_provider_type != "All": conditions.append(f"p.Type = '{selected_provider_type}'")
    if selected_food_type != "All": conditions.append(f"fl.Food_Type = '{selected_food_type}'")
    if selected_meal_type != "All": conditions.append(f"fl.Meal_Type = '{selected_meal_type}'")

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)
    
    base_query += " ORDER BY fl.Expiry_Date ASC;"

    filtered_df = run_query(base_query)
    st.dataframe(filtered_df, use_container_width=True)
    st.info(f"Showing {len(filtered_df)} listings based on your filters.")

# ==============================================================================
# PAGE 3: MANAGE DATA (CRUD Operations)
# ==============================================================================
elif page == "📝 Manage Data (CRUD)":
    st.header("📝 Manage Data")
    st.markdown("Add, update, or delete records in the database.")

    tab1, tab2, tab3 = st.tabs(["➕ Add Listing", "🔄 Update Claim", "❌ Delete Listing"])

    with tab1:
        st.subheader("Add a New Food Listing")
        providers = run_query("SELECT Provider_ID, Name FROM providers_data;")
        provider_dict = {name: id for id, name in zip(providers['Provider_ID'], providers['Name'])}

        with st.form("add_food_form", clear_on_submit=True):
            food_name = st.text_input("Food Name")
            quantity = st.number_input("Quantity", min_value=1)
            expiry_date = st.date_input("Expiry Date", min_value=datetime.date.today())
            selected_provider_name = st.selectbox("Provider", options=provider_dict.keys())
            
            submitted = st.form_submit_button("Add Listing")
            if submitted:
                provider_id = provider_dict[selected_provider_name]
                max_id_df = run_query("SELECT MAX(Food_ID) as max_id FROM food_listings_data")
                new_id = int(max_id_df['max_id'].iloc[0] or 0) + 1
                
                query = "INSERT INTO food_listings_data (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID) VALUES (?, ?, ?, ?, ?)"
                execute_query(query, (new_id, food_name, quantity, str(expiry_date), provider_id))
                st.success("Food listing added successfully!")

    with tab2:
        st.subheader("Update a Claim's Status")
        pending_claims = run_query("SELECT Claim_ID, Food_ID FROM claims_data WHERE Status = 'Pending';")
        
        if not pending_claims.empty:
            claim_id_to_update = st.selectbox("Select a Pending Claim ID:", options=pending_claims['Claim_ID'])
            new_status = st.selectbox("New Status:", ["Completed", "Cancelled"])
            
            if st.button("Update Status"):
                query = "UPDATE claims_data SET Status = ? WHERE Claim_ID = ?"
                execute_query(query, (new_status, claim_id_to_update))
                st.success(f"Claim {claim_id_to_update} status updated to {new_status}.")
                st.rerun()
        else:
            st.info("No pending claims to update.")

    with tab3:
        st.subheader("Delete a Food Listing")
        listings = run_query("SELECT Food_ID, Food_Name FROM food_listings_data ORDER BY Food_ID;")
        
        if not listings.empty:
            listing_to_delete = st.selectbox("Select a listing to delete:", options=listings['Food_ID'], format_func=lambda x: f"ID: {x} - {listings.loc[listings['Food_ID'] == x, 'Food_Name'].iloc[0]}")
            
            if st.button("DELETE THIS LISTING PERMANENTLY", type="primary"):
                st.warning(f"This will delete listing {listing_to_delete} and any associated claims.")
                execute_query("DELETE FROM claims_data WHERE Food_ID = ?", (listing_to_delete,))
                execute_query("DELETE FROM food_listings_data WHERE Food_ID = ?", (listing_to_delete,))
                st.success(f"Listing {listing_to_delete} has been deleted.")
                st.rerun()
        else:
            st.info("No listings available to delete.")