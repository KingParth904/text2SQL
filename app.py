# import streamlit as st
# import os
# import sqlite3
# import google.generativeai as genai
# from streamlit_option_menu import option_menu
# from PIL import Image

# # Configure the Google Generative AI model
# genai.configure(api_key="AIzaSyA5ge4WCnSwZ_9f7NgF4R1nOUYOBFo4c1U")

# # Function to load Google Gemini model and provide query
# def get_geminiresponse(question, prompt):
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content([prompt[0], question])
#     return response.text

# # Function to retrieve query from SQL
# def read_sql(sql, db):
#     conn = sqlite3.connect(db)
#     cur = conn.cursor()
#     cur.execute(sql)
#     rows = cur.fetchall()
#     conn.commit()
#     conn.close()
#     return rows

# # Prompt for Google Gemini
# prompt = [
#     """
#     You are an expert in converting English questions to SQL query!
#     The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
#     SECTION, and MARKS.
#     \n\n For example,\n Example 1 - How many entries of records are present?, 
#     the SQL command will be something like this: SELECT COUNT(*) FROM STUDENT;
#     \nExample 2 - Tell me all the students studying in the Data Science class?, 
#     the SQL command will be something like this: SELECT * FROM STUDENT 
#     WHERE CLASS="Data Science";
#     """
# ]

# # Streamlit App

# st.set_page_config(page_title="Gemini SQL Data Retriever", page_icon="📊", layout="wide")
# st.title("🔍 Gemini SQL Data Retriever")
# st.markdown("""
#     <style>
#         .main {
#             background-color: #f0f2f6;
#             padding: 20px;
#             border-radius: 10px;
#         }
#         .stButton > button {
#             background-color: #4CAF50;
#             color: white;
#             border-radius: 8px;
#             font-size: 16px;
#             padding: 10px 24px;
#         }
#     </style>
#     """, unsafe_allow_html=True)

# # Sidebar Menu
# with st.sidebar:
#     selected = option_menu(
#         "Menu",
#         ["Home", "SQL Query Generator", "About"],
#         icons=["house", "code-slash", "info-circle"],
#         menu_icon="cast",
#         default_index=0,
#     )

# if selected == "Home":
#     st.header("Welcome to the Gemini SQL Data Retriever App! 🎉")
#     st.write("""
#         This app allows you to ask questions in plain English, and it will generate and execute the corresponding SQL query for you.
#         Simply enter your question in the input box, and hit the button to get the SQL results!
#     """)

# elif selected == "SQL Query Generator":
#     question = st.text_input("Enter your question:", placeholder="e.g., How many students are in the Data Science class?", key="input")

#     submit = st.button("Retrieve Data")

#     if submit:
#         with st.spinner("Processing your request..."):
#             response = get_geminiresponse(question, prompt)
#             sql_results = read_sql(response, "student.db")
        
#         st.subheader("Query Results:")
#         if sql_results:
#             st.table(sql_results)
#         else:
#             st.write("No results found.")

# elif selected == "About":
#     st.header("About This App")
#     st.write("""
#         The Gemini SQL Data Retriever app leverages Google’s Gemini AI to convert natural language questions into SQL queries.
#         It can be particularly useful for individuals who are not familiar with SQL but need to interact with databases.
#     """)
#     image = Image.open("download.jpg")  # Replace with your image path
#     st.image(image, caption="Your Image Caption", use_column_width=True)
import streamlit as st
import sqlite3
import google.generativeai as genai

# Configure the Google Generative AI model
genai.configure(api_key="AIzaSyA5ge4WCnSwZ_9f7NgF4R1nOUYOBFo4c1U")

# Function to load Google Gemini model and provide query
def get_geminiresponse(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query from SQL with error handling
def read_sql(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # Print the generated SQL query for debugging
    st.text(f"Generated SQL Query: {sql}")
    
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    except sqlite3.OperationalError as e:
        st.error(f"An error occurred: {e}")
        st.error(f"The problematic SQL query was: {sql}")
        return []
    finally:
        conn.commit()
        conn.close()
    
    return rows

# Prompt for Google Gemini
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has two tables: PURCHASE_BEHAVIOUR and TRANSACTION_DATA.
    The PURCHASE_BEHAVIOUR table has columns: `LIFESTAGE`, `PREMIUM_CUSTOMER`, `PURCHASE_BEHAVIOUR`.
    The TRANSACTION_DATA table has columns: `DATE`, `STORE`, `CUSTOMER_ID`, `AMOUNT`, `PRODUCT_ID`.
    Please generate appropriate SQL queries based on the questions provided.
    Avoid using asterisks (*) for selecting columns. Always specify the column names explicitly.
    """
]

# Streamlit App
st.set_page_config(page_title="Gemini SQL Data Retriever", page_icon="📊", layout="wide")
st.title("🔍 Gemini SQL Data Retriever")

# Sidebar Menu
question = st.text_input("Enter your question:", placeholder="e.g., What is the average transaction amount?", key="input")

submit = st.button("Retrieve Data")

if submit:
    with st.spinner("Processing your request..."):
        response = get_geminiresponse(question, prompt)
        
        if not response.strip().lower().startswith("select"):
            st.error("The generated response doesn't look like a valid SQL query. Please try again.")
            st.error(f"Generated Response: {response}")
        else:
            sql_results = read_sql(response, "company.db")
        
            st.subheader("Query Results:")
            if sql_results:
                st.table(sql_results)
            else:
                st.write("No results found.")
