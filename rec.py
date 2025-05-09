import streamlit as st

# Set page configuration

def run():
    # Apply custom CSS styling
    st.markdown("""
        <style>
        .stApp {
            background-color: #00264d;  /* Dark Blue Background */
            color: white;  /* Default text color */
        }

        h1, h2, h3, h4, h5, h6, p, li {
            color: white !important;
        }

        p, li {
            font-size: 20px !important;  /* Increase normal text size */
        }

        .markdown-text-container {
            font-size: 20px !important;
        }

        /* Sidebar style */
        section[data-testid="stSidebar"] {
            background-color: #001f3f;
        }
        section[data-testid="stSidebar"] * {
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # Now write your recommendations
    st.title("📈 Business Recommendations")

    st.markdown("""
    This system represents a **balanced combination** of reasonable cost, high accuracy, and significant business value, making it an ideal strategic investment for telecom companies like **Jio, Airtel, Vi, and BSNL**.

    ## Recommendations for Business:

    1. **Offer More Data & Flexible Plans**  
       📶 Data consumption continues to grow across all age groups.  
       📊 Introduce plans with **higher data limits** or **rollover features**.  
       🎯 Consider **data booster packs** and **pay-as-you-go models** for flexibility, especially for younger users.

    2. **Ensure Wide and Reliable Network Coverage**  
       🌐 Poor network coverage is a major reason for churn.  
       🏗️ Invest in infrastructure, especially in high-churn or weak-signal regions.  
       🔍 Conduct **regular network health assessments**.

    3. **Maintain Reasonable and Transparent Pricing**  
       💸 Customers are very **price-sensitive**.  
       📦 Launch **clear value plans** without hidden charges.  
       👨‍👩‍👧‍👦 Offer **family or group bundles** to boost retention.

    4. **Improve Customer Service Experience**  
       🙋 Poor service drives dissatisfaction and churn.  
       🚀 Focus on **fast, efficient, and empathetic support**.

    5. **Proposed Churn Reduction Campaign: "Stay Connected, Stay Empowered"**  
       👩‍💼 Targeted at **female customers** with special benefits.  
       💖 Build **strong emotional connections** with the brand.

    ---
    """)

