import streamlit as st
import pandas as pd
from math import factorial

# Function for calculating combinations
def combinations(n, k):
    return factorial(n) / (factorial(k) * factorial(n - k))

# DataFrame structure and handle partial matches
def calculate_probability(numbers, winning_numbers, historical_data):
    n_combinations_ticket = combinations(6, winning_numbers)
    n_combinations_remaining = combinations(43, 6 - winning_numbers)
    successful_outcomes = n_combinations_ticket * n_combinations_remaining

    n_combinations_total = combinations(49, 6)
    probability = successful_outcomes / n_combinations_total
    probability_percentage = probability * 100

    # Adjust the logic to count partial matches
    partial_match_count = 0
    for index, row in historical_data.iterrows():
        draw_numbers = set(row['AggregatedNumbers'])  # Convert list to set for efficient lookups
        user_numbers_set = set(numbers)  # Ensure user numbers are also in a set
        match_count = len(user_numbers_set.intersection(draw_numbers))

        if match_count == winning_numbers:
            partial_match_count += 1

    return f"The probability of having exactly {winning_numbers} winning numbers is: {probability_percentage:.6f}%. Your selected numbers have matched {winning_numbers} winning numbers in past draws {partial_match_count} times."

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
        result = calculate_probability(numbers_list, winning_numbers, historical_data)
        st.success(result)
    else:
        st.error("Please enter exactly six unique numbers, each between 1 and 49.")
