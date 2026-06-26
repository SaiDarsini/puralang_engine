import streamlit as st
import pandas as pd
import os
from puralang.core import run_pure_script
from google import genai
from google.genai import types

# Set up clean web browser tab configurations
st.set_page_config(page_title="PuraLang AI Engine", page_icon="✨", layout="centered")

st.title("✨ PuraLang AI Data Engine")
st.caption("Transform and clean messy CSV datasets using simple, plain English instructions.")

# User inputs their API key securely in the UI sidebar
with st.sidebar:
    st.header("🔑 Authentication")
    api_key = st.text_input("Enter Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    st.markdown("---")
    st.markdown("### 💡 Supported Operations:")
    st.markdown("- `drop duplicate user_id values`")
    st.markdown("- `fill null age spaces with value 24`")
    st.markdown("- `format email to lowercase`")
    st.markdown("- `filter rows where age > 25`")
    st.markdown("- `rename column email to contact_email`")

# Main file upload interface component
uploaded_file = st.file_uploader("Upload your messy CSV file", type=["csv"])

if uploaded_file:
    # Save file temporarily to disk so our compiler engine can read it locally
    temp_filename = uploaded_file.name
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    df_preview = pd.read_csv(temp_filename)
    st.subheader("📊 Original Data Preview")
    st.dataframe(df_preview.head())
    
    # Input text box for plain English queries
    user_query = st.text_input(
        "What cleaning operations should we run?", 
        placeholder="e.g., filter rows where age is greater than 25 and format email to lowercase"
    )
    
    if st.button("🔥 Run Clean Engine Pipeline"):
        if not api_key:
            st.error("Please provide a valid Gemini API Key in the sidebar to proceed.")
        elif not user_query:
            st.warning("Please type a cleaning instruction query first.")
        else:
            # Set environment variable temporarily for core module tracking
            os.environ["GEMINI_API_KEY"] = api_key
            
            with st.spinner("🤖 Consulting PuraLang AI Agent & parsing rules..."):
                try:
                    # Initialize the client inside app context to retrieve translated script structure
                    client = genai.Client(api_key=api_key)
                    system_instruction = """
                    You are the natural language translation engine for PuraLang, a data-cleaning DSL.
                    Your sole job is to translate a user's plain English cleaning request into a valid PuraLang script.
                    
                    VALID KEYWORDS AND SYNTAX:
                    LOAD "filename.csv"
                      |> DROP_DUPLICATES "column_name"
                      |> FILL_NULLS "column_name" VALUE 20
                      |> FORMAT_STRINGS "column_name" TO LOWERCASE
                      |> FILTER_ROWS "column_name" > 50
                      |> RENAME_COLUMN "old_name" TO "new_name"
                      |> EXPORT_CSV "output.csv"
                      
                    CRITICAL INSTRUCTIONS:
                    - Respond ONLY with the raw PuraLang code script. 
                    - Do NOT include markdown code blocks like ```text or ```puralang.
                    - Do NOT write any conversational filler text.
                    """
                    
                    # Force the AI to target the specific file the user uploaded
                    refined_prompt = f"Load '{temp_filename}' then perform: {user_query}. Make sure to export the result to 'cleaned_output.csv'."
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=refined_prompt,
                        config=types.GenerateContentConfig(system_instruction=system_instruction, temperature=0.1)
                    )
                    
                    generated_code = response.text.strip()
                    
                    st.info("💻 **AI Generated PuraLang Compilation Script:**")
                    st.code(generated_code)
                    
                    # Execute generated code using our native compilation pipeline rules
                    run_pure_script(generated_code)
                    
                    # Render the cleaned file preview and download buttons if successful
                    if os.path.exists("cleaned_output.csv"):
                        cleaned_df = pd.read_csv("cleaned_output.csv")
                        st.subheader("✅ Cleaned Data Output Preview")
                        st.dataframe(cleaned_df)
                        
                        # Provide a web download link for the newly structured matrix
                        with open("cleaned_output.csv", "rb") as file:
                            st.download_button(
                                label="📥 Download Cleaned CSV File",
                                data=file,
                                file_name="puralang_cleaned_data.csv",
                                mime="text/csv"
                            )
                    else:
                        st.error("Engine pipeline finished, but output file was not found.")
                except Exception as e:
                    st.error(f"Pipeline Failure: {e}")