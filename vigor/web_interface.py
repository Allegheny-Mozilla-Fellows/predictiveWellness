"""A program to create a Streamlit web interface for Vigor."""
from classificationAlgorithms import decision_tree
from classificationAlgorithms import naive_bayes
from classificationAlgorithms import support_vector_machine as svm
from createData import comprehensive_individual_labeling as label
from createData import create_custom_individual as custom_individual
from createData import create_individual_data as provided_individual
from databaseAccess import health_query

import streamlit as st
import pandas as pd


def individual_analysis_type():
    """Determine what type of individual data should be analyzed."""
    individual_data = st.selectbox(
        "Would you like to analyze provided or customized data?",
        ["Provided", "Customized"],
    )
    return individual_data


def customized_setup():
    """Input and store personal information for data generation."""
    age = st.number_input("Please enter your age (in years)", min_value=1)
    weight = st.number_input("Please enter your weight (in pounds)", min_value=1.0)
    height = st.number_input("Please enter your height (in inches", min_value=1.0)
    activity_level = st.slider(
        "Please enter your activity level", min_value=1, max_value=5, value=None
    )
    if activity_level == 1:
        st.write("Level 1: Extremely inactive")
    if activity_level == 2:
        st.write("Level 2: Sedentary lifestyle (little to no exercise)")
    if activity_level == 3:
        st.write("Level 3: Moderately active")
    if activity_level == 4:
        st.write("Level 4: Vigorously active")
    if activity_level == 5:
        st.write("Level 5: Extremely active (competitive athlete)")
    kilograms = weight * 0.453592
    meters_squared = height * 0.00064516
    bmi = kilograms / meters_squared
    return age, weight, height, activity_level, bmi


def create_provided_individual():
    """Create data for provided individual info."""
    with st.spinner("Wait for it..."):
        individual_data = pd.read_csv(
            "/home/maddykapfhammer/Documents/Allegheny/MozillaFellows/predictiveWellness/vigor/dataFiles/individual_data.csv"
        )
        data = provided_individual.main(individual_data)
        # st.dataframe(data)
        st.bar_chart(data)
        individual_data.to_csv(
            "/home/maddykapfhammer/Documents/Allegheny/MozillaFellows/predictiveWellness/vigor/dataFiles/individual_data.csv"
        )
    st.success("Complete!")
    return data


def create_custom_individual(age, activity_level):
    """Create data for personalized individual info."""
    with st.spinner("Wait for it..."):
        custom_data = pd.read_csv(
            "/home/maddykapfhammer/Documents/Allegheny/MozillaFellows/predictiveWellness/vigor/dataFiles/customIndividual.csv",
            index_col=[0],
        )
        # Create individual data and print dataframe
        st.header("Generating customized individual data....")
        data = custom_individual.main(age, activity_level, custom_data)
        st.bar_chart(data)
        custom_data.to_csv(
            "/home/maddykapfhammer/Documents/Allegheny/MozillaFellows/predictiveWellness/vigor/dataFiles/customIndividual.csv"
        )
    st.success("Complete!")
    return data


def label_data(data, data_type):
    """Label the data in the dataframe with health risks."""
    with st.spinner("Preparing labeled data..."):
        st.header("Labeling data with health risks....")
        labeled_data = label.main(data)
        if data_type == "Provided":
            labeled_data.to_csv("/home/maddykapfhammer/Documents/Allegheny/MozillaFellows/predictiveWellness/vigor/dataFiles/individual_data.csv")
        if data_type == "Customized":
            labeled_data.to_csv("/home/maddykapfhammer/Documents/Allegheny/MozillaFellows/predictiveWellness/vigor/dataFiles/customIndividual.csv")
        st.dataframe(labeled_data)
        st.success("Complete!")
    return label_data


def classify_data(dataset, data_type):
    """Classify data and health risks with selected classification."""
    st.header("Please Choose Your Method of Classification:")
    naive_classification = st.button("Naive Bayes Classification")
    gini_classification = st.button("Gini Index Decision Tree Classification")
    entropy_classification = st.button("Entropy Decision Tree Classification")
    svm_classification = st.button("Support Vector Machine Classification")

    if naive_classification:
        with st.spinner("Classifying with Naive Bayes..."):
            new_data = naive_bayes.import_data(data_type)
            st.area_chart(new_data["Health"])
            interpretation = naive_bayes.perform_methods(data_type)
            classification_type = "Naive Bayes Classification"
        st.success("Complete!")

    if gini_classification:
        with st.spinner("Classifying with Gini Index..."):
            new_data = decision_tree.import_data(data_type)
            st.area_chart(new_data["Health"])
            interpretation = decision_tree.perform_gini_index(data_type)
        st.success("Complete!")

    if entropy_classification:
        with st.spinner("Classifying with Entropy..."):
            new_data = decision_tree.import_data(data_type)
            st.area_chart(new_data["Health"])
            interpretation = decision_tree.perform_entropy(data_type)
        st.success("Complete!")

    if svm_classification:
        with st.spinner("Classifying with Support Vector Machine..."):
            new_data = svm.import_data(data_type)
            st.area_chart(new_data["Health"])
            interpretation = svm.perform_methods(data_type)
            classification_type = "Support Vector Machine Classification"
        st.success("Complete!")

    return interpretation


def individual_analysis():
    """Perform analysis for individual data."""
    individual_data = individual_analysis_type()
    if individual_data == "Customized":
        age, weight, height, activity_level, bmi = customized_setup()
        data = create_custom_individual(age, activity_level)
        labeled_data = label_data(data, individual_data)
        classify_data(labeled_data, individual_data)
        
    if individual_data == "Provided":
        data = create_provided_individual()
        labeled_data = label_data(data, individual_data)
        classify_data(labeled_data, individual_data)


def query_pubmed(interpretation, amount):
    health_query.perform_methods(interpretation, amount)


def follow():
    """Give contact information with images."""
    st.title("Follow Us")
    st.image(
        # pylint: disable=C0301
        "/home/maddykapfhammer/Documents/Allegheny/MozillaFellows/predictiveWellness/vigor/webInterface/VigorImages/github.png",
        width=500,
    )
    st.image(
        # pylint: disable=C0301
        "/home/maddykapfhammer/Documents/Allegheny/MozillaFellows/predictiveWellness/vigor/webInterface/VigorImages/instagram.png",
        width=300,
    )
    st.image(
        # pylint: disable=C0301
        "/home/maddykapfhammer/Documents/Allegheny/MozillaFellows/predictiveWellness/vigor/webInterface/VigorImages/website.png",
        width=400,
    )


def setup():
    """Perform setup for Streamlit webinterface."""
    st.image(
        # pylint: disable=C0301
        "/home/maddykapfhammer/Documents/Allegheny/MozillaFellows/predictiveWellness/vigor/webInterface/VigorImages/vigor.png",
        width=900,
    )
    st.sidebar.title("Welcome to Vigor!")
    home_menu = st.selectbox(
        "Menu",
        [
            "Home",
            "Data Generation with Faker",
            "Understanding Classification Algorithms",
            "Individual Health Analysis",
            "Community Health Analysis",
            "About Vigor",
        ],
    )
    if home_menu == "Home":
        with open(
            # pylint: disable=C0301
            "/home/maddykapfhammer/Documents/Allegheny/MozillaFellows/predictiveWellness/vigor/webInterface/home_page.md"
        ) as home_file:
            st.markdown(home_file.read())
        follow()
    if home_menu == "Data Generation with Faker":
        with open(
            # pylint: disable=C0301
            "/home/maddykapfhammer/Documents/Allegheny/MozillaFellows/predictiveWellness/vigor/dataGenerationWithFaker/faker_instructions.md"
        ) as faker_file:
            st.markdown(faker_file.read())
        follow()
    if home_menu == "Understanding Classification Algorithms":
        with open(
            # pylint: disable=C0301
            "/home/maddykapfhammer/Documents/Allegheny/MozillaFellows/predictiveWellness/vigor/classificationAlgorithms/classification_description.md"
        ) as classification:
            st.markdown(classification.read())
        follow()
    if home_menu == "Individual Health Analysis":
        individual_analysis()
        follow()
    if home_menu == "Community Health Analysis":
        st.write("Comming Soon!")
        follow()
    if home_menu == "About Vigor":
        with open(
            # pylint: disable=C0301
            "/home/maddykapfhammer/Documents/Allegheny/MozillaFellows/predictiveWellness/vigor/webInterface/about.md"
        ) as about:
            st.markdown(about.read())
        follow()


if __name__ == "__main__":
    setup()
