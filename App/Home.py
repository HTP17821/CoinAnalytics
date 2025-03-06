import streamlit as st

# Cấu hình giao diện
st.set_page_config(page_title="Website NFT Token Tracker", page_icon="💰", layout="wide")

# Hàm tạo hiệu ứng rainbow cho tiêu đề
def rainbow_text(text):
    return "".join([f'<span style="color: hsl({i * 360 / len(text)}, 100%, 50%)">{char}</span>' for i, char in enumerate(text)])

def home_page():
    # Tiêu đề trang với hiệu ứng rainbow
    title_text = "Hello there! 👋"
    rainbow_title = rainbow_text(title_text)
    st.markdown(f"<h1 style='text-align:center;'>{rainbow_title}</h1>", unsafe_allow_html=True)

    # Giới thiệu ngắn gọn
    st.markdown("""
    Đây là website bạn có thể xem giá của các loại token game NFT phổ biến nhất hiện nay, 
    được cập nhật mỗi ngày từ sàn giao dịch lớn nhất là Binance. Bên cạnh đó, bạn cũng sẽ tìm thấy 
    thông tin về đội ngũ phát triển, kênh chính thức và mạng xã hội của các tựa game NFT này. Ngoài ra, website còn 
    cung cấp các lịch sử dữ liệu giao dịch để bạn có thể phân tích chi tiết và có thể tham khảo để đưa ra quyết định đầu tư thông minh.
    """)

    st.markdown("## Các tính năng chính:")
    st.markdown("""
    - **Theo dõi giá token**: Cập nhật liên tục mỗi ngày giá của 8 token game NFT.
    - **Phân tích chi tiết**: Thống kê và phân tích lịch sử giá token theo các thông số chuyên sâu.
    - **Hướng dẫn và thông tin game**: Cung cấp thông tin chi tiết về các game NFT nổi bật và phổ biến.
    """)

    st.markdown("## Quy trình ETL:")
    st.markdown("""
    - **Extract (Crawl Data)**: Lấy lịch sử giá của 8 token từ khi chúng được niêm yết trên sàn Binance cho đến hiện tại 
                và lấy thông tin về đội ngũ phát triển token từ sàn CoinMarketCap bằng apikey và secretkey.  
    - ** Transform (Xử lý & làm sạch dữ liệu)**: Chuẩn hóa timestamp, Chuyển đổi định dạng cột số, Xử lý các giá trị 'null', 
                xử lý data bị thiếu bằng cách thay thế giá trị thiếu bằng giá trị trung bình của cột đó, ....
    - ** Load (Lưu vào Database & MinIO)**: Data thô thì lưu vào datalake(MinIO) và phân data thành 3 bảng chính
                dim_token - Thông tin cơ bản về token.
                dim_token_info - Thông tin chi tiết (team, social links).  
                fact_token_prices - Giá token theo thời gian. 
    """)


    # Chèn một ảnh minh họa
    st.image(r"D:\HTP\Project-personal\CoinAnalytics\Main\App\workflow.png", use_container_width=True)



    # Giao diện đẹp, dùng bảng màu nhẹ nhàng
    st.markdown("## Cảm ơn bạn đã xem qua!")
    st.markdown("Đây là một project nhỏ mình làm ra nhằm mục đích thực hành và học hỏi thêm nên là còn nhiều thiếu sót. Nếu các bạn có thắc mắc hay đóng góp ý tưởng gì để giúp project của mình hoàn thiện hơn nữa, thì liên hệ với mình qua thông tin bên dưới nha ^^  ")

    # Footer
    st.markdown(""" 
    ---
    ### Contact me:
    Email: [Tanphatcoder@Gmail.com](mailto:tanphatcoder@Gmail.com).  
    Github: [https://github.com/HTP17821](https://github.com/HTP17821)  
    Linkedin: [https://www.linkedin.com/in/htp201/](https://www.linkedin.com/in/htp201/)
    """)


#############################################################################################################

# Giao diện Sidebar
def sidebar():
    st.sidebar.title("Hướng dẫn: ")
    st.sidebar.markdown("""
    Chọn các mục sau để xem thông tin chi tiết:
    - **Price**: Theo dõi giá token.
    - **Analysis**: Phân tích chuyên sâu.
    - **Info**: Thông tin về nhà phát triển Token.               
    """)

if __name__ == "__main__":
    sidebar()  # Hiển thị sidebar
    home_page()  # Hiển thị nội dung của trang chủ
