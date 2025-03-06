import streamlit as st
import pandas as pd
import psycopg2

# Kết nối đến PostgreSQL
def create_connection():
    return psycopg2.connect(
        host="localhost",
        database="token",
        user="HTP",
        password="htp1782k1"
    )

# Hàm truy vấn dữ liệu từ database
def fetch_data(query, params=None):
    conn = create_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                colnames = [desc[0] for desc in cur.description]
                data = cur.fetchall()
                return pd.DataFrame(data, columns=colnames)
    except Exception as e:
        st.error(f"Lỗi khi truy vấn dữ liệu: {e}")
        return pd.DataFrame()

# Hiển thị thông tin token
def show_token_info(selected_token):
    query_info = """
        SELECT dti.description, dti.website, dti.technical_doc, 
               dti.twitter, dti.reddit, dti.logo
        FROM dim_token d
        JOIN dim_token_info dti ON d.id = dti.token_id
        WHERE d.token = %s
    """
    info = fetch_data(query_info, (selected_token,))
    
    if not info.empty:
        st.subheader(f"Thông tin về token: {selected_token}")
        st.markdown(f"**Mô tả:** {info['description'].iloc[0]}")
        
        # Chia layout thành 2 cột
        col1, col2 = st.columns([1, 2])  # Cột 1 chiếm 1 phần, cột 2 chiếm 2 phần
        
        with col1:
            # Hiển thị logo
            st.image(info['logo'].iloc[0], width=150, caption=f"Logo {selected_token}")
        
        with col2:
            # Hiển thị thông tin URL
            st.markdown(f"**Website:** {info['website'].iloc[0]}")
            st.markdown(f"**Document:** {info['technical_doc'].iloc[0]}")
            st.markdown(f"**Twitter:** {info['twitter'].iloc[0]}")
            st.markdown(f"**Reddit:** {info['reddit'].iloc[0]}")
    else:
        st.warning(f"Không tìm thấy thông tin cho token {selected_token}.")

# Giao diện chính
def info_page():
    st.title("Thông tin Token")
    
    # Lấy danh sách token từ database và sắp xếp theo thứ tự chữ cái
    query_tokens = "SELECT token FROM dim_token ORDER BY token ASC"
    tokens = fetch_data(query_tokens)
    
    if not tokens.empty:
        token_list = tokens["token"].tolist()
        selected_token = st.selectbox("Chọn token", token_list)
        
        if selected_token:
            show_token_info(selected_token)
    else:
        st.error("Không có dữ liệu token nào trong database.")

# Chạy ứng dụng
if __name__ == "__main__":
    info_page()
