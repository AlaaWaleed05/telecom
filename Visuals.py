import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.colors as pc
import plotly.express as px

def run():  # 🔹 Add this line to wrap everything below
    dark_blue = "#1e2a47"  # Dark blue color code for column names
    white= "#ffffff"  # White color code for descriptions

    # Add custom CSS to set the background color, text color, and specific column styling
    hover_blue = "#2c3b61"

    st.markdown(f"""
        <style>
            /* Main background */
            .stApp {{
                background-color: {dark_blue} !important;
                color: {white} !important;
            }}

            /* Sidebar */
            section[data-testid="stSidebar"] {{
                background-color: {dark_blue} !important;
            }}

            /* Text */
            .stMarkdown, .stText, p, span, div, label {{
                color: {white} !important;
            }}

            /* Input and dropdown base */
            div[data-baseweb="select"] {{
                background-color: {dark_blue} !important;
                color: {white} !important;
                border-color: {white} !important;
            }}

            /* Input text */
            div[data-baseweb="select"] input {{
                color: {white} !important;
            }}

            /* Dropdown list when opened */
            div[role="listbox"] {{
                background-color: {dark_blue} !important;
                color: {white} !important;
            }}

            /* Individual dropdown options */
            div[role="option"] {{
                background-color: {dark_blue} !important;
                color: {white} !important;
            }}

            /* Hover on dropdown options */
            div[role="option"]:hover {{
                background-color: {hover_blue} !important;
            }}

            /* Selected item in dropdown */
            div[aria-selected="true"] {{
                background-color: {hover_blue} !important;
                color: {white} !important;
            }}

            /* Buttons */
            .stButton>button {{
                background-color: {dark_blue} !important;
                color: {white} !important;
                border: 1px solid {white} !important;
            }}

            .stButton>button:hover {{
                background-color: {hover_blue} !important;
            }}

            /* Fix borders and outlines */
            div[data-baseweb="select"]:hover,
            div[data-baseweb="select"]:focus-within {{
                border-color: {white} !important;
            }}

            /* Header text (h1, h2, etc.) */
            h1, h2, h3, h4 {{
                color: {white} !important;
            }}
        </style>
    """, unsafe_allow_html=True)

    st.title("📈 Visualizations")


    # Load data
    df_telecom_churn = pd.read_csv("preprocessed_telecom_churn_data.csv")
    st.sidebar.header("🔍 Filters")

    selected_partners = st.sidebar.multiselect(
        "Select Telecom Partners:",
        options=df_telecom_churn['telecom_partner'].unique(),
        default=df_telecom_churn['telecom_partner'].unique()
    )

    selected_states = st.sidebar.multiselect(
        "Select States:",
        options=df_telecom_churn['state'].unique(),
        default=df_telecom_churn['state'].unique()
    )

    # Filter the DataFrame based on selections
    filtered_df = df_telecom_churn[
        (df_telecom_churn['telecom_partner'].isin(selected_partners)) &
        (df_telecom_churn['state'].isin(selected_states))
        ]
    total_customers = df_telecom_churn.shape[0]
    churned = df_telecom_churn['churn'].sum()
    avg_data_used = df_telecom_churn['data_used'].mean()
    avg_calls = df_telecom_churn['calls_made'].mean()

    # Create cards with columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("👥 Total Customers", len(filtered_df))

    with col2:
        churn_rate = filtered_df['churn'].mean()
        st.metric("📉 Churn Rate", f"{churn_rate:.2%}")

    with col3:
        avg_calls = filtered_df['calls_made'].mean()
        st.metric("📞 Avg. Calls Made", f"{avg_calls:.1f}")
    df=filtered_df
    # ========== 📊 Charts Section ==========

    # ========== Churn Rate Pie Chart ==========
    section = st.sidebar.radio(
        "Select a Section to Explore its Analysis",
        ["Data_Overview","Telecom partners Offers", "Churn Analysis", "Age Group Analysis"]
    )

    if section == "Telecom partners Offers":
        st.header(" Telecom Partners offers Analysis")
        st.subheader("1-Telecom Partners offers")
        offer_cols = ['sms_sent', 'calls_made', 'data_used']
        negative_data = df[df[offer_cols].lt(0).any(axis=1)]  # Rows with negative values in any of the offer columns

        # Melt data to create a 'long' format DataFrame
        negative_melted = negative_data[['telecom_partner'] + offer_cols].melt(
            id_vars='telecom_partner',
            var_name='Offer_Type',
            value_name='Value'
        )
        pie_data = negative_melted.groupby(['telecom_partner', 'Offer_Type']).size().reset_index(name='Count')
        # Filter for negative values only
        negative_melted = negative_melted[negative_melted['Value'] < 0]
        selected_data = pie_data[pie_data['telecom_partner'].isin(selected_partners)]

        # Group by telecom_partner and Offer_Type to get counts
        pie_data = negative_melted.groupby(['telecom_partner', 'Offer_Type']).size().reset_index(name='Count')
        fig = px.pie(
            selected_data,
            names='Offer_Type',
            values='Count',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig.update_traces(textinfo='percent+label')
        fig.update_layout(template='plotly_dark')

        st.plotly_chart(fig)

        negative_sms = df[df["sms_sent"] < 0]
        negative_sms_counts = negative_sms.groupby(["state", "telecom_partner"]).size().reset_index(name="count")

        st.subheader("2-SMS Offers per State and Telecom Partner")
        if not negative_sms_counts.empty:
            fig4 = px.bar(
                negative_sms_counts,
                x="state",
                y="count",
                color="telecom_partner",

                text="count",
                labels={"state": "State", "count": "Number of Negative Records", "telecom_partner": "Telecom Partner"},
                barmode="group",
                color_discrete_sequence=px.colors.sequential.Viridis  # Changed to Viridis color scheme
            )
            fig4.update_layout(template="plotly_dark", xaxis_tickangle=-45)
            st.plotly_chart(fig4)
        else:
            st.warning("⚠️ No negative values found in sms_sent.")

        # Negative Data Used Records
        negative_data = df[df["data_used"] < 0]
        negative_data_counts = negative_data.groupby(["state", "telecom_partner"]).size().reset_index(name="count")
        st.subheader("3-Data offers per State and Telecom Partner")
        if not negative_data_counts.empty:
            fig6 = px.bar(
                negative_data_counts,
                x="state",
                y="count",
                color="telecom_partner",

                text="count",
                labels={"state": "State", "count": "Number of Negative Records", "telecom_partner": "Telecom Partner"},
                barmode="group",
                color_discrete_sequence=px.colors.sequential.Viridis  # Changed to Viridis color scheme
            )
            fig6.update_layout(template="plotly_dark", xaxis_tickangle=-45)
            st.plotly_chart(fig6)
        else:
            st.warning("⚠️ No negative values found in data_used.")

        # Negative Calls Records
        negative_calls = df[df["calls_made"] < 0]
        negative_calls_counts = negative_calls.groupby(["state", "telecom_partner"]).size().reset_index(name="count")
        st.subheader("4-Calls made per State and Telecom Partner")
        if not negative_calls_counts.empty:
            fig7 = px.bar(
                negative_calls_counts,
                x="state",
                y="count",
                color="telecom_partner",

                text="count",
                labels={"state": "State", "count": "Number of Negative Records", "telecom_partner": "Telecom Partner"},
                barmode="group",
                color_discrete_sequence=px.colors.sequential.Viridis  # Changed to Viridis color scheme
            )
            fig7.update_layout(template="plotly_dark", xaxis_tickangle=-45)
            st.plotly_chart(fig7)
        else:
            st.warning("⚠️ No negative values found in calls_made.")

        st.subheader("5-Offers at each month")

        df['date_of_registration'] = pd.to_datetime(df['date_of_registration'], errors='coerce')

        # Extract month name from the date
        df['registration_month'] = df['date_of_registration'].dt.strftime('%B')



        # Define offer columns where negative values are considered "offers"
        offer_cols = ['sms_sent', 'calls_made', 'data_used']

        # Filter rows where any of those columns have negative values
        offer_rows = df[(df[offer_cols] < 0).any(axis=1)]  # Correct filtering condition

        # Melt data to create a 'long' format DataFrame for negative offers
        negative_melted = offer_rows[['telecom_partner'] + offer_cols].melt(
            id_vars='telecom_partner',
            var_name='Offer_Type',
            value_name='Value'
        )

        # Filter for negative values only
        negative_melted = negative_melted[negative_melted['Value'] < 0]

        # Ensure that we correctly match the 'registration_month' from the original 'offer_rows' to the melted data
        # We need to repeat the 'registration_month' column for each melted row
        negative_melted['registration_month'] = pd.concat([offer_rows['registration_month']] * len(offer_cols),
                                                          ignore_index=True)

        # Check the first few rows of the melted data for correctness


        # Group by 'registration_month' and count occurrences of negative offers
        monthly_offer_counts = negative_melted.groupby(['registration_month']).size().reset_index(
            name='Negative Offers')

        # Ensure that the months are ordered correctly
        monthly_offer_counts['registration_month'] = pd.Categorical(
            monthly_offer_counts['registration_month'],
            categories=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                        'October', 'November', 'December'],
            ordered=True
        )

        # Sort the months by the correct order
        monthly_offer_counts = monthly_offer_counts.sort_values('registration_month')



        # Plot number of negative offers per month
        fig = px.bar(
            monthly_offer_counts,
            x='registration_month',
            y='Negative Offers',
            color='registration_month',
            color_discrete_sequence=px.colors.sequential.Viridis,

        )

        fig.update_layout(template='plotly_dark', xaxis_tickangle=-45)
        st.plotly_chart(fig)

        registrations_per_year = df_telecom_churn.groupby(["registration_year", "telecom_partner"]).size().reset_index(
            name="Number of Customers")
        st.subheader("6-Customer Registrations Trend Over Years by Telecom Partner",)
        # Create the line plot for registrations over years by telecom partner
        fig = px.line(
            registrations_per_year,
            x="registration_year",
            y="Number of Customers",
            color="telecom_partner",
            markers=True,

            labels={
                "registration_year": "Year",
                "Number of Customers": "Customers",
                "telecom_partner": "Telecom Partner"
            },
            color_discrete_sequence=px.colors.sequential.Viridis  # Using Viridis color scheme
        )

        fig.update_layout(template="plotly_dark", title_x=0.5)
        st.plotly_chart(fig)

        # Step 1: Calculate totals per year
        totals = registrations_per_year.groupby("registration_year")["Number of Customers"].sum().reset_index()
        totals["telecom_partner"] = "Total"

        # Step 2: Append to original data
        registrations_with_total = pd.concat([registrations_per_year, totals], ignore_index=True)
        st.subheader("7-Customer Registrations Per Year by Telecom Partner (with Total)")
        # Step 3: Create the bar plot for customer registrations per year (including totals)
        fig10 = px.bar(
            registrations_with_total,
            x="telecom_partner",
            y="Number of Customers",
            color="telecom_partner",

            facet_col="registration_year",
            facet_col_wrap=2,
            labels={
                "registration_year": "Registration Year",
                "Number of Customers": "Count",
                "telecom_partner": "Telecom Partner"
            },
            text="Number of Customers",
            color_discrete_sequence=px.colors.sequential.Viridis  # Using Viridis color scheme
        )

        fig10.update_layout(
            template="plotly_dark",


        )



        # Update annotations to display the correct year in facet titles
        fig10.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

        st.plotly_chart(fig10)
        bins = [18, 32, 46, 60, 74]
        labels = ["18-32", "33-46", "47-60", "61-74"]

        # Create an age group column
        df_telecom_churn["age_group"] = pd.cut(df_telecom_churn["age"], bins=bins, labels=labels, right=False)

        # Melt the relevant columns to long format for negative offers
        offer_cols = ['sms_sent', 'calls_made', 'data_used']
        melted = df_telecom_churn[['age_group'] + offer_cols].melt(
            id_vars='age_group',
            value_vars=offer_cols,
            var_name='Offer_Type',
            value_name='Value'
        )

        # Filter negative values (which are considered offers)
        negative_offers = melted[melted['Value'] < 0]

        # Count the negative offers by age group and offer type
        offer_counts = negative_offers.groupby(['age_group', 'Offer_Type']).size().reset_index(name='Count')
        st.subheader('8-Offers by Age Group ')
        # Plot the distribution of offers by age group and offer type
        fig_age_group = px.bar(
            offer_counts,
            x='age_group',
            y='Count',
            color='Offer_Type',
            barmode='group',

            labels={'age_group': 'Age Group', 'Count': 'Number of Offers'},
            template='plotly_dark',
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig_age_group)






    elif section == "Churn Analysis":
        st.header("Churn Analysis ")
        st.subheader("1-Churn Rate by Telecom Partner")
        telecom_partner_counts = df_telecom_churn["telecom_partner"].value_counts()
        churned_customers = df_telecom_churn[df_telecom_churn["churn"] == 1]["telecom_partner"].value_counts()
        churn_rate = (churned_customers / telecom_partner_counts) * 100

        churn_rate_df = churn_rate.reset_index()
        churn_rate_df.columns = ["telecom_partner", "churn_rate"]

        fig1 = px.pie(
            churn_rate_df,
            names="telecom_partner",
            values="churn_rate",

            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig1.update_traces(textinfo="percent+label")
        fig1.update_layout(template="plotly_dark")
        st.plotly_chart(fig1)

        st.subheader("2. Churn Rate by Gender")
        gender_churn_df = df_telecom_churn.groupby("gender")["churn"].mean().reset_index()
        gender_churn_df["churn"] *= 100

        fig2 = px.bar(
            gender_churn_df,
            x="gender",
            y="churn",

            labels={"gender": "Gender", "churn": "Churn Rate (%)"},
            text=gender_churn_df["churn"].round(2),
            color="churn",
            color_continuous_scale=px.colors.sequential.Viridis
        )
        fig2.update_layout(template="plotly_dark")
        st.plotly_chart(fig2)

        st.subheader("3. Churn Rate by Dependents")
        dependent_churn_df = df_telecom_churn.groupby("num_dependents")["churn"].mean().reset_index()
        dependent_churn_df["churn"] *= 100

        fig3 = px.bar(
            dependent_churn_df,
            x="num_dependents",
            y="churn",

            labels={"churn": "Churn Rate (%)"},
            text=dependent_churn_df["churn"].round(2),
            color="churn",
            color_continuous_scale="Viridis"
        )
        fig3.update_layout(template="plotly_dark")
        st.plotly_chart(fig3)

        st.subheader("4.Churn Rate by Engagement Type ")
        grouped = df_telecom_churn.groupby(["telecom_partner", "engagement_type"])["churn"].agg(
            ["sum", "count"]).reset_index()
        grouped["churn_rate"] = (grouped["sum"] / grouped["count"]) * 100
        grouped["churn_rate_text"] = grouped["churn_rate"].apply(lambda x: f"{x:.2f}%")

        fig4 = px.bar(
            grouped,
            x="engagement_type",
            y="churn_rate",
            color="churn_rate",
            color_continuous_scale=px.colors.sequential.Viridis,
            facet_col="telecom_partner",
            facet_col_wrap=2,
            text="churn_rate_text",

        )
        fig4.update_layout(template="plotly_dark")
        fig4.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        st.plotly_chart(fig4)

        st.subheader("6-Churn Rate by Plan Type ")
        grouped = df_telecom_churn.groupby(["telecom_partner", "plan_type"])["churn"].agg(
            ["sum", "count"]).reset_index()
        grouped["churn_rate"] = (grouped["sum"] / grouped["count"]) * 100
        grouped["churn_rate_text"] = grouped["churn_rate"].apply(lambda x: f"{x:.2f}%")

        fig5 = px.bar(
            grouped,
            x="plan_type",
            y="churn_rate",
            color="churn_rate",
            color_continuous_scale=px.colors.sequential.Viridis,
            facet_col="telecom_partner",
            facet_col_wrap=2,
            text="churn_rate_text",

        )
        fig5.update_layout(template="plotly_dark")
        fig5.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        st.plotly_chart(fig5)

        st.subheader("6. Churn Rate by Calls Made")
        call_churn_df = df_telecom_churn.groupby("calls_made")["churn"].mean().reset_index()
        call_churn_df["churn"] *= 100

        fig6 = px.line(
            call_churn_df,
            x="calls_made",
            y="churn",

            labels={"churn": "Churn Rate (%)"},
            markers=True,
            line_shape="spline",
            color_discrete_sequence=["#440154"]
        )
        fig6.update_layout(template="plotly_dark")
        st.plotly_chart(fig6)

        st.subheader("7. Churn Rate by SMS Sent")
        sms_churn_df = df_telecom_churn.groupby("sms_sent")["churn"].mean().reset_index()
        sms_churn_df["churn"] *= 100

        fig7 = px.line(
            sms_churn_df,
            x="sms_sent",
            y="churn",

            labels={"churn": "Churn Rate (%)"},
            markers=True,
            line_shape="spline",
            color_discrete_sequence=["#440154"]
        )
        fig7.update_layout(template="plotly_dark")
        st.plotly_chart(fig7)

        st.subheader("8-Churn Rate by Data Usage Category")
        # Step 1: Define custom bins and labels
        bins = [-float('inf'), 0, 2490, 4978, 7493.25, 10991, float('inf')]
        labels = ['Offers Usage', 'Low Usage', 'Below Average', 'Above Average', 'High Usage', 'Extreme Usage']

        # Step 2: Create the bin column
        df['data_usage_category'] = pd.cut(df['data_used'], bins=bins, labels=labels)

        # Step 3: Group by the new bins and calculate churn rate
        data_churn_df = df.groupby("data_usage_category")["churn"].mean().reset_index()
        data_churn_df["churn"] *= 100  # Convert to percentage

        # Step 4: Plot
        fig8 = px.line(
            data_churn_df,
            x="data_usage_category",
            y="churn",
            labels={"data_usage_category": "Data Usage Category", "churn": "Churn Rate (%)"},
            markers=True,
            line_shape="spline",
            color_discrete_sequence=["#440154"]
        )

        fig8.update_layout(template="plotly_dark")

        # Step 5: Streamlit render
        st.plotly_chart(fig8, use_container_width=True)

        st.subheader("9. Churn Rate by Age Group")
        bins = [18, 32, 46, 60, 74]
        labels = ["18-32", "33-46", "47-60", "61-74"]
        df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, include_lowest=True)
        age_churn_rate = df.groupby("age_group")["churn"].mean() * 100
        age_churn_df = age_churn_rate.reset_index()

        fig = px.bar(
            age_churn_df,
            x="age_group",
            y="churn",

            labels={"age_group": "Age Group", "churn": "Churn Rate (%)"},
            text=age_churn_df["churn"].round(2),
            color="churn",
            color_continuous_scale="Viridis"
        )
        fig.update_layout(
            xaxis_title="Age Group",
            yaxis_title="Churn Rate (%)",
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig)

    elif section == "Age Group Analysis":
        st.subheader("1-Engagement Type By Age Group")
        bins = [18, 32, 46, 60, 74]
        labels = ["18-32", "33-46", "47-60", "61-74"]

        # Create an age group column
        df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)

        # Aggregate
        df_engagement = df.groupby(['engagement_type', 'age_group']).size().reset_index(name='count')

        # Plot
        fig1 = px.bar(df_engagement,
                      x='engagement_type',
                      y='count',
                      color='age_group',

                      barmode='stack',
                      labels={'engagement_type': 'Engagement Type', 'age_group': 'Age Group'},
                      color_discrete_sequence=px.colors.sequential.Viridis,
                      category_orders={'engagement_type': df_telecom_churn['engagement_type'].unique()})

        fig1.update_layout(template='plotly_dark', title={'x': 0.5})

        # Display in Streamlit
        st.plotly_chart(fig1, use_container_width=True)

        # Second Chart: Age Group Distribution by Plan Type
        st.subheader("2-Plan Type By Age Group")

        # Aggregate
        df_plan = df.groupby(['plan_type', 'age_group']).size().reset_index(name='count')

        # Plot
        fig2 = px.bar(df_plan,
                      x='plan_type',
                      y='count',
                      color='age_group',

                      barmode='stack',
                      labels={'plan_type': 'Plan Type', 'age_group': 'Age Group'},
                      color_discrete_sequence=px.colors.sequential.Viridis,
                      category_orders={'plan_type': df_telecom_churn['plan_type'].unique()})

        fig2.update_layout(template='plotly_dark', title={'x': 0.5})

        # Display in Streamlit
        st.plotly_chart(fig2, use_container_width=True)

        st.title("3-Average Estimated Salary by Age Group")

        # Make sure df_telecom_churn is loaded and contains 'age_group' and 'estimated_salary'

        # Aggregate: Calculate average salary by age group
        avg_salary_df = df.groupby('age_group')['estimated_salary'].mean().reset_index()

        # Plot
        fig = px.bar(avg_salary_df,
                     x='age_group',
                     y='estimated_salary',
                     color='age_group',

                     labels={'age_group': 'Age Group', 'estimated_salary': 'Average Salary'},
                     color_discrete_sequence=px.colors.sequential.Viridis)

        fig.update_layout(template='plotly_dark', title={'x': 0.5})

        # Display in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    elif section=="Data_Overview":
        st.markdown("## 📊 Data Overview")

        st.write("""
        This dataset contains information about customers from the **top 4 telecom partners in India** who are actively competing to offer the best telecom services.  
        It includes **243,553 rows** and **14 columns** add it to it 2 columns through feature engineering so it beame total of 16 columns, each representing key details about customers and their usage patterns.
        """)

        st.markdown("### 🧾 Dataset Description")

        st.write("### Column Descriptions:")
        st.write("1.**Customer_id**: Unique identifier for each customer.")  # Example description
        st.write("2.**Telecom_partner**: The telecom partner associated with the customer.")
        st.write("3.**Gender**: The gender of the customer.")
        st.write("4.**Age**: The age of the customer.")
        st.write("5.**State**: The Indian state in which the customer is located.")
        st.write("6.**City**: The city in which the customer is located.")
        st.write("7.**Pincode**: The pincode of the customer's location.")
        st.write("8.**Date_Of_Registration**: The date on which the customer registered with the telecom partner.")
        st.write("9.**Num_Dependents**: The number of dependents (e.g. children) the customer has.")
        st.write("10.**Estimated_Salary**: The customer's estimated salary.")
        st.write("11.**Calls_made**: The number of calls made by the customer.")
        st.write("12.**SMS_sent**: The number of SMS messages sent by the customer.")
        st.write("13.**Data_used**: The amount of data used by the customer.")
        st.write("14.**Churn**: Binary variable indicating whether the customer has churned or not (1 = churned, 0 = not churned).")
        st.write("15.**Engagement_Type**: Describes the customer's interaction level or usage engagement pattern (data_heavy, call_heavy, sms_heavy,inactive, balanced). ")
        st.write("16.**Plan_Type**: Type of telecom plan the customer is subscribed to (High_data,Moderate Data,Family Plan,Calls Plan,Basic CS). ")
        st.subheader("Sample for the dataset")

        st.write(df.head())
        numerical_cols = df.select_dtypes(include=["number"]).columns
        viridis_colors = pc.sample_colorscale('Viridis',
                                              [i / (len(numerical_cols) - 1) for i in range(len(numerical_cols))])

        fig1 = go.Figure()

        # Add traces for each numerical column
        for col, color in zip(numerical_cols, viridis_colors):
            fig1.add_trace(go.Box(y=df[col], name=col, marker_color=color))
        st.subheader("1-Numerical Columns Distributions")
        fig1.update_layout(

            xaxis_title="Columns",
            yaxis_title="Values",
            template="plotly_dark"
        )

        # Show boxplot
        st.plotly_chart(fig1)

        st.subheader(f"2-Distribution of Categorical Columns")
        # **Bar Charts for Categorical Columns**
        categorical_cols = df.select_dtypes(include=["object", "category"]).columns
        categorical_cols = categorical_cols.drop(["date_of_registration", "pincode"], errors="ignore")

        for col in categorical_cols:
            counts = df[col].value_counts().reset_index()
            counts.columns = [col, "count"]

            fig2 = px.bar(
                counts,
                x=col,
                y="count",

                labels={col: "Category", "count": "Count"},
                color="count",
                color_continuous_scale="viridis"
            )

            fig2.update_layout(template="plotly_dark")
            st.plotly_chart(fig2)

        # **Bar Chart of Telecom Partner Ranking by State**
        state_partner_counts = df.groupby(["state", "telecom_partner"]).size().reset_index(name="count")

        # Rank telecom partners within each state
        state_partner_counts["rank"] = state_partner_counts.groupby("state")["count"].rank(method="dense",
                                                                                           ascending=False)

        # Sort by state and rank
        state_partner_counts = state_partner_counts.sort_values(by=["state", "rank"])

        # Set colors for telecom partners
        viridis_colors = px.colors.sequential.Viridis[:len(state_partner_counts["telecom_partner"].unique())]
        st.subheader("3-Telecom Partner Ranking in Each State")
        fig3 = px.bar(
            state_partner_counts,
            x="state",
            y="count",
            color="telecom_partner",
            text="rank",

            labels={"count": "Number of Users", "telecom_partner": "Telecom Partner"},
            barmode="group",
            color_discrete_sequence=viridis_colors
        )

        fig3.update_layout(template="plotly_dark", xaxis_tickangle=-45)

        # Show ranking chart
        st.plotly_chart(fig3)




