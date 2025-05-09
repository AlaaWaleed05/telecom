import streamlit as st

# Set page configuration
def run():
    st.markdown("""
        <style>
        .stApp {
            background-color: #00264d;  /* Dark Blue Background */
            color: white;
        }

        h1, h2, h3, h4, h5, h6, p, li {
            color: white !important;
        }

        p, li {
            font-size: 20px !important;
        }

        .markdown-text-container {
            font-size: 20px !important;
        }

        section[data-testid="stSidebar"] {
            background-color: #001f3f;
        }
        section[data-testid="stSidebar"] * {
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # Title and intro
    st.title("💰 Cost-Effective Solution & Strategic Value")

    st.markdown("""
    The proposed churn prediction system offers a **highly cost-effective** solution for telecom partners like **Jio, Airtel, Vi, and BSNL**.  
    Using efficient machine learning models such as **XGBoost**, **Decision Trees**, and **Ensemble Methods**, the system reached **up to 85% accuracy**, making it both **impactful and scalable**.

    ---

    ## 📊 Business Benefits of This System

    1. 💸 **Churn Reduction = Cost Savings**  
       - Acquiring a new customer is **5x more expensive** than retaining one.

    2. 🔁 **Customer Lifetime Value Increases**  
       - Retained customers generate **more revenue over time**.

    3. 🎯 **Targeted Marketing**  
       - Smart segmentation helps **focus efforts and budget** only on likely churners.

    4. 🧭 **Better Strategic Planning**  
       - Forecast **risk areas** and adapt offers, plans, and services accordingly.

    5. 🤝 **Improved Brand Loyalty**  
       - Personalized outreach (like the **female-focused campaign**) builds **emotional bonds**.

    6. 📉 **Reduces Revenue Loss from Churn**  
       - Every lost customer = **missed revenue** from data, calls, upgrades.

    7. 🎁 **Enhances Customer Experience**  
       - Offers like **discounts and loyalty gifts** increase satisfaction and retention.

    8. ⭐ **Strengthens Brand Reputation**  
       - Happy customers leave **positive reviews**, refer friends, and **stay longer**.

    ---

    ## 💼 Why It's a Cost-Effective Investment

    1. 🧮 **Reasonable Investment**  
       - Development & deployment costs are **moderate** compared to churn losses.  
       - Scalable models mean **minimal added cost** for future updates.

    2. 📈 **Strong Performance**  
       - Up to **85% accuracy** = 8–9 out of 10 churners correctly identified.  
       - Enables **early intervention** and **customer retention**.

    3. 📊 **High ROI (Return on Investment)**  
       - Faster response = **lower churn** and **higher profits**.  
       - Scalable architecture means the system **adapts and improves** as customer behavior changes.  

    ---


    This is **not just a predictive system** — it's a **strategic tool** that transforms insights into **retention**, **loyalty**, and **long-term growth**.
    """)

# Apply custom CSS styling
