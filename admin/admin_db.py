import streamlit as st
import pandas as pd
import sqlite3
#import os

import shutil
import datetime



def backup_db():
    # 資料庫檔案位置
    source_file = 'TESTDB0724.sqlite3'

    # 設定備份檔案名稱
    backup_file = f'TESTDB0724_backup_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.sqlite3'

    # 執行備份
    shutil.copy2(source_file, backup_file)




# SQLite 連接設置
def get_connection():
    
    # 創建資料檔並進行初始化
    conn = sqlite3.connect('TESTDB0724.sqlite3')
    cursor = conn.cursor()
    # 執行初始化 SQL 指令
    cursor.execute('CREATE TABLE IF NOT EXISTS USERS (ID TEXT (30),NAME TEXT (50),PASSWORD TEXT (50),PRIMARY KEY (ID))')
    conn.commit()
    
    #conn.close()    
    
    return conn

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
        edited_data = st.data_editor(data, key='DB_USERS', num_rows="dynamic", use_container_width=True)
        submitted = st.form_submit_button("保存修改")  


    # 保存編輯後的數據
    if submitted:
        
        editor_key=st.session_state["DB_USERS"]
        
        st.write(editor_key)
        
        return True
        
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
        
        backup_db()
        
        #st.success("資料已更新")
        # 重新加載頁面以顯示最新的數據
        # 更新狀態並重新加載頁面
        st.session_state.data_updated = True        
        st.rerun()
        
    # 顯示更新訊息
    if st.session_state.data_updated:
        st.success("資料已更新21")
        st.session_state.data_updated = False


main()
