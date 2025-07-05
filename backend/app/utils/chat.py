from langchain_openai import ChatOpenAI
from app.schema.model_outputs import ClassificationOutput, MultipleFilesSelection, SingleFileSelection
from langchain_core.prompts import PromptTemplate

classification_model = ChatOpenAI(model="provider-3/gpt-4.1-nano").with_structured_output(ClassificationOutput)
classification_prompt = PromptTemplate.from_template("""
You are a classifier that analyzes software engineering user questions about a github code repository.
Classify each question into exactly one of these categories: GENERAL, FILE, FUNCTION&CLASS.
Return your response in the following JSON format:
{{ "label": "GENERAL" }}
Here are some examples:
---
Question: How do I install the dependencies for this repo?  
{{ "label": "GENERAL" }}
---
Question: What does the file utils.py do?  
{{ "label": "FILE" }}
---
Question: What is the purpose of the class ConfigLoader?  
{{ "label": "FUNCTION&CLASS" }}
---
Question: How can I contribute to this repository?  
{{ "label": "GENERAL" }}
---
Question: Is there a license file in this repo?  
{{ "label": "FILE" }}
---
Question: Can you explain how the authenticate_user function works?  
{{ "label": "FUNCTION&CLASS" }}
---
Question: Who maintains this project?  
{{ "label": "GENERAL" }}
---
Question: What is inside the README.md file?  
{{ "label": "FILE" }}
---
Question: What arguments does the process_data method take?  
{{ "label": "FUNCTION&CLASS" }}
---
Question: What are the main goals of this repository?  
{{ "label": "GENERAL" }}
---
Question: Describe the contents of config.yaml  
{{ "label": "FILE" }}
---
Question: What does the UserManager class handle?  
{{ "label": "FUNCTION&CLASS" }}
---
Now classify the following question:
Question: {user_question}
""")


relevant_multiple_files_prompt = PromptTemplate.from_template("""
You are an expert software engineering assistant helping analyze a github code repository.
A user has asked the following question:
{user_question}

Your job is to identify which specific files from the repository are relevant to answering this question.
Below is the list of all available files in the repository, along with their paths and name.

{file_symbol_table}

From this list, choose the files that are most relevant to answering the user's question.
Return ONLY a JSON object in this exact format:
{{ "files": ["<full_path_1>", "<full_path_2>", ...] }}

- Include full file paths (from the list above), not just filenames.
- Always return at least one file — even if your best guess is based on file names or language.
- Do NOT include any explanation or extra text. Just the JSON object.
""")
relevant_multiple_files_model = ChatOpenAI(model="provider-3/gpt-4.1-nano").with_structured_output(MultipleFilesSelection)



relevant_single_file_prompt = PromptTemplate.from_template("""
You are an expert software engineering assistant helping analyze a github code repository.
A user has asked the following question:
{user_question}

Below is a list of all available files in the repository:
{file_symbol_table}

The user has explicitly mentioned a filename in their question.
Your task is to:
- Identify exactly which file they are referring to from the list.
- If no such filename is present in the list, return: {{ "file_path": "-1" }}
- Return ONLY a JSON object in this exact format: {{ "file_path": "<full_path>" }}
- The full path must match only one of the paths listed above.
- Do not include any explanation or extra text.
""")
relevant_single_file_model = ChatOpenAI(model="provider-3/gpt-4.1-nano").with_structured_output(SingleFileSelection)

classification_chain = classification_prompt | classification_model

#res=chain.invoke({"user_question": "how to make changes to get_me"})
#print(res.label.value)







def format_file_symbol_table(symbol_table):
    output = ""
    for data in symbol_table:
        output+=f"- Path: {data['path']}   Filename: {data['filename']}\n"   
    return output




FILES_SYMBOL_TABLE = [
    {"path": "C:/repo/src/utils.py", "language": ".py", "filename": "utils.py"},
    {"path": "C:/repo/src/config.yaml", "language": ".yaml", "filename": "config.yaml"},
    {"path": "C:/repo/README.md", "language": ".md", "filename": "README.md"},
]

file_table_str = format_file_symbol_table(FILES_SYMBOL_TABLE)
chain = relevant_files_prompt | relevant_files_model
res = chain.invoke({
   "user_question": "what is this repo about and how do configure it?",
    "file_symbol_table": file_table_str
})


print(res.files)
def chat(CHAT_HISTORY,user_input):
    pass


