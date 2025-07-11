from langchain_openai import ChatOpenAI
from app.schema.model_outputs import ClassificationOutput, MultipleFilesSelection, SingleFileSelection
from langchain_core.prompts import PromptTemplate
from app.utils.ingest_repo import NONCODE_VECTOR_STORE_RETRIVER,CODE_VECTOR_STORE_RETRIEVER,validate_and_read_file
from langchain_core.runnables import RunnableLambda,RunnableBranch
from langchain_core.messages import HumanMessage, AIMessage


CHAT_MODEL = ChatOpenAI(model="provider-3/gpt-4.1-nano")
SYSTEM_PROMPT ="""
You are an expert AI assistant specialized in answering questions about a GitHub code repository.
Your tasks include:
- Answering questions related to files, code, functions, classes, documentation, or any technical details in the repository.
- Handling questions that are general or conceptual about the codebase, its purpose, design, or structure.
- Generating new code snippets, suggestions, or explanations if the user asks for help beyond the provided code (e.g. improvements, examples, refactoring).
- Using relevant context provided to you, which may include:
    - Code snippets
    - Non-code snippets
    - Complete file contents

Guidelines:
- Always use the provided context first to answer the user's question if it is relevant.
- If the user asks an open-ended question that goes beyond the context, feel free to answer using your own knowledge, but also try to incorporate the context if it's helpful.
- If the context provided does not contain sufficient information to answer the specific question, and the question is not open-ended, reply:
    > "The provided context is not sufficient to answer this question."
- Never fabricate details about specific code or files if the context does not mention them.
Be precise, technical, and helpful in your answers.
"""


classification_model = ChatOpenAI(model="provider-3/gpt-4.1-nano").with_structured_output(ClassificationOutput)
classification_prompt = PromptTemplate.from_template("""
You are a classifier that analyzes software engineering user questions about a github code repository.
Classify each question into exactly one of these categories: GENERAL, FILE, FUNCTION&CLASS, FOLLOWUP.
Return your response in the following JSON format:
{{ "label": "<CATEGORY_LABEL>" }}
Here are some examples:
---
Question: What arguments does the process_data method take?  
{{ "label": "FUNCTION&CLASS" }}
---
Question: Yes, please explain more about that.  
{{ "label": "FOLLOWUP" }}
---
Question: What does the UserManager class handle?  
{{ "label": "FUNCTION&CLASS" }}
---
Question: Could you summarize what you just said?  
{{ "label": "FOLLOWUP" }}
---
Question: How do I install the dependencies for this repo?  
{{ "label": "GENERAL" }}
---
Question: What is inside the README.md file?  
{{ "label": "FILE" }}
---
Question: Okay, and what about authentication?  
{{ "label": "FOLLOWUP" }}
---
Question: How can I contribute to this repository?  
{{ "label": "GENERAL" }}
---
Question: Describe the contents of config.yaml  
{{ "label": "FILE" }}
---
Question: What does the file utils.py do?  
{{ "label": "FILE" }}
---
Question: Thanks, that makes sense. I got that.  
{{ "label": "FOLLOWUP" }}
---
Question: What are the main goals of this repository?  
{{ "label": "GENERAL" }}
---
Question: Who maintains this project?  
{{ "label": "GENERAL" }}
---
Question: Can you explain how the authenticate_user function works?  
{{ "label": "FUNCTION&CLASS" }}
---
Question: Is there a license file in this repo?  
{{ "label": "FILE" }}
---
Question: What is the purpose of the class ConfigLoader?  
{{ "label": "FUNCTION&CLASS" }}
---
Now classify the following question:
Question: {query}
""")


relevant_multiple_files_prompt = PromptTemplate.from_template("""
You are an expert software engineering assistant helping analyze a GitHub code repository.
A user has asked the following question:
{query}

Your task is to decide which specific files from the repository are relevant to answering this question.
Below is the list of all available files in the repository, each assigned a unique index:

{file_symbol_table}

Instructions:
- If the user's question requires examining specific files to answer, return a list of the indices of those relevant files, using the numbers shown before each file above.
- If the user's question does NOT require referring to any specific files (e.g. it's a follow-up question, a general conversational reply, or does not depend on repository contents), return [-1].
- Return ONLY a JSON object in this exact format:
    {{ "file_indices": [1, 5, 8] }}    OR    {{ "file_indices": [-1] }}
- Do NOT include any explanation or extra text. Only the JSON object with numeric values.
""")
relevant_multiple_files_model = ChatOpenAI(model="provider-3/gpt-4.1-nano").with_structured_output(MultipleFilesSelection)



relevant_single_file_prompt = PromptTemplate.from_template("""
You are an expert software engineering assistant helping analyze a GitHub code repository.
A user has asked the following question:
{query}

Below is a numbered list of all available files in the repository:
{file_symbol_table}

The user has explicitly mentioned a filename in their question.
Your task is to:
- Identify exactly which single file they are referring to from the list above.
- If the filename mentioned in the question does NOT match any file in the list, return -1.
- Return ONLY a JSON object in this exact format:
{{ "file_index": 3 }}     OR    {{ "file_index": -1 }}
- Do NOT include any explanation or extra text. Only the JSON object with an integer value.
""")
relevant_single_file_model = ChatOpenAI(model="provider-3/gpt-4.1-nano").with_structured_output(SingleFileSelection)




final_prompt = PromptTemplate.from_template("""
USER QUESTION: {query}

---:RELEVANT CONTEXT:---
{context}

""")



def format_file_symbol_table(symbol_table):
    output = ""
    i=1
    for data in symbol_table:
        output+=f"{i}.  Path: {data['path']}   Filename: {data['filename']}\n"  
        i+=1 
    return output



def RAG(inputs):
    user_query = inputs["query"]
    output = "CODE RELATED CONTEXT:-----\n"
    code_results = CODE_VECTOR_STORE_RETRIEVER.get_relevant_documents(user_query,k=3)
    non_code_results= NONCODE_VECTOR_STORE_RETRIVER.get_relevant_documents(user_query,k=3)

    for ind,doc in enumerate(code_results,1):
        output+=f"""{ind}.  File: {doc.metadata['file_path']}\n Content:-\n{doc.page_content}\n"""

    output+="\nNON CODE RELATED CONTEXT:-----\n"
    
    for ind,doc in enumerate(non_code_results,1):
        output+=f"""{ind}.  File: {doc.metadata['file_path']}\n Content:-\n{doc.page_content}\n"""

    return output
rag_runnable = RunnableLambda(RAG)


def comman_chain(inputs):
    prompt = final_prompt.invoke(inputs).text
    CHAT_HISTORY = inputs["CHAT_HISTORY"]
    CHAT_HISTORY.append(HumanMessage(content=prompt))
    result = CHAT_MODEL.invoke(CHAT_HISTORY).content
    return result
comman_chain_runnable = RunnableLambda(comman_chain)


def follow_up(inputs):
    return "A follow-up question is asked, No context Needed."
follow_up_runnable = RunnableLambda(follow_up)
    

def GENERAL(inputs):
    general_chain = relevant_multiple_files_prompt | relevant_multiple_files_model 
    relevant_files = general_chain.invoke(inputs).file_indices
    output = ""
    FILES_SYMBOL_TABLE = inputs["FILES_DATA"]
    cnt=1

    if(relevant_files[0]==-1):
        output = "No Context Needed."
    else:
        for file_ind in (relevant_files):
            if(file_ind - 1 <0 or file_ind-1 >= len(FILES_SYMBOL_TABLE) ):
                continue
            else:
                content,filename = validate_and_read_file(FILES_SYMBOL_TABLE[file_ind-1]['path'])
                if(content==None):
                    continue
                output+=f"""{cnt}.  Filename: {filename} \nContents:-\n{content}\n"""
                cnt+=1

    return output

general_runnable = RunnableLambda(GENERAL)



def single_file(inputs):
    single_file_chain = relevant_single_file_prompt | relevant_single_file_model
    relevant_files = single_file_chain.invoke(inputs).file_index
    output = ""
    FILES_SYMBOL_TABLE = inputs["FILES_DATA"]
    if(relevant_files == -1):
        output = "No Context Needed."
    else:
        if(relevant_files-1 <0 or relevant_files-1>= len(FILES_SYMBOL_TABLE)):
            output=""
        else:
            content,filename = validate_and_read_file(FILES_SYMBOL_TABLE[relevant_files-1]['path'])
            if(content!=None):
                output+=f"""1.  Filename: {filename} \nContents:-\n{content}\n"""

    return output
single_file_runnable = RunnableLambda(single_file)




classification_chain = classification_prompt | classification_model

branched_chain = RunnableBranch(
        (lambda inputs: inputs["category"] == "FUNCTION&CLASS", rag_runnable),
        (lambda inputs: inputs["category"] == "FOLLOWUP", follow_up_runnable),
        (lambda inputs: inputs["category"] == "GENERAL", general_runnable),
        (lambda inputs: inputs["category"] == "FILE", single_file_runnable),
        lambda x: "No Context Needed",
)


def LLM_OUTPUT(query,CHAT_HISTORY,FILE_SYMBOL_TABLE,file_table_str):
    classification_result = classification_chain.invoke({"query":query}).label.value
    INPUTS = {"category":classification_result,"query":query,"CHAT_HISTORY":CHAT_HISTORY,"file_symbol_table":file_table_str,"FILES_DATA":FILE_SYMBOL_TABLE}
    context = branched_chain.invoke(INPUTS)
    INPUTS["context"]=context
    result = comman_chain_runnable.invoke(INPUTS)
    CHAT_HISTORY.append(AIMessage(content=result))
    return result

