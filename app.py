import streamlit as st
import pickle
import numpy as np


@st.cache_resource
def load_model():
    with open("final_model.pkl", "rb") as file:
        model = pickle.load(file)
    return model

model = load_model()


insurance_map = {
    'Comprehensive': 0,
    'Third Party insurance': 1,
    'Third Party': 1,
    'Zero Dep': 2,
    'Not Available': 3
}

fuel_map = {'Petrol': 0, 'Diesel': 1, 'CNG': 2}

owner_map = {
    'First Owner': 1,
    'Second Owner': 2,
    'Third Owner': 3,
    'Fourth Owner': 4,
    'Fifth Owner': 5
}

transmission_map = {'Manual': 0, 'Automatic': 1}


# ---- PAGE ----
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚘",   # small change icon
    layout="centered"
)

# ---- SIMPLE BLACK UI ----
st.markdown("""
<style>
.stApp {
    background-color: #000000;
    color: white;
}
h1 {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# ---- TITLE ----
st.title("Used Car Price Predictor")
st.caption("Simple resale value estimator")  # changed subtitle

st.markdown("---")


# ---- INPUT SECTION ----
st.subheader("Enter Details")

col1, col2 = st.columns(2)

with col1:
    insurance = st.selectbox("Insurance", list(insurance_map.keys()))
    fuel = st.selectbox("Fuel", list(fuel_map.keys()))
    owner = st.selectbox("Owner Type", list(owner_map.keys()))

with col2:
    transmission = st.selectbox("Transmission", list(transmission_map.keys()))
    kms_driven = st.number_input("KMs Driven", min_value=0, max_value=300000, step=1000)  # changed slider → input


st.markdown("")


# ---- BUTTON ----
if st.button("Predict Price", use_container_width=True):

    try:
        input_data = np.array([[
            insurance_map[insurance],
            fuel_map[fuel],
            kms_driven,
            owner_map[owner],
            transmission_map[transmission]
        ]])

        prediction = model.predict(input_data)[0]

        st.markdown("---")

        # ---- RESULT (Changed UI style slightly) ----
        st.success(f"Estimated Price: ₹ {prediction:.2f} Lakhs")

        # Slightly changed logic text
        if prediction < 5:
            st.write("Segment: Budget")
        elif prediction < 15:
            st.write("Segment: Mid-range")
        else:
            st.write("Segment: Premium")

    except Exception as e:
        st.error(f"Error: {e}")


st.markdown("---")
st.caption("Streamlit ML App")