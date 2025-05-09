import streamlit as st
import numpy as np
import pandas as pd
import joblib
import hashlib







def run():
    # Load the saved model, scaler, and power transformer
    modelxg = joblib.load('model_XG.pk1')
    
    scaler = joblib.load('scaler.pkl')
    pt = joblib.load('power_transformer.joblib')
    st.markdown(
        """
        <style>
        body {
            background-image: url('https://user-images.githubusercontent.com/114465492/262604940-a44b8f9a-886d-458d-943a-83ced746a6c7.png'); /* Replace with your image URL */
            background-size: cover;
            background-position: center;
            color: white;  /* White text for contrast */
        }
        .stApp {
            background-color: rgba(0, 0, 0, 0.5);  /* Semi-transparent overlay to improve readability */
            background-image: url('https://user-images.githubusercontent.com/114465492/262604940-a44b8f9a-886d-458d-943a-83ced746a6c7.png'); /* Same image */
            background-size: cover;
            background-position: center;
        }
        h1, h2, h3, h4, h5, h6, p {
            color: white !important;  /* Ensure all text is white and important */
        }
        .stTitle {
            color: white !important;  /* Make the main header white and important */
        }
        .stSubheader {
            color: white !important;  /* Make the subheaders white and important */
        }
        .stTextInput, .stSelectbox, .stNumberInput, .stButton, .stDateInput {
            color: white;
            background-color: rgba(0, 0, 0, 0.6);  /* Slightly transparent background for inputs */
            border: 1px solid white;
        }
        section[data-testid="stSidebar"] {
                background-color: #001f3f;
        }
        section[data-testid="stSidebar"] * {
                color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title('Telecom Churn Prediction')

    # User inputs
    customer_id = st.number_input("Customer ID")
    gender = st.selectbox("Gender", ['Male', 'Female'])
    age = st.number_input("Age", min_value=10, max_value=100, value=30,format="%d")
    state = st.text_input("State")
    city = st.text_input("City")
    pincode = st.text_input("Pincode")
    date_of_registration = st.date_input("Date of Registration")
    num_dependents = st.number_input("Number of Dependents",format="%d")
    estimated_salary = st.number_input("Estimated Salary")
    calls_made = st.number_input("Calls Made",format="%d")
    sms_sent = st.number_input("SMS Sent",format="%d")
    data_used = st.number_input("Data Used (GB)",format="%d")
    telecom_partner = st.selectbox("Telecom Partner", ['Reliance jio', 'BSNL', 'Airtel', 'Vodafone'])


    # Collect input data into a dictionary
    input_data = {
        'customer_id': customer_id,
        'telecom_partner': telecom_partner,
        'gender': gender,
        'age': age,
        'state': state,
        'city': city,
        'pincode': pincode,
        'date_of_registration': date_of_registration,
        'num_dependents': num_dependents,
        'estimated_salary': estimated_salary,
        'calls_made': calls_made,
        'sms_sent': sms_sent,
        'data_used': data_used,
    }

    input_df = pd.DataFrame([input_data])

    input_df['calls_made'] = int(input_df['calls_made'])
    input_df['sms_sent'] = int(input_df['sms_sent'])
    input_df['data_used'] = float(input_df['data_used'])

    input_df['estimated_salary'] = float(input_df['estimated_salary'])
    input_df['age'] = int(input_df['age'])
    input_df['num_dependents'] = int(input_df['num_dependents'])
    def classify_engagement(row):
        calls = row['calls_made']
        sms = row['sms_sent']
        data = row['data_used']

        # Engagement classification logic
        if calls == 0 and sms == 0:
            return 'data_heavy'

        calls_val = max(calls, 0)
        sms_val = max(sms, 0)
        data_val = max(data, 0)
        total = calls_val + sms_val + data_val

        if total == 0 or (calls < 0 and sms < 0 and data < 0):
            return 'inactive'

        call_ratio = calls_val / total
        sms_ratio = sms_val / total
        data_ratio = data_val / total

        if data_ratio >= 0.6:
            return 'data_heavy'
        elif call_ratio >= 0.6:
            return 'call_heavy'
        elif sms_ratio >= 0.6:
            return 'sms_heavy'
        else:
            return 'balanced'

    def assign_plan_type(row):
        num_dependents = row['num_dependents']
        age = row['age']

        if num_dependents > 0:
            return 'Family Plan'
        elif 18 <= age <= 32:
            return 'High Data'
        elif 33 <= age <= 46:
            return 'Moderate Data'
        elif 47 <= age <= 60:
            return 'Calls Plan'
        elif 61 <= age <= 74:
            return 'Basic CS'
        else:
            return 'Standard'

    input_df['engagement_type'] = input_df.apply(classify_engagement, axis=1)
    input_df['plan_type'] = input_df.apply(assign_plan_type, axis=1)

    input_df['date_of_registration'] = pd.to_datetime(input_df['date_of_registration'])
    input_df['registration_year'] = input_df['date_of_registration'].dt.year
    input_df['registration_month'] = input_df['date_of_registration'].dt.month

    # Fix state using city-to-state mapping
    city_state_mapping_df = pd.read_csv("india_cities_states.csv")
    city_state_mapping = dict(zip(city_state_mapping_df["City"], city_state_mapping_df["State"]))
    input_df['state'] = input_df['city'].map(city_state_mapping).fillna(input_df['state'])

    # Process pincode
    state_pincode_mapping = {
        "11": ["Delhi"],
    "12": ["Haryana"], "13": ["Haryana"],
    "14": ["Punjab"], "15": ["Punjab"], "16": ["Punjab"],
    "17": ["Himachal Pradesh"],
    "18": ["Jammu", "Kashmir"], "19": ["Jammu", "Kashmir"],
    "20": ["Uttar Pradesh"], "21": ["Uttar Pradesh"], "22": ["Uttar Pradesh"],
    "23": ["Uttar Pradesh"], "24": ["Uttar Pradesh", "Uttarakhand"], "25": ["Uttar Pradesh", "Uttarakhand"],
    "26": ["Uttar Pradesh", "Uttarakhand"], "27": ["Uttar Pradesh"], "28": ["Uttar Pradesh"],
    "29": ["Rajasthan"], "30": ["Rajasthan"], "31": ["Rajasthan"], "32": ["Rajasthan"], "33": ["Rajasthan"],
    "34": ["Rajasthan"], "35": ["Rajasthan"],
    "36": ["Gujarat"], "37": ["Gujarat"], "38": ["Gujarat"], "39": ["Gujarat"],
    "40": ["Maharashtra"], "41": ["Maharashtra"], "42": ["Maharashtra"], "43": ["Maharashtra"], "44": ["Maharashtra"],
    "45": ["Madhya Pradesh"], "46": ["Madhya Pradesh"], "47": ["Madhya Pradesh"],
    "48": ["Chhattisgarh"], "49": ["Chhattisgarh"],
    "403": ["Goa"],
    "50": ["Andhra Pradesh"], "51": ["Andhra Pradesh"], "52": ["Andhra Pradesh"], "53": ["Andhra Pradesh"],
    "54": ["Telangana"], "55": ["Telangana"],
    "56": ["Karnataka"], "57": ["Karnataka"], "58": ["Karnataka"], "59": ["Karnataka"],
    "60": ["Tamil Nadu"], "61": ["Tamil Nadu"], "62": ["Tamil Nadu"], "63": ["Tamil Nadu"], "64": ["Tamil Nadu"],
    "65": ["Tamil Nadu"], "66": ["Tamil Nadu"],
    "67": ["Kerala"], "68": ["Kerala"], "69": ["Kerala"],
    "70": ["West Bengal"], "71": ["West Bengal"], "72": ["West Bengal"], "73": ["West Bengal"], "74": ["West Bengal"],
    "737": ["Sikkim"],
    "75": ["Odisha"], "76": ["Odisha"], "77": ["Odisha"],
    "78": ["Assam"],
    "79": ["Arunachal Pradesh"],
    "796": ["Mizoram"], "793": ["Meghalaya"], "799": ["Tripura"], "795": ["Manipur"],
    "80": ["Bihar", "Jharkhand"], "81": ["Bihar", "Jharkhand"], "82": ["Bihar", "Jharkhand"],
    "83": ["Bihar", "Jharkhand"], "84": ["Bihar", "Jharkhand"], "85": ["Bihar", "Jharkhand"], "86": ["Bihar", "Jharkhand"],
    "87": ["Nagaland"],
    "88": ["Assam"], "89": ["Assam"],
    "90": ["APS"], "91": ["APS"], "92": ["APS"], "93": ["APS"], "94": ["APS"],
    "95": ["APS"], "96": ["APS"], "97": ["APS"], "98": ["APS"], "99": ["APS"]
    }

    def extract_pincode(pincode):
        pincode = str(pincode)
        if pincode.startswith(('403', '795', '737', '796', '799')):
            prefix = pincode[:3]
            suffix = pincode[3:]
        else:
            prefix = pincode[:2]
            suffix = pincode[2:]
        return prefix, suffix

    input_df[['pincode_prefix', 'pincode_suffix']] = input_df['pincode'].apply(
        lambda x: pd.Series(extract_pincode(x)))

    def correct_pincode(row):
        correct_prefixes = [k for k, v in state_pincode_mapping.items() if row['state'] in v]
        if correct_prefixes:
            correct_prefix = correct_prefixes[0]
            suffix = row['pincode_suffix']
            suffix = suffix.zfill(6 - len(correct_prefix))
            return correct_prefix + suffix
        return row['pincode']

    input_df['pincode'] = input_df.apply(correct_pincode, axis=1)
    input_df.drop(columns=['pincode_prefix', 'pincode_suffix'], inplace=True)

    # Hash city, state, and pincode columns
    def hash_string(val, digits=2):
        return int(hashlib.md5(val.encode()).hexdigest(), 16) % (10 ** digits)

    input_df['city'] = input_df['city'].astype(str).apply(lambda x: hash_string(x, digits=4))
    input_df['state'] = input_df['state'].astype(str).apply(lambda x: hash_string(x, digits=2))
    input_df['pincode'] = input_df['pincode'].astype(str).apply(lambda x: hash_string(x, digits=8))
    input_df['customer_id'] = input_df['customer_id'].astype(str).apply(lambda x: hash_string(x, digits=8))
    input_df['gender'] =input_df['gender'].map({'M': 0, 'F': 1})
    for col in ['plan_type', 'engagement_type', 'telecom_partner']:
        input_df[col] = input_df[col].map(input_df[col].value_counts())
    # Apply model to make prediction
    cols_to_transform = ['calls_made', 'sms_sent', 'data_used']



    input_df[cols_to_transform] = pt.fit_transform(input_df[cols_to_transform])
    # Ensure consistent types


    if st.button("Predict Churn"):
        input_scaled = input_df.drop(['customer_id', 'date_of_registration', 'registration_month', 'gender'],
                                     axis=1)
        input_scaled = scaler.transform(input_scaled)
        input_array = np.array(input_scaled)

        prediction = modelxg.predict(input_array)

        st.success(f"Predicted Churn: {'Yes' if prediction[0] == 1 else 'No'}")





# Run the Streamlit app
if __name__ == "__main__":
    run()
