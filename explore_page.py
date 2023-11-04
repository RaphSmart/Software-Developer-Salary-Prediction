import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt 



@st.cache_data # This decorator catches this finction so that once it loads it catches it so it does not have to reload again
def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

def load_data():
    df = pd.read_csv("/Users/raphsmart/Desktop/Raph_projects/SoftwareDeveloperSalaryPrediction/dataset /stack-overflow-developer-survey-2020/survey_results_public.csv")
    df_new = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df_new = df_new.rename({"ConvertedComp": "Salary"}, axis=1)
    df_new = df_new[df_new["Salary"].notnull()]
    df_new = df_new.dropna()
    df_new = df_new[df_new["Employment"] == "Employed full-time"]
    df_new = df_new.drop("Employment", axis=1)

    country_map = shorten_categories(df_new.Country.value_counts(), 400)
    df_new['Country'] = df_new['Country'].map(country_map)
    df_new = df_new[df_new["Salary"] <= 250000]
    df_new = df_new[df_new["Salary"] >= 10000]
    df_new = df_new[df_new['Country'] != 'Other']

    df_new['YearsCodePro'] = df_new['YearsCodePro'].apply(clean_experience)
    df_new['EdLevel'] = df_new['EdLevel'].apply(clean_education)

    return df_new

df = load_data()

# displays page
def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
        ### Stack Overflow Developer Survey 2020
        """
    )


    # display chats

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=90)
    ax1.axis("equal") # Equal aspect ratio, ensures that pie is drawn as a circle.

    st.write("""#### Nuber of Data from different countries""")

    st.pyplot(fig1)

    st.write(
        """
        ### Mean Salary Based on Country
        """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)