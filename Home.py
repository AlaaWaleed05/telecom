import streamlit as st


def run():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://user-images.githubusercontent.com/114465492/262604940-a44b8f9a-886d-458d-943a-83ced746a6c7.png');  /* Replace with your image URL */
            background-size: cover;
            background-position: center;
            height: 100%;
            width: 100%;
        }
        h1, h2, h3, h4, h5, h6 {
            color: white !important;
        }

        .stHeader {
            color: white !important;
        }

        /* Set other text color to white */
        .stMarkdown, .stText, .stWrite, .css-1cpxqw2 {
            color: white !important;
        }

        /* Sidebar background to dark blue */
        section[data-testid="stSidebar"] {
                background-color: #001f3f;
            }
            section[data-testid="stSidebar"] * {
                color: white !important;
            }
        </style>
        """, unsafe_allow_html=True)

    st.title("📱 Telecom Churn Prediction App")





    # Optional image, logo, or other content
    # st.image("path_to_logo.png", width=200)


