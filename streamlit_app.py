import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Algorithm Time Complexities',
    page_icon=':bar_chart:',  # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def load_data():
    """Load data from the CSV files."""
    # Load data for 'data.csv'
    data_filename = Path(__file__).parent/'data.csv'
    data_df = pd.read_csv(data_filename)

    # Load data for 'times_data.csv'
    times_filename = Path(__file__).parent/'times_data.csv'
    times_df = pd.read_csv(times_filename)

    return data_df, times_df

# Load data
data_df, times_df = load_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :bar_chart: Algorithm Time Complexity Dashboard

Explore and visualize the time complexities of different sorting algorithms based on your provided data.
'''

# Add some spacing
''

# Display the datasets
st.subheader("Dataset 1: Data.csv Overview")
st.write(data_df.head())

st.subheader("Dataset 2: Times_data.csv Overview")
st.write(times_df.head())

# Add a slider to filter data by size category in `data_df`
min_size = int(data_df['category'].min())
max_size = int(data_df['category'].max())

selected_size_range = st.slider(
    'Select the size range of data you are interested in:',
    min_value=min_size,
    max_value=max_size,
    value=(min_size, max_size))

filtered_data_df = data_df[(data_df['category'] >= selected_size_range[0]) & 
                           (data_df['category'] <= selected_size_range[1])]


st.subheader("Filtered Data.csv based on Size Category")
st.write(filtered_data_df)

# Allow selection of algorithms to display from `times_df`
algorithms = times_df.columns.tolist()[1:-1]  
selected_algorithms = st.multiselect(
    'Select the algorithms you want to visualize:',
    algorithms,
    default=algorithms)  # Default to all algorithms

# Filter `times_df` based on selected algorithms
filtered_times_df = times_df[['size'] + selected_algorithms]


st.subheader("Filtered Times Data.csv")
st.write(filtered_times_df)

st.header('Time Complexity Visualization for Selected Algorithms')
st.line_chart(
    filtered_times_df.set_index('size')
)
st.header('Algorithm Performance Comparison', divider='gray')

cols = st.columns(3) 

for i, algorithm in enumerate(selected_algorithms):
    col = cols[i % len(cols)]

    with col:
        
        first_time = filtered_times_df[algorithm].iat[0]
        last_time = filtered_times_df[algorithm].iat[-1]

        if math.isnan(first_time):
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{last_time / first_time:.2f}x'
            delta_color = 'normal'

        st.metric(
            label=f'{algorithm} Time Complexity',
            value=f'{last_time:.4f}',
            delta=growth,
            delta_color=delta_color
        )
