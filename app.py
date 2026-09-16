import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from serpapi import GoogleSearch

st.title("My AI Agent")


# Web Search Function
def web_search(query):
    search = GoogleSearch({
        "q": query,
        "api_key": st.secrets["SERPAPI_API_KEY"],
        "engine": "google"
    })

    results = search.get_dict()
    return results.get("organic_results", [])


# Groq API Key
api_key = st.secrets["GROQ_API_KEY"]


if api_key:

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        api_key=api_key
    )

    user_input = st.text_input("Ask me anything:")

    if user_input:

        # Web Search
        search_results = web_search(user_input)

        if search_results:

            st.write("### Web Search Results")

            for result in search_results[:3]:
                st.write(result.get("title"))
                st.write(result.get("link"))
                st.write(result.get("snippet"))
# AI Response using search results
search_text = ""

for result in search_results[:3]:
    search_text += result.get("title", "") + "\n"
    search_text += result.get("snippet", "") + "\n"

response = llm.invoke([
    HumanMessage(
        content=f"""
Use the following web search results to answer the user's question.

Web Search Results:
{search_text}

User Question:
{user_input}

Give a simple and clear answer based on the search results.
"""
    )
])

st.write("### AI Agent Response")
st.write(response.content)