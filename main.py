import streamlit as st
import pandas as pd
import altair as alt
from sklearn.linear_model import LinearRegression

DATA_URL = "https://www.kaggle.com/datasets/imrulhasanrobi/world-population-all-countries-different-parameter"
PATH_TO_DATA = "world_population.csv"
GITHUB_URL = "https://github.com/rajinsyed/Capstone-Project"
DEPLOYED_URL = "https://rajinsyed-capstone-project-main-lep1nx.streamlit.app/"

st.title("World Population Analysis")

st.write("---")

# caching the data
@st.cache_data 
def get_population():
    return pd.read_csv(PATH_TO_DATA)

data = get_population()

data['Population(2020)'] = data['Population(2020)'].str.replace(',', '').astype(int)

# Replace 'N.A.' values with NaN
data = data.replace('N.A.', pd.NA)

# -------------------------- pie chart ------------------------------
# What's the total population in this world? 

# Select the columns to use for the pie chart
country_data = data[['Country or Dependency', 'Population(2020)']].dropna()

# find total world population
total_world_population = country_data['Population(2020)'].sum()

# Sort the data by population in descending order
country_data = country_data.sort_values(by='Population(2020)', ascending=False)

# Get the top 10 countries by population and combine the others
top_countries = country_data.head(10)
others = pd.DataFrame({
    'Country or Dependency': ['Others'],
    'Population(2020)': [country_data[10:]['Population(2020)'].sum()]
})

# Combine the top countries and others into a single dataframe
combined_data = pd.concat([top_countries, others])

# find the percentage of each country
combined_data['Population %'] = combined_data['Population(2020)'] / total_world_population * 100

# Create the pie chart using Altair
pie = alt.Chart(combined_data).mark_arc().encode(
    theta='Population(2020)',
    color=alt.Color('Country or Dependency',scale=alt.Scale(range=["#1f77b4", "#F8D37A", "#57AD9E", "#EA4339", "#6641B9", "#8c564b", "#F3AFAD", "#93C7FA", "#bcbd22", "#D6DAE4", "#a93226"])),
    tooltip=[alt.Tooltip('Country or Dependency'), alt.Tooltip('Population(2020)', format=',', title="Population"), alt.Tooltip('Population %', format='.2f', title="Percentage (%)")],
).properties(
    width=600,
    height=400,
    title='Whats the total population in this world?' 
)

# Show the pie chart in Streamlit
st.altair_chart(pie)

# write the total pop
st.caption(f"Total population: **{total_world_population:,}**.")

# Description
st.write("### Description")
st.write(f"This pie chart shows the distribution of the world's population. The chart displays the top 10 countries by population and combines the rest of the countries into an \"Others\" category. Hovering over each section of the pie chart shows the name of the country, its population and the percentage of the world's population that it represents. The total population of the world is **{total_world_population:,}**. China and India are the two countries with the highest populations in the world.")

st.write('-----')

# -------------------------- bar chart ------------------------------
#   Bar chart

# Group the data by regions and sum the population for each region
df_regions = data.groupby("Regions")["Population(2020)"].sum().reset_index()

# Sort the data by population in descending order
df_regions = df_regions.sort_values("Population(2020)", ascending=False)

# Create the Altair chart
chart = alt.Chart(df_regions).mark_bar().encode(
    x=alt.X("Population(2020)", axis=alt.Axis(tickCount=5, labelExpr='datum.value / 1E9 + "B"')),
    y=alt.Y("Regions", sort="-x"),
    color=alt.Color("Regions", legend=None),
    tooltip=[alt.Tooltip("Regions"), alt.Tooltip("Population(2020)",format=",", title="Population")]
).properties(
    width=600,
    height=400,
    title="Which regions have the highest population?"
)

# Display the chart using Streamlit
st.altair_chart(chart)

# Description
st.write("### Description")
st.write(f"This bar chart shows the total population of different regions in the world. The chart reveals that the top three regions with the highest population are Asia, Africa, and Europe, North America, South America, and Oceania have comparatively lower populations. The Y-axis shows the regions, sorted in descending order based on their population. The X-axis represents the population, in billions. You can hover over each bar to see the name of the region and its corresponding population.")


st.write('----------')

# -------------------------- bar chart ------------------------------
# Which countries experienced the highest net change in 1 year in population? Bar chart

# Convert "Net Change" column to numeric
data["Net Change"] = pd.to_numeric(data["Net Change"].str.replace(",", ""))

# Sort the dataframe by "Net Change" column in descending order
data = data.sort_values(by=["Net Change"], ascending=False).reset_index(drop=True)

# Select the top 10 countries with the highest net change in population
top_countries = data.iloc[:10]

# Create the bar chart
chart = alt.Chart(top_countries).mark_bar().encode(
    x=alt.X("Country or Dependency:N", sort="-y"),
    y=alt.Y("Net Change:Q"),
    tooltip=[alt.Tooltip("Country or Dependency"), alt.Tooltip("Net Change",format=",")]
).properties(
    title="Which countries experienced the highest net change in 1 year in population?"
)

# Display the chart using Streamlit
st.altair_chart(chart, use_container_width=True)

# Description
st.write("### Description")
st.write("This bar chart shows the top 10 countries that experienced the highest net change in population in 1 year. The net change is calculated by subtracting the number of deaths from the number of births, and adding the net migration to the population. The countries are sorted in descending order based on their net change values. Hover over each bar to see the name of the country and the net change value in millions.")


st.write('----------')

# -------------------------- bar chart ------------------------------
# Which countries have the highest population density? Horizontal Bar chart

data["Density(p/km^2)"] = pd.to_numeric(data["Density(p/km^2)"].str.replace(",", ""))

# Sort the data by population density in descending order
df_density = data.sort_values("Density(p/km^2)", ascending=False)

# Create the Altair chart
chart = alt.Chart(df_density.head(10)).mark_bar().encode(
    x=alt.X("Density(p/km^2)", axis=alt.Axis(format=",.0f")),
    y=alt.Y("Country or Dependency", sort="-x"),
    color=alt.Color("Density(p/km^2)", scale=alt.Scale(scheme='reds')),
    tooltip=[alt.Tooltip("Country or Dependency"), alt.Tooltip("Density(p/km^2)", format=",.0f")],
).properties(
    width=600,
    height=400,
    title="Which countries have the highest population density?"
)

# Display the chart using Streamlit
st.altair_chart(chart)

# Description
st.write("### Description")
st.write("This visualization is a horizontal bar chart that shows the top 10 countries with the highest population density. Population density is calculated by dividing a country's population by its land area. The countries are sorted in descending order based on their population density, and the bars are colored based on their density value. The chart shows that the top countries with the highest population density are mostly small islands and city-states.")


st.write('----------')

# -------------------------- pie chart ------------------------------
# What percentage of the world's population lives in urban areas? Pie chart

# Drop rows with NaN values in the Urban column
data = data.dropna(subset=['Urban'])

data["Urban"] = data["Urban"].str.rstrip("%").astype("float")

urban_population = data["Population(2020)"] * data["Urban"] / 100
total_urban_population = urban_population.sum()

# Calculate the percentage of urban population for each country
data["Urban"] = data["Urban"] * data["Population(2020)"] / 100

# Group by regions and sum the urban population
data_grouped = data.groupby("Regions")["Urban"].sum().reset_index()

# Percentage of world population that lives in urban areas
percentage_of_urban = total_urban_population / total_world_population  * 100

# get percentage from total urban population
data_grouped["Urban %"] = data_grouped["Urban"] / total_urban_population * 100


# Create a pie chart using altair
pie = alt.Chart(data_grouped).mark_arc().encode(
    theta="Urban",
    color=alt.Color('Regions', scale=alt.Scale(range=['#93C7FA', '#2B66C2', '#F3AEAD', '#EA4339', '#9AECA7', '#FBEA64'])),
    tooltip=[alt.Tooltip("Regions"), alt.Tooltip("Urban", format=",.0f", title="Urban Population"),alt.Tooltip("Urban %", format=",.2f", title="Percentage (%)"),]
).properties(
    width=600,
    height=400,
    title="What percentage of the world's population lives in urban areas? "
)

# Display the pie chart using streamlit
st.altair_chart(pie)

# show the total of world population that lives in urban areas
st.caption(f'Total of world population that lives in urban areas: {total_urban_population:,.0f}')

# show the percentage of world population that lives in urban areas
st.caption(f'Percentage of world population that lives in urban areas: {percentage_of_urban:.2f}%')

# Description
st.write("### Description")
st.write("This visualization shows the percentage of the world's population that lives in urban areas. The pie chart is colored based on regions and each slice represents the percentage of urban population for that region. The tooltip displays the name of the region, the total urban population and the percentage of urban population for that region. The total urban population in the world and the percentage of the world's population that lives in urban areas are displayed below the pie chart.")

st.write('----------')

# -------------------------- PDA ------------------------------

st.write("### Predicting the population (Predictive Analysis)")

# # Cleaning the data
data["Yearly Change"] = data["Yearly Change"].str.rstrip("%").astype("float")

# Train a linear regression model
features = ["Yearly Change", "Net Change"]
X = data[features]
y = data["Population(2020)"]
model = LinearRegression().fit(X, y)

# Predict the population in X years in the future (The dataset's population is from 2020)
prediction_year = 10

future_population_list = [total_world_population]

# run a for loop for find the prediction for the next prediction_years
for i in range(prediction_year):
    future_yearly_change = data["Yearly Change"].mean() * (i + 1)
    future_net_change = data["Net Change"].mean() * (i + 1)
    future_X = [[future_yearly_change, future_net_change]]
    future_population_increase = model.predict(future_X)[0] * (i + 1)
    future_population = total_world_population + future_population_increase

    # append the future population to the list
    future_population_list.append(future_population)


# Create a dataframe for the predicted population from 2020 to 2030
df = pd.DataFrame({
    "Year": [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029,2030],
    "Population": future_population_list
})

# Create a bar chart using Altair
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("Year:O", title="Year"),
    y=alt.Y("Population:Q", title="World Population"),
    color=alt.condition(
        alt.datum.Year == 2020,
        alt.value("steelblue"),
        alt.value("orange")
    ),
    tooltip=[alt.Tooltip("Year"), alt.Tooltip("Population", format=",.0f")],
).properties(
    width=600,
    height=400,
    title=f"World Population from 2020 to 2030"
)

# Show the chart
st.altair_chart(chart)


# Description
st.write("### Description")
st.write("This visualization shows the predicted world population from 2020 to 2030 using a linear regression model based on the data from the dataset. The predicted population takes into account the yearly change and net change of the world population. The bar chart shows the world population on the y-axis and the year on the x-axis. The blue bar represents the actual population in 2020 (the metrics in the dataset was of 2020), while the orange bars represent the predicted population from 2021 to 2030. Hovering over the bars displays the year and the corresponding population in the tooltip. This visualization provides insights into the future world population trend based on the current data.")

