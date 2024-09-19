import re
from datetime import datetime, timedelta
import streamlit as st

st.title("Query Expander")

long_string = st.text_area(
    "Please enter the query to expand. This app will take the given query block and append a duplicate the given query block with an incremented date (standard format: _YYYYMMDD) with a UNION ALL. \n If your block has a suffix like GROUP BY or ORDER BY, add it in the second text box.",
    ""
)

short_string=st.text_area("Please enter suffix here:","")
days = st.number_input("Enter the number of days before or after the date in the query (negative value for days before)", step=1,min_value=-100, max_value=100, value=0)

def generate_union_strings(long_string, short_string, days):
    # regex to match dates in the form yyyymmdd after _
    pattern = r'_(\d{8})' 
    # List to hold all the resulting strings (original + new versions)
    result_strings = [long_string]  # Start with the original string
    # Loop through each day offset (positive or negative based on `days`)
    for day_offset in range(1, abs(days) + 1):
        # Calculate the increment or decrement direction based on the sign of days
        day_delta = day_offset if days > 0 else -day_offset
        # Function to iterate (increment or decrement) the date
        def iterate_date(match):
            # Extract the date string from the match
            date_str = match.group(1)    
            # Convert the string to a datetime object
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            # Increment or decrement the date by the specified day_delta
            new_date_obj = date_obj + timedelta(days=day_delta)
            # Convert the new datetime back to string in yyyymmdd format
            new_date_str = new_date_obj.strftime('%Y%m%d')
            # Return the new date in the form _yyyymmdd (preserving the _)
            return f"_{new_date_str}"
        # Generate a new version of the string by replacing each date with the iterated date
        new_string = re.sub(pattern, iterate_date, long_string)
        result_strings.append(new_string)
    final_result = " UNION ALL \n".join(result_strings)+"\n"+short_string
    return final_result

result = generate_union_strings(long_string, short_string, days)

text_contents = result
st.download_button("Download Expanded Query", text_contents, file_name="Expanded Query.txt")

st.code(result, language="sql")


