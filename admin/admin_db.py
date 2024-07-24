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


def main():
    
    # 初始化狀態
    if 'data_updated' not in st.session_state:
        st.session_state.data_updated = False
    
    
    #st.markdown("### 資料表處理")    

    # 顯示數據表
    st.subheader("資料表內容")
    
    with st.form("my_form"):    
        data = fetch_data()
        edited_data = st.data_editor(data, num_rows="dynamic", use_container_width=True)
        submitted = st.form_submit_button("保存修改")  


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
        
        #st.success("資料已更新")
        # 重新加載頁面以顯示最新的數據
        # 更新狀態並重新加載頁面
        st.session_state.data_updated = True        
        st.rerun()
        
    # 顯示更新訊息
    if st.session_state.data_updated:
        st.success("資料已更新10")
        st.session_state.data_updated = False


main()
