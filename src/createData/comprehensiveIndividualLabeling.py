"""A program to determine health risks with fitness data."""

import pandas as pd
from pymed import PubMed


def label_cardiovascular_disease(df):
    """Label cardiovascular disease risk based on physical activity and hours sitting."""
    df.CD = df.CD.astype(str)
    for i, j in df.iterrows():
        physical_activity = (
            j["Minutes_moderate_activity"] + j["Minutes_intense_activity"]
        )
        hours_sitting = j["Minutes_sitting"] / 60
        if physical_activity < 30 and hours_sitting > 8:
            df.at[i, "CD"] = "Cardiovascular disease"

            # and j["BP"] >= 130 and j["HR"] >= 80


def label_metabolic_syndrome(df):
    """Label metabolic syndrome risk based on hours sitting and daily steps."""
    df.MS = df.MS.astype(str)
    for i, j in df.iterrows():
        hours_sitting = j["Minutes_sitting"] / 60
        if j["Steps"] < 7500 and hours_sitting > 8:
            df.at[i, "MS"] = "Metabolic syndrome"
            # and j["BP"] >= 130


def label_diabetes(df):
    """Label type II diabetes risk based on physical activity and daily steps."""
    df.Diabetes = df.Diabetes.astype(str)
    for i, j in df.iterrows():
        physical_activity = (
            j["Minutes_moderate_activity"] + j["Minutes_intense_activity"]
        )
        if physical_activity < 30 and j["Steps"] < 7500:
            df.at[i, "Diabetes"] = "Type II Diabetes"
            # and j["BP"] >= 120


def label_health_risks(df):
    """Determine health risks based on labels, or lack of labels."""
    df.Health = df.Health.astype(str)
    health = " "
    for i, j in df.iterrows():
        if j["CD"] != "nan":
            health = health + "Cardiovascular Disease, "
        if j["MS"] != "nan":
            health = health + "Metabolic Syndrome, "
        if j["Diabetes"] != "nan":
            health = health + "Type II Diabetes "
        if j["CD"] == "nan" and j["MS"] == "nan" and j["Diabetes"] == "nan":
            health = "Good health"
        df.at[i, "Health"] = health
        health = ""


def create_labels(df):
    """Label data with corresponding 0,1,2 for machine learning."""
    # Good Health: 0
    # Cardiovascular disease risk: 1
    # Metabolic syndrome risk: 2
    # Type II diabetes risk: 3
    df.Labels = df.Labels.astype(str)
    labels = ""
    for i, j in df.iterrows():
        if j["CD"] != "nan":
            labels = labels + "1, "
        if j["MS"] != "nan":
            labels = labels + "2, "
        if j["Diabetes"] != "nan":
            labels = labels + "3"
        if j["CD"] == "nan" and j["MS"] == "nan" and j["Diabetes"] == "nan":
            labels = "0"
        df.at[i, "Labels"] = labels
        labels = ""


if __name__ == "__main__":
    individual_data = pd.read_csv("individual_data.csv")
    label_cardiovascular_disease(individual_data)
    label_metabolic_syndrome(individual_data)
    label_diabetes(individual_data)
    label_health_risks(individual_data)
    create_labels(individual_data)
    individual_data.to_csv("individual_data.csv")