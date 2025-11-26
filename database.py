import sqlite3

# Connect (or create) DB
conn = sqlite3.connect("furniture.db", check_same_thread=False)
cursor = conn.cursor()

# Create tables
def create_tables():
    for table in ["FORM1", "FORM2", "FORM3", "FORM4", "FORM5", "FORM6", "STAFF"]:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                user_name TEXT,
                user_id TEXT,
                user_status TEXT,
                level TEXT,
                stream TEXT,
                desk_sj TEXT,
                desk_status TEXT,
                chair_sj TEXT,
                chair_status TEXT,
                locker_No TEXT,
                locker_status TEXT,
                Cupboard_sj TEXT,
                Cupboard_status TEXT,
                Block TEXT,
                Room_No TEXT,
                Floor TEXT,
                Table_sj TEXT,
                Table_status TEXT,
                Year_issued TEXT,
                Gender TEXT,
                Date_Returned TEXT
            )
        """)
    conn.commit()

def save_dataframe(df, table_name):
    if df.empty:
        return 0  # nothing to save

    for _, row in df.iterrows():
        cursor.execute(f"""
            INSERT INTO {table_name} (
                user_name, user_id, user_status, level, stream, desk_sj, desk_status,
                chair_sj, chair_status, locker_No, locker_status, Cupboard_sj,
                Cupboard_status, Block, Room_No, Floor, Table_sj, Table_status,
                Year_issued, Gender, Date_Returned
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, tuple(row))
    conn.commit()
    return len(df)

