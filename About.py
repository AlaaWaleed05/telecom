import streamlit as st

def run():
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
            color: white !important;
        }

        .markdown-text-container {
            font-size: 20px !important;
        }

            /* Optional: make sidebar blend with dark theme */
        section[data-testid="stSidebar"] {
                background-color: #001f3f;
        }
        section[data-testid="stSidebar"] * {
                color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)


    st.markdown(
    """
    ### 📱 Telecom Churn Prediction App

    This web application is built to help telecom companies identify customers who are at risk of **churning** specifically at India.
    By predicting customer churn, businesses can take proactive steps to retain users, improve services, and boost satisfaction.

    #### 🎯 Key Features:
    - **Churn Prediction**: Enter customer information to predict the likelihood of churn using a machine learning model.
    - **Interactive Visualizations**: Understand trends, patterns, and important features through charts and graphs.
    - **Data Insights**: Dive into your customer data to explore what drives churn behavior.

    #### 🛠️ Technologies Used:
    - **Python**
    - **Streamlit**
    - **Machine Learning (scikit-learn)**
    - **Pandas / NumPy / Matplotlib / Seaborn**

    

    ---
    """)
