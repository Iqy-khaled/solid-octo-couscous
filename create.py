import streamlit as st
import pandas as pd
import sqlite3


st.title('FURNITURE DATABASE SYSTEM')
rcolumn, ccolumn, lcolumn = st.columns(3)


st.image('C:\\Users\\sj013496\\Desktop\\furniture\\sjlogo.png',width=250)
st.session_state.cdata = pd.DataFrame({
            "user_name":pd.Series(dtype="str"),
            "user_sj": pd.Series(dtype="str"),
            "desk_no": pd.Series(dtype="str"),
            "chair_no": pd.Series(dtype="str"),
            "locker_no": pd.Series(dtype="str")
            
        })
if "save" not in st.session_state:
    st.session_state.save = False



    # Initialize session_state.cdata only once
    if "cdata" not in st.session_state:
        st.session_state.cdata = pd.DataFrame({

            "user_name":pd.Series(dtype="str"),
            "user_sj": pd.Series(dtype="str"),
            "desk_no": pd.Series(dtype="str"),
            "chair_no": pd.Series(dtype="str"),
            "locker_no": pd.Series(dtype="str")
            
            

        })

# Always show the data editor if cdata exists
if "cdata" in st.session_state:
    st.session_state.cdata = st.data_editor(
        st.session_state.cdata,
        num_rows="dynamic",
        key="cdata_editor_unique"  # Keep a fixed key to preserve edits
    )

    levels=st.selectbox('select Level:',[
           'FORM1',
           'FORM2',
           'FORM3',
           'FORM4',
           'FORM5',
           'FORM6', 
            ])
    
  
# --- DATABASE SETUP ---
def init_db(levels):
    conn = sqlite3.connect("C:\\Users\sj013496\\Desktop\\furniture\\furniture.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {levels} (
            user_name TEXT,
            user_sj TEXT PRIMARY KEY,
            desk_no TEXT,
            chair_no TEXT,
            locker_no TEXT
            
        )
    ''')
    conn.commit()
    return conn, cursor

# --- SAVE TO DATABASE ---
def save_to_db(df,levels):
    if df.empty:
        st.warning("No data to save")
        return

    conn, cursor = init_db(levels)
    for _, row in df.iterrows():
        cursor.execute(f"""
            INSERT OR REPLACE INTO {levels} (user_name,user_sj,desk_no,chair_no,locker_no)
            VALUES (?,?,?,?,?)
        """, (row['user_name'], row['user_sj'], row['desk_no'], row['chair_no'], row['locker_no']))
    conn.commit()
    conn.close()
    st.success(f"{len(df)} rows saved successfully to {levels}!")
    st.session_state.cdata = st.session_state.cdata.iloc[0:0]  # Clear table

# --- BUTTON TO SAVE ---
if st.button("Save"):
    if levels:
        df = st.session_state.cdata.dropna(how="all")   
        df = df[df.apply(lambda row: row.astype(str).str.strip().ne("").any(), axis=1)]  

        if df.empty:
            st.warning("⚠ No valid data to save. Please fill in the form before saving.")
        else:
            save_to_db(df, levels.replace(" ", "_"))  
            st.success("✅ Data saved successfully!")
    else:
        st.error("Please select a level (table) first.")

   
 
   