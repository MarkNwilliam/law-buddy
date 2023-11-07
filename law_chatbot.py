# First
import openai 
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

openai_api_key = st.secrets.OPENAI_API_KEY
import json
import requests

st.title("Legal Chatbot")

st.sidebar.title("Customization Options")
    
customization_options = {
        "country": st.sidebar.selectbox("Select Country", ["INDIA", "USA", "UK"]),
        "use_chatgpt":st.sidebar.radio("Use ChatGPT", ["No", "Yes"]),
        "words": st.sidebar.slider("Number of words", 0, 750, 100),
        "src": st.sidebar.radio("Show Source of Text", ["No", "Yes"])
    }

country_cid = {"INDIA": 5, "USA": 6, "UK": 7}
all_country_api = "zwt_h_p6lWnM5xwLO7Cd-3T6HPyphP7F78VOtZTPTg"

doc_api = 'zwt_h_p6lRRxXAfEbeh006odfopywkBn2YWcZJxEgg'

def query_vectara(corpus_id, query, api):
    url = "https://api.vectara.io/v1/query"
    payload = json.dumps({
    "query": [
        {
        "query": query,
        "start": 0,
        "numResults": 10,
        "contextConfig": {
            "charsBefore": 30,
            "charsAfter": 30,
            "sentencesBefore": 3,
            "sentencesAfter": 3,
            "startTag": "<b>",
            "endTag": "</b>"
        },
        "corpusKey": [
            {
            "customerId": 0,
            "corpusId": corpus_id,
            "semantics": "DEFAULT",
            "dim": [
                {
                "name": "string",
                "weight": 0
                }
            ],
            "metadataFilter": "part.lang = 'eng'",
            "lexicalInterpolationConfig": {
                "lambda": 0
            }
            }
        ],
        "rerankingConfig": {
            "rerankerId": 272725717
        },
        "summary": [
        {
          "summarizerPromptName": "vectara-summary-ext-v1.2.0",
          "maxSummarizedResults": 5,
          "responseLang": "en"
        }
        ]
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'customer-id': '2281339541',
    'x-api-key': api
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    k = response.text
    k = json.loads(k)

    return k 

# extract summary and all text 

def extract_from_vectara(vectera_response):
    summary = vectera_response['responseSet'][0]['summary'][0]['text']

    # all text
    all_text = ""
    for i in vectera_response['responseSet'][0]['response']:
        all_text = all_text + i['text'] + '\n'

    return summary, all_text


# OPENAI_API_KEY = st.secrets.OPENAI_API_KEY

llm = ChatOpenAI(temperature=0.9, openai_api_key = openai_api_key)

def query_gpt(lawtext, text, query):
    nwords = customization_options['words']
    prompt = "Using the above " + lawtext + "and the current information related to it " + text + "answer the queestion given below {query} in {nwords}" 
    prompt = ChatPromptTemplate.from_template(prompt)

    chain = LLMChain(llm=llm, prompt=prompt)

    output = chain.run(query)

    return output



if 1:
    if "messages" not in st.session_state.keys(): # Initialize the chat messages history
        st.session_state.messages = [{"role": "assistant", "content": "Ask me anything about the law!"}]

    if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages: # Display the prior chat messages
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                cid = country_cid[customization_options['country']]
                resp = query_vectara(cid, prompt, all_country_api)
                msg, texts = extract_from_vectara(resp)
                if customization_options["use_chatgpt"] == "Yes":
                    # cid = country_cid[customization_options['country']]
                    # resp1 = query_vectara(cid, prompt, all_country_api)
                    # msg1, texts1 = extract_from_vectara(resp1)
                    # msg = query_gpt(texts1, texts, prompt)
                    nwords = customization_options['words']
                    prompt1 = "using the above text " + texts + "answer the following question {query} in " + str(nwords)
                    prompt1 = ChatPromptTemplate.from_template(prompt1)

                    chain = LLMChain(llm=llm, prompt=prompt1)

                    msg = chain.run(prompt)

                st.write(msg)
                if customization_options['src'] == "Yes":
                    st.code(texts, language='python')
                message = {"role": "assistant", "content": msg}
                st.session_state.messages.append(message) # Add response to message history
