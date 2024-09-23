import streamlit as st
import pandas as pd
import os

# Load the CSV file (adjust the path if necessary)
data_path = 'PartITI2024.csv'
parts_df = pd.read_csv(data_path)

# Function to show the diagram for the selected model (placeholder for images)
def show_diagram(model):
    image_file = os.path.join("diagrams", f"{model}.png")
    if os.path.exists(image_file):
        st.image(image_file, caption=f"Diagram for {model}")
    else:
        st.write("No diagram available for this model.")

# Set up the Streamlit app interface
st.title("Part Finder")

# Step 1: Input box for model number
model_input = st.text_input("Enter your model number", "")

if model_input:
    # Filter the data based on the model number
    filtered_df = parts_df[parts_df['Model'] == model_input]
    
    if not filtered_df.empty:
        # Step 2: Dropdown for part description (TCLNA)
        part_description = st.selectbox("Select Part Description (TCLNA)", filtered_df['Part Description (TCLNA)'].unique())
        
        # Filter based on selected part description
        selected_part = filtered_df[filtered_df['Part Description (TCLNA)'] == part_description]
        
        if not selected_part.empty:
            # Outcome: Display Part Number, Alternate Part Number, and Type
            st.write(f"**Part Number**: {selected_part['Part No.'].values[0]}")
            st.write(f"**Type**: {selected_part['Type'].values[0]}")
            st.write(f"**Year Sold**: {selected_part['Year Sold'].values[0]}")
            
            # Step 3: Button to show the price (correct column name with space)
            if st.button("Do you want to know the price?"):
                st.write(f"**Price**: ${selected_part[' Price '].values[0]}")
            
            # Step 4: Button to show the diagram
            if st.button("Do you want to see the diagram for this model?"):
                show_diagram(model_input)
        else:
            st.write("No parts found for the selected description.")
    else:
        st.write("Model number not found.")
else:
    st.write("Please enter a model number to get started.")
