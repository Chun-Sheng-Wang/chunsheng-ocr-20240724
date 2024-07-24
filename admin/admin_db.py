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
    data = fetch_data()
    edited_data = st.data_editor(data)

    # 保存編輯後的數據
    if st.button("保存修改"):
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

    # 選擇操作
    st.sidebar.title("操作")
    operation = st.sidebar.selectbox("選擇操作", ["新增記錄", "刪除記錄"])

    # 表單輸入
    if operation == "新增記錄":
        st.sidebar.subheader("新增記錄")
        new_id = st.sidebar.text_input("ID")
        new_name = st.sidebar.text_input("Name")
        new_password = st.sidebar.text_input("Password")
        if st.sidebar.button("提交"):
            insert_record(new_id, new_name, new_password)
            st.success("新增記錄成功")

    elif operation == "刪除記錄":
        st.sidebar.subheader("刪除記錄")
        delete_id = st.sidebar.text_input("ID (刪除目標)")
        if st.sidebar.button("提交"):
            delete_record(delete_id)
            st.success("刪除記錄成功")

    # 重新加載數據以顯示更新
    st.subheader("更新後的資料表內容")
    data = fetch_data()
    st.data_editor(data)

main()
