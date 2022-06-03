
import streamlit as st
import pickle
import numpy as np 
import pandas as pd



#loading the model:
def load_model():
    with open("saved_steps.pk1", 'rb') as file:
        data = pickle.load(file)
    return(data)

#load the data
data = load_model()
model = data['model']
column_encoder2 = data['column_encoder']
scaler_pickle = data['scaler']



#the prediction method
def predict(country, education, years_of_experience):
    input = [[country, education, int(years_of_experience)]]
    cols = ['Country', 'EdLevel', 'YearsCodePro']
    input = pd.DataFrame(input, columns= cols)
    input = pd.DataFrame(column_encoder2.transform(input).toarray())
    result = model.predict(input)
    result = scaler_pickle.inverse_transform(result.reshape(-1,1))
    return(result[0][0])

def show_predict_page():
    st.title("Software Developer Salaries Prediction")

    st.markdown('#### We need some information to predict the salary')

    #list the countries for the dropdown:

    countries = ['Sweden',
                 'Spain',
                'Germany',
                'Turkey',
                'Canada',
                'France',
                'Switzerland',
                'United Kingdom',
                'Russia',
                'Israel',
                'Other',
                'United States of America',
                'Brazil',
                'Italy',
                'Netherlands',
                'Poland',
                'Australia',
                'India',
                'Norway']

    years = (np.arange(0,31,1))

    education_level = ['No bachelors', 'Bachelors', 'Post-grad']

    country = st.selectbox("Select Countries", sorted(countries))
    education = st.selectbox("Education Level", sorted(education_level))
    experience = st.slider("Years of Experience",0,30,3,1)
    calculate = st.button("Predict Salary")

    if(calculate):
        result = predict(country, education, experience)
        st.markdown('##### The predicted salary is {:,.0f} USD'.format(result))

    


#the loaded part of the dataframe:
