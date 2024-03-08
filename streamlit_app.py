import streamlit as st
import pandas as pd
import plotly.express as px
from math import factorial

# Function for calculating combinations
def combinations(n, k):
    return factorial(n) / (factorial(k) * factorial(n - k))

# Function to calculate partial matches in historical data
def calculate_partial_matches(numbers, historical_data):
    match_counts = {n: 0 for n in range(2, 6)}

    for index, row in historical_data.iterrows():
        draw_numbers = set(row['AggregatedNumbers'])
        user_numbers_set = set(numbers)
        match_count = len(user_numbers_set.intersection(draw_numbers))

        if match_count in match_counts:
            match_counts[match_count] += 1

    return match_counts

# Function to calculate the probability of winning
def calculate_probability(numbers, winning_numbers, historical_data):
    n_combinations_ticket = combinations(6, winning_numbers)
    n_combinations_remaining = combinations(43, 6 - winning_numbers)
    successful_outcomes = n_combinations_ticket * n_combinations_remaining

    n_combinations_total = combinations(49, 6)
    probability = successful_outcomes / n_combinations_total
    probability_percentage = probability * 100

    partial_match_counts = calculate_partial_matches(numbers, historical_data)
    partial_match_count = partial_match_counts.get(winning_numbers, 0)

    return f"The probability of having exactly {winning_numbers} winning numbers is: {probability_percentage:.6f}%. Your selected numbers have matched {winning_numbers} winning numbers in past draws {partial_match_count} times.", partial_match_counts

# Load historical data
historical_data = pd.read_csv("649.csv")
historical_data['AggregatedNumbers'] = historical_data.apply(lambda row: [row[f'NUMBER DRAWN {i}'] for i in range(1, 7)], axis=1)

# Streamlit app UI setup
st.title('Lottery Probability Calculator')

user_numbers = st.text_input("Enter your six numbers separated by commas (e.g., 1,2,3,4,5,6)")

winning_numbers = st.selectbox(
    "Select the number of winning numbers you're interested in",
    options=[2, 3, 4, 5]
)

if st.button('Calculate Probability'):
    numbers_list = [int(n.strip()) for n in user_numbers.split(',') if n.strip().isdigit()]

    if len(numbers_list) == 6 and all(1 <= n <= 49 for n in numbers_list) and len(set(numbers_list)) == 6:
        message, match_counts = calculate_probability(numbers_list, winning_numbers, historical_data)
        st.success(message)
        
        # Plotting the frequency of partial matches
        match_data = pd.DataFrame({
            'Match Count': list(match_counts.keys()),
            'Frequency': list(match_counts.values())
        })
        
        fig = px.bar(match_data, x='Match Count', y='Frequency', title='Frequency of Partial Matches in Historical Draws')
        st.plotly_chart(fig)
        
    else:
        st.error("Please enter exactly six unique numbers, each between 1 and 49.")
