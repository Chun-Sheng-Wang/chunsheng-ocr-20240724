import streamlit as st


# 預設的帳號和密碼
USERNAME = "user"
PASSWORD = "1234"









if "role" not in st.session_state:
    st.session_state.role = "Admin"

ROLES = [None, "Requester", "Responder", "Admin"]


def login():

    st.header("請輸入帳號密碼")
    
    #role = st.selectbox("Choose your role", ROLES)

    username = st.text_input("帳號")
    password = st.text_input("密碼", type="password")


    if st.button("登入"):
        if check(username, password):
            st.success("登入成功！")
            st.session_state.role = "Admin"
            st.rerun()
            
        else:
            st.error("帳號或密碼錯誤")
    
        #st.session_state.role = role
        #st.rerun()


def logout():
    st.session_state.role = None
    st.rerun()



# 建立登入檢查函數
def check(username, password):
    if username == USERNAME and password == PASSWORD:
        return True
    else:
        return False


role = st.session_state.role

logout_page = st.Page(logout, title="登出", icon=":material/logout:")
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")
request_1 = st.Page(
    "request/request_1.py",
    title="Request 1",
    icon=":material/help:",
    default=(role == "Requester"),
)
request_2 = st.Page(
    "request/request_2.py", title="Request 2", icon=":material/bug_report:"
)
respond_1 = st.Page(
    "respond/respond_1.py",
    title="Respond 1",
    icon=":material/healing:",
    default=(role == "Responder"),
)
respond_2 = st.Page(
    "respond/respond_2.py", title="Respond 2", icon=":material/handyman:"
)
admin_1 = st.Page(
    "admin/admin_1.py",
    title="圖檔OCR與識別",
    icon=":material/person_add:",
    default=(role == "Admin"),
)
admin_2 = st.Page("admin/admin_2.py", title="圖檔批次處理", icon=":material/security:")


admin_db = st.Page("admin/admin_db.py", title="資料表處理", icon=":material/handyman:")

#account_pages = [logout_page, settings]
account_pages = [logout_page]

request_pages = [request_1, request_2]
respond_pages = [respond_1, respond_2]
admin_pages = [admin_1, admin_2, admin_db]

st.title("標準檢驗局OCR專案")
#st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")

st.logo("images/logo6.jpg", icon_image="images/logo6.jpg")

page_dict = {}

#if st.session_state.role in ["Requester", "Admin"]:
#    page_dict["待處理資料"] = request_pages
#if st.session_state.role in ["Responder", "Admin"]:
#    page_dict["已處理結果"] = respond_pages

if st.session_state.role == "Admin":
    # page_dict["待處理資料"] = request_pages
    
    page_dict["處理資料"] = admin_pages
    #page_dict["已處理結果"] = respond_pages
    
    # pass

if len(page_dict) > 0:
    pg = st.navigation({"帳號": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()