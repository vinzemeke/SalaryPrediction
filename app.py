from sklearn.metrics import mean_absolute_error
import streamlit as st
from explore_page import show_explore_page
from predict_page import show_predict_page



def main():
    menu = st.sidebar.radio('Menu', ('Predict', 'Explore', 'Model info'))
    if(menu == "Predict"):
        show_predict_page()
    elif(menu == "Explore"):
        show_explore_page()




if __name__ == '__main__':
    main()