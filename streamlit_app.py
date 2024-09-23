import streamlit as st
import pandas as pd
import spacy

# Load spaCy model for NLP
nlp = spacy.load('en_core_web_sm')

# Load the main CSV file (ensure it exists in your workspace)
data_path = 'PartITI2024.csv'
try:
    parts_df = pd.read_csv(data_path)
except FileNotFoundError:
    st.error(f"File not found: {data_path}. Please ensure the file is uploaded.")
    st.stop()

# Load additional Excel file for images and NOs
new_file_path = 'H25D44W.xlsx'
try:
    image_df = pd.read_excel(new_file_path)
except FileNotFoundError:
    st.error(f"File not found: {new_file_path}. Please ensure the file is uploaded.")
    st.stop()

# Set up the chatbot interface
st.title("Parts Information Chatbot")

# Chat input box
user_input = st.text_input("Ask me about a part (e.g., 'Show me part for model H25'):")

if user_input:
    doc = nlp(user_input)
    model_mentioned = None

    # Extract potential model number from the input
    for token in doc:
        if token.text.isdigit() or (token.text.isalpha() and token.text.startswith("H")):
            model_mentioned = token.text
            break

    if model_mentioned:
        # Filter parts data based on the model number
        filtered_df = parts_df[parts_df['Model'].str.contains(model_mentioned, case=False)]
        if not filtered_df.empty:
            st.write(f"Parts found for model: {model_mentioned}")
            part_description = st.selectbox("Select Part Description (TCLNA)", filtered_df['Part Description (TCLNA)'].unique())

            selected_part = filtered_df[filtered_df['Part Description (TCLNA)'] == part_description]
            if not selected_part.empty:
                # Display the part details
                st.write(f"**Part Number**: {selected_part['Part No.'].values[0]}")
                st.write(f"**Alternate Part Number**: {selected_part['Alternate Part No.'].values[0]}")
                st.write(f"**Price**: ${selected_part['Price'].values[0]}")
                st.write(f"**Type**: {selected_part['Type'].values[0]}")
                st.write(f"**Year Sold**: {selected_part['Year Sold'].values[0]}")

                # Check for image and NO from the additional file
                part_no = selected_part['Part No.'].values[0]
                image_info = image_df[image_df['Part No.'] == part_no]
                if not image_info.empty:
                    st.image(image_info['Image URL'].values[0], caption=f"Image for Part {part_no}")
                    st.write(f"**NO.**: {image_info['NO'].values[0]}")
                else:
                    st.write("No image found for this part.")
            else:
                st.write("No parts found for the selected description.")
        else:
            st.write("Model number not found.")
    else:
        st.write("Please ask about a specific model.")
