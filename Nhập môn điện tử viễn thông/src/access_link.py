import gdown
import os
import pdfplumber
from pdf2image import convert_from_path
import pytesseract

# Đường dẫn tệp link.txt
link_file_path = 'data/link.txt'

# Đọc các liên kết từ link.txt
with open(link_file_path, 'r', encoding='utf-8') as file:
    links = [line.strip() for line in file if line.strip()]  # Bỏ dòng trống

# Tạo thư mục lưu PDF và kết quả nếu chưa tồn tại
os.makedirs('data/pdf_files', exist_ok=True)
os.makedirs('data/text_results', exist_ok=True)

# Tệp tổng hợp văn bản
final_text_path = 'data/a.txt'

# Xóa nội dung cũ trong tệp tổng hợp
with open(final_text_path, 'w', encoding='utf-8') as a_file:
    a_file.write("")  # Xóa nội dung cũ

# Xử lý từng liên kết
for idx, url in enumerate(links, start=1):
    try:
        # Lấy ID tệp từ Google Drive (giả sử URL có định dạng chuẩn)
        file_id = url.split('/d/')[1].split('/')[0]
        download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
        
        # Đường dẫn để lưu PDF
        output_pdf_path = f'data/pdf_files/file_{idx}.pdf'
        
        # Tải tệp PDF từ Google Drive
        print(f"Tải PDF từ liên kết {idx}/{len(links)}: {url}")
        gdown.download(download_url, output_pdf_path, quiet=False, fuzzy=True)

        # Kiểm tra xem PDF đã tải về thành công chưa
        if os.path.exists(output_pdf_path):
            text_from_pdf = ""
            
            # Trích xuất văn bản từ PDF
            with pdfplumber.open(output_pdf_path) as pdf:
                for page in pdf.pages:
                    text_from_pdf += page.extract_text() or ""  # Thêm văn bản từng trang

            # Nếu không có văn bản trong PDF, sử dụng OCR
            if not text_from_pdf.strip():
                print(f"PDF {idx} không chứa văn bản, tiến hành OCR...")
                images = convert_from_path(output_pdf_path, dpi=300)  # Chuyển PDF sang ảnh
                for img in images:
                    text_from_pdf += pytesseract.image_to_string(img, config='--psm 6')

            # Ghi kết quả từng tệp vào tệp tổng hợp
            with open(final_text_path, 'a', encoding='utf-8') as a_file:
                a_file.write(f"\n--- Văn bản từ PDF {idx} ---\n")
                a_file.write(text_from_pdf)

            print(f"Văn bản từ PDF {idx} đã được ghi vào tệp tổng hợp.")
        else:
            print(f"Không thể tải tệp PDF {idx}.")
    except Exception as e:
        print(f"Lỗi khi xử lý PDF {idx}: {e}")

print(f"\nToàn bộ văn bản đã được ghi vào {final_text_path}.")
