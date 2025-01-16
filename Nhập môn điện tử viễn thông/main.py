from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import gradio as gr

from src.retriever import create_retriever
from src.load_llm import load_llm
from src.prepare_vector_db import load_db


def create_prompt(template):
    prompt = PromptTemplate(template=template, input_variables=["context","question"])
    return prompt


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

db = load_db('vector_db/')
llm = load_llm()

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

prompt = create_prompt(template)
chain = create_chain(llm, prompt, db)

def get_answer(question):
    return chain.invoke(question)["result"]

import gradio as gr


conversation_history = []

def get_answer(question):
    
    conversation_history.append(("Sinh viên", question))
    
    answer = chain.invoke(question)["result"]
    conversation_history.append(("Trợ lý", answer))
    
    chat_display = ""
    for speaker, text in conversation_history:
        chat_display += f"**{speaker}:** {text}\n\n"
    return chat_display
# Gradio interface
with gr.Blocks() as rag_interface:
    
    gr.Markdown("<h1>University FAQ Helper</h1><p>Ask a question, and I’ll retrieve relevant information to provide an answer!</p>")
    
    # Display chat history
    chat_output = gr.Textbox(label="Chat History", value="", lines=10, interactive=False)
    
    # Input for the user's question
    question_input = gr.Textbox(label="Nhập câu hỏi của bạn", placeholder="Type your question here...", lines=2)
    
    # Submit button to update the conversation
    submit_button = gr.Button("Submit")
    submit_button.click(fn=get_answer, inputs=question_input, outputs=chat_output)
    
    # Clear button to reset the conversation
    clear_button = gr.Button("Clear Chat")
    clear_button.click(fn=lambda: "", outputs=chat_output)
    
# Launch the interface
rag_interface.launch(inbrowser=True, share=False)
