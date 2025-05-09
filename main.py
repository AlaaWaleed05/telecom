import streamlit as st
import Visuals
import script
import Home
import About
import rec
import App_Cost
st.set_page_config(page_title="Telecom Churn App", layout="wide")

def sidebar():

    st.sidebar.title("🔀 Sections")
    page = st.sidebar.radio("Go to", ["🏠Home","ℹ️ About","📊 Visualizations", "📈 Churn Prediction","📋Recommendations" ,"💼App Cost"])
    return page


def main():
    page = sidebar()

    if page == "🏠Home":
        st.title(" Welcome to our Churn Prediction System")  # Calls the home_page function to display the content
        Home.run()
    elif page == "ℹ️ About":

        About.run()
    elif page == "📊 Visualizations":
        st.title("📊 Visualizations")
        Visuals.run()
    elif page == "📈 Churn Prediction":
        st.title("📊 Churn Prediction")
        script.run()  # This should contain the model inputs and prediction UI

    # This should contain your boxplot and any other plots


    elif page == "📋Recommendations":

        rec.run()
    elif page == "💼App Cost":

        App_Cost.run()

if __name__ == "__main__":
    main()