import streamlit as st
import random
import sqlite3
import hashlib
import os


# ------------------------------
# DATABASE SETUP
# ------------------------------
conn = sqlite3.connect('farmer_data.db', check_same_thread=False)
c = conn.cursor()

# Create users table
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT,
    phone TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    address TEXT,
    land_proof TEXT,
    bank_details TEXT,
    farming_type TEXT,
    credit_history TEXT,
    verification_doc TEXT,
    interests TEXT,
    agreement TEXT,
    role TEXT NOT NULL,
    org_role TEXT,
    gov_id TEXT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)''')

# Create user credentials table (if needed for Aadhaar-based login)
c.execute('''CREATE TABLE IF NOT EXISTS user_credentials (
    aadhaar TEXT PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
)''')

# Create loan history table
c.execute('''CREATE TABLE IF NOT EXISTS loan_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aadhaar TEXT,
    name TEXT,
    amount REAL,
    status TEXT,
    Date DATETIME DEFAULT CURRENT_TIMESTAMP
)''')


# Create credit cards table
c.execute('''CREATE TABLE IF NOT EXISTS credit_cards (
    aadhaar TEXT,
    card_number TEXT,
    limit_amount REAL,
    activation_code TEXT,
    status TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS contributor_rates (
    id INTEGER PRIMARY KEY,
    contributor_username TEXT,
    preferred_rate REAL
)''')
c.execute('''CREATE TABLE IF NOT EXISTS contributor_rates (
    id INTEGER PRIMARY KEY,
    contributor_username TEXT,
    preferred_rate REAL
)
''')
c.execute('''CREATE TABLE IF NOT EXISTS contributor_rates (
    id INTEGER PRIMARY KEY,
    contributor_username TEXT,
    preferred_rate REAL
);
''')


conn.commit()


# ------------------------------
# HELPER FUNCTIONS
# ------------------------------

def hash_password(password):
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_login(username, password):
    """Verifies the username and password against the database."""
    hashed_pw = hash_password(password)
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
    user = c.fetchone()
    return user  # Return the user if login is successful, otherwise None


# ------------------------------
# STREAMLIT UI SETUP
# ------------------------------
st.set_page_config(page_title="Tenant Farmer Loan Management System", layout="wide")

# ------------------------------
# SIDEBAR MENU
# ------------------------------
sidebar_img_path = r"C:\Users\vidya\Downloads\WhatsApp Image 2025-03-25 at 9.52.01 AM.jpeg"  # Replace with your actual path

if os.path.exists(sidebar_img_path):
    st.sidebar.image(sidebar_img_path, use_container_width=True)
else:
    st.sidebar.error("❗ Sidebar image not found! Check the path.")

st.sidebar.title("🌱 HarvestPay - Tenant Farmer Loan System")
menu = st.sidebar.radio("Choose a feature:", [
    "Home", "Features", "Register", "Login", "Loan Application","Verification", "Feedback System"
])


# ------------------------------
# MAIN CONTENT BASED ON MENU SELECTION
# ------------------------------

if menu == "Home":
    # ------------------------------
    # HOME PAGE CONTENT
    # ------------------------------
    home_img_path = r"C:\Users\vidya\Downloads\WhatsApp Image 2025-03-25 at 9.52.01 AM (2).jpeg"

    if os.path.exists(home_img_path):
        st.image(home_img_path, use_container_width=True)
    else:
        st.error("❗ Home page image not found! Check the path.")
    st.title("🏡 Welcome to the Tenant Farmer Loan Management System")
    st.write("### Features available:")
    st.markdown(
        """
        - ✅ User Registration
        - 💸 Loan Application
        - 🤖 Risk Assessment
        - 💳 Credit Card Issuance
        - 🔐 Card Activation
        - 👤 User Profile Management
        - 📚 Loan History
        - 📝 Feedback System
        """
    )

elif menu == "Features":
    st.title("✨ System Features Overview")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 👤 User Registration")
        st.write("Register new users with roles and details.")

        st.markdown("#### 💸 Loan Application")
        st.write("Apply for loans by specifying the amount and details.")

        st.markdown("#### 🤖 Risk Assessment")
        st.write("AI-based risk analysis for loan approval.")

    with col2:
        st.markdown("#### 💳 Credit Card Issuance")
        st.write("Issue credit cards with set limits for users.")

        st.markdown("#### 🔐 Card Activation")
        st.write("Activate issued cards with one-time code.")

        st.markdown("#### 👤 User Profile Management")
        st.write("Manage and view user details.")

    with col3:
        st.markdown("#### 📚 Loan History")
        st.write("Track and manage previous loan applications.")

        st.markdown("#### 📝 Feedback System")
        st.write("Allow users to submit feedback on services.")

        st.markdown("#### 📊 Dashboard & Reporting")
        st.write("View statistics and loan summary reports.")

elif menu == "Register":
    st.title("User Registration")

    role = st.selectbox("Select Role", ["Farmer", "Contributor", "Admin"])

    full_name = st.text_input("Full Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    hashed_pw = hash_password(password)

    if role == "Farmer":
        age = st.number_input("Age", min_value=18, max_value=100)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        phone = st.text_input("Phone Number")
        address = st.text_area("Address")
        land_proof = st.file_uploader("Land Ownership Proof")
        bank_details = st.text_input("Bank Account Details")
        farming_type = st.text_input("Type of Farming")
        credit_history = st.text_area("Credit History")

        if st.button("Register Farmer"):
            if full_name and username and password and phone and age and gender and address and land_proof and bank_details and farming_type and credit_history:
                try:
                    c.execute('''INSERT INTO users (full_name, phone, age, gender, address, land_proof, bank_details, farming_type, credit_history, role, username, password)
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                              (full_name, phone, age, gender, address, land_proof.name if land_proof else None,
                               bank_details, farming_type, credit_history, role, username, hashed_pw))
                    conn.commit()
                    st.success("Farmer registered successfully! Please login.")
                except sqlite3.Error as e:
                    st.error(f"Database error: {e}")
            else:
                st.error("Please fill out all the required fields.")

    elif role == "Contributor":
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        verification_doc = st.file_uploader("Verification Document")
        interests = st.text_area("Areas of Interest")
        agreement = st.checkbox("I agree to the terms and compliance")
        preferred_rate = st.number_input("Preferred Rate of Interest (%)", min_value=0.0, max_value=20.0, step=0.1)

    if st.button("Register Contributor"):
        if full_name and username and password and phone and email and verification_doc and interests and agreement:
            if agreement:
                try:
                    # Insert contributor details into users table
                    c.execute('''INSERT INTO users (full_name, email, phone, verification_doc, interests, agreement, role, username, password)
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                              (full_name, email, phone, verification_doc.name if verification_doc else None,
                               interests, str(agreement), role, username, hashed_pw))
                    conn.commit()

                    # Insert preferred rate into contributor_rates table
                    c.execute('''INSERT INTO contributor_rates (contributor_username, preferred_rate)
                                 VALUES (?, ?)''', (username, preferred_rate))
                    conn.commit()
                    st.success("Contributor registered successfully! Please login.")
                except sqlite3.Error as e:
                    st.error(f"Database error: {e}")
            else:
                st.error("You must agree to the terms and compliance.")
        else:
            st.error("Please fill out all required fields.")

    elif role == "Admin":
        email = st.text_input("Email")
        contact_number = st.text_input("Contact Number")
        org_role = st.text_input("Role in Organization")
        gov_id = st.file_uploader("Government ID Proof")

        if st.button("Register Admin"):
            if full_name and username and password and contact_number and email and org_role and gov_id:
                try:
                    c.execute('''INSERT INTO users (full_name, email, phone, org_role, gov_id, role, username, password)
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                              (full_name, email, contact_number, org_role, gov_id.name if gov_id else None, role,
                               username, hashed_pw))
                    conn.commit()
                    st.success("Admin registered successfully! Please login.")
                except sqlite3.Error as e:
                    st.error(f"Database error: {e}")
            else:
                st.error("Please fill out all required fields.")

elif menu == "Login":
    st.title("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        user = verify_login(username, password)
        if user:
            st.success(f"Welcome back, {user[1]}! You are logged in as {user[14]}.")  # Changed index to 14 for 'role'
            # Store user information in session state for other pages
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['role'] = user[14]  # Role is at index 14

        else:
            st.error("Invalid username or password.")

# ------------------------------
# LOAN APPLICATION NAVIGATION
# ------------------------------
elif menu == "Loan Application":
    st.title("💸 Loan Application")

    # Check if the user is logged in as a farmer
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        role = st.session_state.get('role', None)
        if role == "Farmer":
            # Create columns for layout
            col1, col2 = st.columns([1, 4])  # Calculator on the left, main content on the right

            with col1:
                st.subheader("EMI Calculator")
                with st.expander("Calculate Your EMI"):
                    calculator_loan_amount = st.number_input("Loan Amount (₹)", min_value=1000.0, step=100.0, key="calculator_amount")
                    calculator_interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=20.0, step=0.1, key="calculator_rate")
                    calculator_repayment_period = st.selectbox("Repayment Period", ["6 months", "1 year", "2 years", "3 years", "5 years"], key="calculator_period")

                    if st.button("Calculate EMI", key="calculate_emi"):
                        # Convert repayment period to months
                        if calculator_repayment_period == "6 months":
                            months = 6
                        elif calculator_repayment_period == "1 year":
                            months = 12
                        elif calculator_repayment_period == "2 years":
                            months = 24
                        elif calculator_repayment_period == "3 years":
                            months = 36
                        elif calculator_repayment_period == "5 years":
                            months = 60

                        # Calculate EMI
                        monthly_interest_rate = (calculator_interest_rate / 100) / 12
                        emi = calculator_loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** months / ((1 + monthly_interest_rate) ** months - 1)
                        emi = round(emi, 2)

                        st.write(f"EMI: ₹{emi}")

            with col2:
                st.subheader("Apply for a Loan")

                # Loan Details
                purpose_of_loan = st.text_input("Purpose of Loan")
                loan_amount = st.number_input("Loan Amount (₹)", min_value=1000.0, step=100.0)
                repayment_period = st.selectbox("Repayment Period", ["6 months", "1 year", "2 years", "3 years", "5 years"])

                # Income and Financial Details
                annual_income = st.number_input("Annual Income (₹)", min_value=0.0)
                existing_loans = st.number_input("Existing Loan Amount (₹)", min_value=0.0)
                collateral_details = st.text_area("Collateral Details (if applicable)")

                # Display Contributors with Preferred Rates of Interest
                st.subheader("Select a Contributor")
                c.execute("SELECT u.username, u.interests, u.agreement, cr.preferred_rate FROM users u JOIN contributor_rates cr ON u.username = cr.contributor_username WHERE u.role = 'Contributor'")
                contributors = c.fetchall()

                if contributors:
                    contributor_options = {}
                    for contributor in contributors:
                        contributor_options[contributor[0]] = f"{contributor[0]} - {contributor[1]} - {contributor[2]} - Rate: {contributor[3]}%"

                    selected_contributor = st.selectbox("Choose a Contributor", list(contributor_options.keys()))

                    # Fetch the preferred rate of interest for the selected contributor
                    c.execute("SELECT preferred_rate FROM contributor_rates WHERE contributor_username = ?", (selected_contributor,))
                    preferred_rate = c.fetchone()[0]
                    st.write(f"Selected Contributor's Preferred Rate of Interest: {preferred_rate}%")
                else:
                    st.error("No contributors available.")

                # Loan Approval Process
                st.subheader("Loan Approval Process")
                st.write(
                    """
                    - Your loan application will be reviewed by the bank.
                    - A field officer may visit your farm to verify details.
                    - The bank will assess your creditworthiness based on income, collateral, and repayment capacity.
                    - You will be notified of the approval status via email or SMS.
                    """
                )

                # Loan Repayment Conditions
                st.subheader("Loan Repayment Conditions")
                st.write(
                    """
                    - Repayments must be made as per the agreed schedule.
                    - Late payments may attract penalties.
                    - Early repayment options are available but may include pre-closure charges.
                    """
                )

                # Submit Loan Application
                if st.button("Submit Loan Application"):
                    if purpose_of_loan and loan_amount > 0 and annual_income > 0:
                        try:
                            c.execute('''INSERT INTO loan_history (aadhaar, name, amount, status) 
                                         VALUES (?, ?, ?, ?)''',
                                      (st.session_state['username'], purpose_of_loan, loan_amount, "Pending"))
                            conn.commit()
                            st.success("✅ Your loan application has been submitted successfully!")
                        except sqlite3.Error as e:
                            st.error(f"Database error: {e}")
                    else:
                        st.error("❗ Please fill out all required fields correctly.")
        else:
            st.warning("This section is only accessible to farmers.")
    else:
        st.warning("Please log in as a farmer to access this section.")

######verificatio

elif menu == "Verification":
    st.title("🔍 Loan Verification")

    # Check if the user is logged in as an admin
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        role = st.session_state.get('role', None)
        if role == "Admin":
            st.subheader("Manage Loan Applications")

            # Fetch all pending loan applications
            c.execute("SELECT * FROM loan_history WHERE status = 'Pending'")
            pending_applications = c.fetchall()

            if pending_applications:
                for application in pending_applications:
                    st.write(f"Application ID: {application[0]}")
                    st.write(f"Aadhaar: {application[1]}")
                    st.write(f"Name: {application[2]}")
                    st.write(f"Amount: ₹{application[3]}")

                    # Approval/Rejection Options
                    approval_status = st.selectbox("Status", ["Approve", "Reject"], key=f"approval_{application[0]}")

                    if st.button("Update Status", key=f"update_{application[0]}"):
                        if approval_status == "Approve":
                            c.execute("UPDATE loan_history SET status = 'Approved' WHERE id = ?", (application[0],))
                            conn.commit()
                            st.success("Application approved successfully!")
                        elif approval_status == "Reject":
                            c.execute("UPDATE loan_history SET status = 'Rejected' WHERE id = ?", (application[0],))
                            conn.commit()
                            st.success("Application rejected successfully!")
            else:
                st.info("No pending applications found.")
        else:
            st.warning("This section is only accessible to admins.")
    else:
        st.warning("Please log in as an admin to access this section.")

# ------------------------------
# FEEDBACK SYSTEM
# ------------------------------
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
SMTP_SERVER = "smtp.gmail.com"  # For Gmail
SMTP_PORT = 587
SENDER_EMAIL = "rathodvidyar@gmail.com"  # Your email
SENDER_PASSWORD = "zabh trfm eqmp zolr"  # Your email password or app password
RECEIVER_EMAIL = "rathodvidyar@gmail.com"  # Email where feedback will be sent

def send_feedback(feedback):
    subject = "New Feedback from Tenant Farmer Loan App"
    message = f"User Feedback:\n\n{feedback}"

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending feedback: {e}")
        return False


# Add Feedback System to menu
if menu == "Feedback System":
    st.title("📝 Feedback System")
    feedback = st.text_area("Enter your feedback or suggestions:")
    
    if st.button("Submit Feedback"):
        if feedback.strip():
            if send_feedback(feedback):
                st.success("✅ Thank you for your feedback! It has been sent to the admin via email.")
            else:
                st.error("❌ Failed to send feedback. Please try again later.")
        else:
            st.error("⚠️ Please enter feedback before submitting.")
