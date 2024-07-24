from qdrant_client import QdrantClient
from typing import List, Dict
from openai import OpenAI

client = QdrantClient(":memory:") # For production

def add_tool_to_vector_store(collection_name: str, tools: List[Dict]):
    try:
        docs=[]
        metadata=[]
        ids=[]
        for i in range(0,len(tools)):
            tool=tools[i]
            function=tool['function']
            doc_string=function['description']
            tool_name=function['name']
            docs.append(doc_string)
            metadata.append({"name": tool_name})
            ids.append(i)
        client.add(
            collection_name=collection_name,
            documents=docs,
            metadata=metadata,
            ids=ids
        )
        return True
    except Exception as e:
        print(e)
        return False


def summarize_user_messages_into_query(user_messages: List[str],openai_client:OpenAI,model:str,tools:List)->str:
    """
    Summarizes user messages into a query to be used for searching in the vector store
    """


    system_prompt=f"""
    You have access to no tools
    You will be given a user request of a user ,
    Given the content you need to summarize user query into a single query that can be used to search in the vector store.
    You will also be given all tool names and their descriptions as system prompt is  given that make a query that targets a tool name given user chat history.
    Only summarize no need to make a tool call
    Just return the query that can be used to search in the vector store
    Because we are searching in vector store make the query look like the tools description
     """
    
    user_message="List of user messages: \n"
    last_message=user_messages[-1]
    if last_message['role']=='user':
        user_message+=f"user: last_message['content']"
    if last_message['role']=='assistant':
        user_message+=f"assistant: last_message['content']"


    query = openai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )

    print(query.choices[0].message.content)

    query = query.choices[0].message.content


    return query



def get_tool_from_vector_store(collection_name: str, query: str,top_k=5):
    try:
        search_results = client.query(
            collection_name=collection_name,
            query_text=query,
            
        )
        tool_names=[]
        for i in range(0,len(search_results)):
            tool=search_results[i]
            tool_name=tool.metadata['name']
            tool_names.append(tool_name)
        
        return tool_names[:top_k]
    except Exception as e:
        return None
    
