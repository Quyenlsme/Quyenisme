# import re
# import json

# def flatten_content(data):
#     # Trích xuất page_content và metadata
#     page_content = data.get("page_content", "")
#     metadata = data.get("metadata", {})

#     # Làm phẳng nội dung
#     flat_content = re.sub(r'\n+', '\n', page_content).strip()  # Loại bỏ dòng trống
#     flat_content = re.sub(r'\s+', ' ', flat_content)  # Thay thế nhiều khoảng trắng bằng một khoảng trắng

#     # Lấy thông tin tiêu đề và nguồn từ metadata
#     title = metadata.get("title", "No Title")
#     source = metadata.get("source", "No Source")

#     # Kết hợp chỉ giữ lại content, source
#     result = f"Content:{flat_content}|Source:{source}"
#     return result

# def word_segmentation(text):
#     from underthesea import word_tokenize
#     return word_tokenize(text, format="text")

# # processed_data = []
# # with open('data/data_web.json', 'r', encoding='utf-8') as file:
# #     data = json.load(file)
# #     for item in data:
# #         processed_data.append(word_segmentation(flatten_content(item)))
# processed_data = []
# with open('data/a.txt', 'r', encoding='utf-8') as file:
#     data = 

# # Lưu vào file
# with open('data/processed_data.json', 'w', encoding='utf-8') as file:
#     json.dump(processed_data, file, ensure_ascii=False, indent=4)

import json
from underthesea import word_tokenize

def word_segmentation(text):
    """
    Perform word segmentation on the input text using underthesea's word_tokenize.

    Args:
        text (str): The input text to be segmented.

    Returns:
        str: The segmented text in string format.
    """
    return word_tokenize(text, format="text")

def process_file(input_path, output_path):
    """
    Read the input file, perform word segmentation on each line, and save the processed data to a JSON file.

    Args:
        input_path (str): Path to the input text file.
        output_path (str): Path where the processed JSON data will be saved.
    """
    processed_data = []

    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            for idx, line in enumerate(file, 1):
                stripped_line = line.strip()
                
                if not stripped_line:
                    # Skip empty lines
                    continue
                
                segmented_line = word_segmentation(stripped_line)
                
                # Optionally, store additional information like line numbers
                processed_data.append({
                    "line_number": idx,
                    "original_text": stripped_line,
                    "segmented_text": segmented_line
                })
                
                # Debug: Print progress every 1000 lines
                if idx % 1000 == 0:
                    print(f"Processed {idx} lines...")
                    
    except FileNotFoundError:
        print(f"Error: The file {input_path} does not exist.")
        return
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")
        return

    # Save the processed data to a JSON file
    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            json.dump(processed_data, outfile, ensure_ascii=False, indent=4)
        print(f"Processed data has been saved to {output_path}")
    except Exception as e:
        print(f"An error occurred while saving the processed data: {e}")

if __name__ == "__main__":
    input_file_path = 'data/a.txt'
    output_file_path = 'data/processed_data.json'
    process_file(input_file_path, output_file_path)
