import streamlit as st
import pandas as pd
import sqlite3

# SQLite 連接設置
def get_connection():
    return sqlite3.connect('TESTDB0724')

# 獲取數據
def fetch_data():
    conn = get_connection()
    query = "SELECT * FROM USERS"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 新增記錄
def insert_record(id, name, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO USERS (ID, NAME, PASSWORD) VALUES (?, ?, ?)", (id, name, password))
    conn.commit()
    conn.close()

# 修改記錄
def update_record(id, name, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE USERS SET NAME=?, PASSWORD=? WHERE ID=?", (name, password, id))
    conn.commit()
    conn.close()

# 刪除記錄
def delete_record(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM USERS WHERE ID=?", (id,))
    conn.commit()
    conn.close()

def main():
    #st.markdown("### 資料表處理")    

    # 顯示數據表
    st.subheader("資料表內容")
    
    with st.form("my_form"):    
        data = fetch_data()
        edited_data = st.data_editor(data, num_rows="dynamic", use_container_width=True)
        #submitted = st.form_submit_button("保存修改") 
        submitted = st.button("保存修改")  


    # 保存編輯後的數據
    if submitted:
        conn = get_connection()
        cursor = conn.cursor()
        # 刪除所有現有記錄
        cursor.execute("DELETE FROM USERS")
        conn.commit()

        # 插入編輯後的數據
        for _, row in edited_data.iterrows():
            cursor.execute("INSERT INTO USERS (ID, NAME, PASSWORD) VALUES (?, ?, ?)", (row['ID'], row['NAME'], row['PASSWORD']))
        
        conn.commit()
        conn.close()
        st.success("資料已更新")



main()
