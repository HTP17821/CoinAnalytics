import streamlit as st
import psycopg2
import pandas as pd

# Kết nối đến PostgreSQL
def create_connection():
    return psycopg2.connect(
        host="localhost",
        database="token",
        user="HTP",
        password="htp1782k1"  # Thay đổi với password của bạn
    )

# Lấy dữ liệu giá đóng cửa mới nhất và tên + logo của 8 token
def get_token_prices_and_info():
    conn = create_connection()
    query = """
    SELECT 
        dt.token, 
        dti.logo, 
        ftp.close, 
        ftp.timestamp
    FROM fact_token_prices ftp
    JOIN dim_token dt ON ftp.token_id = dt.id
    JOIN dim_token_info dti ON dt.id = dti.token_id
    WHERE ftp.timestamp = (
        SELECT MAX(timestamp) 
        FROM fact_token_prices 
        WHERE token_id = ftp.token_id
    )
    ORDER BY ftp.timestamp DESC
    LIMIT 8;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Hàm hiển thị thông tin một token
def display_token_info(col, token_data):
    with col:
        st.markdown('<div style="background-color:#999594; padding: 2px 20px;">', unsafe_allow_html=True)  
        st.subheader(f"Token: {token_data['token']}/USDT")
        st.image(token_data['logo'], width=80)
        st.write(f"**Price**: {token_data['close']} 💲")
        st.write(f"**Ngày**: {token_data['timestamp']}")
        st.markdown('</div>', unsafe_allow_html=True)

# Hiển thị giá đóng cửa và thông tin token
def show_token_prices():
    st.title("Giá Token update Mới Nhất")
    token_prices_df = get_token_prices_and_info()
    
    if token_prices_df.empty:
        st.warning("Không có dữ liệu giá.")
    else:
        # Chia bố cục thành các cột cho mỗi hàng (3 token cho hàng 1 và 2, 2 token cho hàng 3)
        cols1 = st.columns(3)
        for i, col in enumerate(cols1):
            display_token_info(col, token_prices_df.iloc[i])

        cols2 = st.columns(3)
        for i, col in enumerate(cols2, start=3):
            display_token_info(col, token_prices_df.iloc[i])

        cols3 = st.columns(2)
        for i, col in enumerate(cols3, start=6):
            display_token_info(col, token_prices_df.iloc[i])

if __name__ == "__main__":
    show_token_prices()
