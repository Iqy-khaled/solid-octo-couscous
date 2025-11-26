import streamlit as st
import pandas as pd
import database as db
import sqlite3


st.title('FURNITURE DATABASE SYSTEM')


st.write('Note: select the condition for the data that you need.')
# --- Filters ---
level = st.selectbox("1️⃣ Select level:", ["FORM1", "FORM2", "FORM3", "FORM4", "FORM5", "FORM6"])

conn = sqlite3.connect("C:\\Users\sj013496\\Desktop\\furniture\\furniture.db")
cursor = conn.cursor()

def delete_row(level, user_name):
    """
    Delete a row from a table by user_id.
    """
    cursor.execute(f"DELETE FROM {level} WHERE user_name = ?", (user_name,))
    conn.commit()

try:
# --- Access Button ---
 if st.button("Access"):
   
  query = f"SELECT * FROM {level}"
  cursor.execute(query)   # no parameters needed
  rows = cursor.fetchall()

  if rows:
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    st.dataframe(df)
  else:
    st.warning(f"No data found in {level}.")
 
except:
  st.warning("There is no data for this level yet")

try:
 def fetch_data(table):
    return pd.read_sql(f"SELECT * FROM {level}", conn)

 st.markdown('---------------------------------DELETING OPTIONS:---------------------------------------------------')
 # = st.selectbox("1️⃣Select Table you want to delete:", ["FORM1", "FORM2", "FORM3", "FORM4", "FORM5", "FORM6", "STAFF"])

 if level:
    df = fetch_data(level)
    #st.dataframe(df)

    
    user_name = st.selectbox("1️⃣Select User_name to delete:", df["user_name"].unique())

    if st.button("Delete Selected"):
        delete_row(level, user_name)
        st.success(f"✅ User Name {user_name} deleted.")
except:
  st.warning('unknown table')
