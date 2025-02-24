import streamlit as st
import psycopg2
import pandas as pd
from datetime import datetime, timedelta

# Kết nối đến PostgreSQL
def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="token",
        user="HTP",
        password="htp1782k1"
    )

# Lấy danh sách token
def get_tokens():
    with connect_db() as conn:
        return pd.read_sql("SELECT token FROM dim_token ORDER BY token", conn)['token'].tolist()

# Lấy dữ liệu giá token
def get_price_data(token, limit):
    query = f"""
    SELECT timestamp, open, high, low, close, volume, 
           price_difference, price_percentage_change, mid_price, vwap
    FROM fact_token_prices
    JOIN dim_token ON fact_token_prices.token_id = dim_token.id
    WHERE dim_token.token = %s
    ORDER BY timestamp DESC
    LIMIT %s;
    """
    with connect_db() as conn:
        return pd.read_sql(query, conn, params=(token, limit))

# Lọc dữ liệu theo khoảng thời gian
def filter_data(df, option, start_date=None, end_date=None):
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    date_map = {
        'Hôm qua': (today - timedelta(days=1), today),
        '1 tuần': (today - timedelta(days=7), today),
        '1 tháng': (today - timedelta(days=30), today),
        '3 tháng': (today - timedelta(days=90), today),
    }
    
    if option == 'Chọn ngày: ' and start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        # Kiểm tra ngày kết thúc không được vượt quá ngày hôm nay
        if end_date > today:
            raise ValueError("Ngày kết thúc không thể vượt quá ngày hôm nay.")
        
        # Kiểm tra ngày kết thúc không được trước ngày bắt đầu
        if end_date < start_date:
            raise ValueError("Ngày kết thúc không thể trước ngày bắt đầu.")
        
        df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
    elif option in date_map:
        start_date, end_date = date_map[option]
        df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
    
    return df

# Trang phân tích
def analysis_page():
    st.title("Phân tích chuyên sâu")

    st.markdown("""
    ### Chú thích:
    - **timestamp**: Thời gian ghi nhận dữ liệu. Được lấy từ thời điểm giao dịch.
    - **open**: Giá mở cửa. Là giá tại thời điểm bắt đầu phiên giao dịch.
    - **high**: Giá cao nhất trong phiên giao dịch.
    - **low**: Giá thấp nhất trong phiên giao dịch.
    - **close**: Giá đóng cửa. Là giá tại thời điểm kết thúc phiên giao dịch.
    - **volume**: Khối lượng giao dịch trong phiên.
    - **price_difference**: Chênh lệch giá giữa giá mở cửa và giá đóng cửa.  `close - open`
    - **price_percentage_change**: Tỷ lệ thay đổi giá giữa giá mở cửa và giá đóng cửa (%). `((close - open) / open) * 100`
    - **mid_price**: Giá trung bình trong phiên giao dịch. `(high + low) / 2`
    - **vwap**: Giá trị giao dịch trung bình theo khối lượng. `(Σ(price * volume)) / Σ(volume)`  
    """)

    # Lựa chọn token
    tokens = get_tokens()
    selected_token = st.selectbox("Chọn Token:", tokens)

    # Hiển thị dữ liệu mẫu
    st.markdown(f"<h3 style='text-align:center; color:#999594;'>{selected_token}</h3>", unsafe_allow_html=True)
    st.table(get_price_data(selected_token, limit=1))

    # Lọc dữ liệu theo thời gian
    filter_option = st.selectbox("Chọn khoảng thời gian muốn xem:", 
                                 ['Hôm qua', '1 tuần', '1 tháng', '3 tháng', 'Chọn ngày: '])

    if filter_option == 'Chọn ngày: ':
        start_date = st.date_input("Chọn ngày bắt đầu:")
        end_date = st.date_input("Chọn ngày kết thúc:")
        custom_start_date = start_date.strftime('%Y-%m-%d')
        custom_end_date = end_date.strftime('%Y-%m-%d')
    else:
        custom_start_date = custom_end_date = None

    try:
        # Lấy và lọc dữ liệu
        all_data = get_price_data(selected_token, limit=1000)
        filtered_data = filter_data(all_data, filter_option, custom_start_date, custom_end_date)

        if filtered_data.empty:
            st.warning("Không có dữ liệu cho khoảng thời gian này.")
        else:
            # Đếm số ngày
            if custom_start_date and custom_end_date:
                start_date = pd.to_datetime(custom_start_date)
                end_date = pd.to_datetime(custom_end_date)
                num_days = (end_date - start_date).days + 1  # +1 để bao gồm cả ngày bắt đầu
                st.subheader(f"Dữ liệu sau khi lọc (Chọn ngày: {num_days} ngày):")
            else:
                st.subheader(f"Dữ liệu từ ({filter_option}):")
            
            

            # Thêm nút tải xuống CSV
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="Tải xuống CSV",
                data=csv,
                file_name=f"{selected_token}_filtered_data.csv",
                mime="text/csv",
            )


            #In table
            st.table(filtered_data)




    except ValueError as e:
        st.error(str(e))

if __name__ == "__main__":
    analysis_page()


