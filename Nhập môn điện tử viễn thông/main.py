import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from src.retriever import create_retriever
from src.load_llm import load_llm
from src.prepare_vector_db import load_db

# Load the database and language model
db = load_db('vector_db/')
llm = load_llm()

# Create the prompt template
template = '''
<|im_start|>system
Bạn là trợ lý AI thông minh, chuyên hỗ trợ sinh viên Điện tử Viễn thông của Đại học Bách Khoa. Khi trả lời, hãy cung cấp thông tin chi tiết, chính xác và dễ hiểu, nhưng chỉ giới hạn trong những nội dung có liên quan đến ngành Điện tử viễn thông và môn học Nhập môn Điện tử viễn thông. Hãy giữ câu trả lời ngắn gọn, không đi sâu vào các nội dung ngoài phạm vi của ngành. Nếu câu hỏi nằm ngoài phạm vi thông tin của ngành, lịch sự từ chối trả lời.

Khi trả lời, vui lòng thực hiện các bước sau:
1. Trích xuất các chi tiết quan trọng từ thông tin tham khảo dưới đây nếu có.
2. Từ những chi tiết quan trọng đó đối chiếu với câu hỏi đưa ra bởi sinh viên.
3. Trả lời câu hỏi một cách chính xác, chỉ tập trung vào nội dung có liên quan đến ngành.
4. Dịch câu trả lời sang Tiếng Việt và đảm bảo rõ ràng, dễ hiểu cho sinh viên.

Thông tin tham khảo:
{context}
<|im_end|>
<|im_start|>user
Câu hỏi của sinh viên:
{question}
<|im_end|>
<|im_start|>assistant
Câu trả lời (liên quan đến ngành Điện tử viễn thông):
'''

prompt = PromptTemplate(template=template, input_variables=["context", "question"])

# Create the chain
def create_chain(llm, prompt, db):
    retriever = create_retriever(db)
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={'prompt': prompt}
    )
    return chain

chain = create_chain(llm, prompt, db)

# Define the bot logic
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Xin chào! Tôi là trợ lý AI hỗ trợ ngành Điện tử Viễn thông. Hãy đặt câu hỏi của bạn!")

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    try:
        response = chain.invoke(question)
        answer = response["result"]
    except Exception as e:
        answer = f"Đã xảy ra lỗi: {str(e)}"

    await update.message.reply_text(answer)

# Main function to run the bot
def main():
    API_TOKEN = "7849554526:AAEbJcX66KBITzXYAhdJT2D5_DBaAdbv6VE"  # Replace with your Telegram bot token

    app = ApplicationBuilder().token(API_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask_question))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()