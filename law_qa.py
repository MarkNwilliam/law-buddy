# First
import openai 
import streamlit as st
import requests
import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

st.session_state.k1 = 0

st.sidebar.title("Customization Options")
    
openai_api_key = st.secrets.OPENAI_API_KEY

customization_options = {
        "country": st.sidebar.selectbox("Select Country", ["INDIA", "USA", "UK"]),
        "use_chatgpt":st.sidebar.radio("Use ChatGPT", ["No", "Yes"]),
        "words": st.sidebar.slider("Number of words", 0, 750, 100),
        "src": st.sidebar.radio("Show Source of Text", ["No", "Yes"])
    }

country_cid = {"INDIA": 5, "USA": 6, "UK": 7}
all_country_api = "zwt_h_p6lWnM5xwLO7Cd-3T6HPyphP7F78VOtZTPTg"

doc_api = 'zwt_h_p6lTWvH8AmgesgThxhNecMP28NKYcLqN2_xw'


llm = ChatOpenAI(temperature=0.9, openai_api_key = openai_api_key)

def query_gpt(lawtext, text, query):
    nwords = customization_options['words']
    prompt = "Using the above " + lawtext + "and the current information related to it " + text + "answer the queestion given below {query} in " + str(nwords) 
    prompt = ChatPromptTemplate.from_template(prompt)

    chain = LLMChain(llm=llm, prompt=prompt)

    output = chain.run(query)

    return output



def query_vectara(corpus_id, query, api):
    url = "https://api.vectara.io/v1/query"
    payload = json.dumps({
    "query": [
        {
        "query": query,
        "start": 0,
        "numResults": 3,
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

def reset_corpus(corpus_id):
    url = "https://api.vectara.io/v1/reset-corpus"
    payload = json.dumps({
    "corpusId": corpus_id
    })
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'customer-id': '2281339541',
    'Authorization': 'Bearer eyJraWQiOiI1SDgrV3FSeW5RNERCdUVGNG1DUDVCUmNTSUN4RlBJalROTnNBbExsK2I0PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI0MmdjcWg2anI2bWlnN25kMXBwOXF2Z3E0aCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiUXVlcnlTZXJ2aWNlXC9RdWVyeSBRdWVyeVNlcnZpY2VcL1N0cmVhbVF1ZXJ5IiwiYXV0aF90aW1lIjoxNjk5MzgxOTg4LCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtd2VzdC0yLmFtYXpvbmF3cy5jb21cL3VzLXdlc3QtMl9iS2tSanhMejYiLCJleHAiOjE2OTkzODU1ODgsImlhdCI6MTY5OTM4MTk4OCwidmVyc2lvbiI6MiwianRpIjoiYjAxMjljNGItYjJmNC00MTQyLWI4MDctOTQxYmVlN2I1MmM4IiwiY2xpZW50X2lkIjoiNDJnY3FoNmpyNm1pZzduZDFwcDlxdmdxNGgifQ.Kfodh9rxjeisdYxNwhU_SdiIhMDEg5Ywr9EP5SNI4KeB2mTddzTi0Lov7y_nvLiV4jWHvrGBZEbIqiT3W7kncYgpqcNYlvA-MNEWdyW3D-6POAPikrvgKOB_07B1hSI0XWN_5j4SYwDbdlnTvwAh1uxB845YYgECGoDYab6GohY_mc_9USq-DiuVKdT7HJI7qRP9X2bPKsPvM6HrCXZqMl_zkQL6IDj0BHWVX8UTnz3apI8Pi3ZWyFjoI3fDJvsg7oeEiP4dJbqZVHg_9sA_nsPCzMi7OcWVgt9bbIFzQlVVDRlNMr0b7hdBZDXYAYwU8YrhJyMZuISrP0mbKQiHUw'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response


def upload_file(file, filename):
    post_headers = {
        "Authorization": f"Bearer eyJraWQiOiI1SDgrV3FSeW5RNERCdUVGNG1DUDVCUmNTSUN4RlBJalROTnNBbExsK2I0PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI0MmdjcWg2anI2bWlnN25kMXBwOXF2Z3E0aCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiUXVlcnlTZXJ2aWNlXC9RdWVyeSBRdWVyeVNlcnZpY2VcL1N0cmVhbVF1ZXJ5IiwiYXV0aF90aW1lIjoxNjk5MzgyOTAzLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtd2VzdC0yLmFtYXpvbmF3cy5jb21cL3VzLXdlc3QtMl9iS2tSanhMejYiLCJleHAiOjE2OTkzODY1MDMsImlhdCI6MTY5OTM4MjkwMywidmVyc2lvbiI6MiwianRpIjoiZDNjMjE0YjgtMDRiNy00YjgyLWFjN2QtM2ViNDA1ZjZiMzE1IiwiY2xpZW50X2lkIjoiNDJnY3FoNmpyNm1pZzduZDFwcDlxdmdxNGgifQ.XjqLae0GNMBWPlSGMCcgBgWZtDRChHcvnK3JT2RbOuDUZLgQ6b1vdkYKg9PKEU05_Y267ziqV2anSCDceOvAJhr4K0S-PnSUKpaJ9X5fEM1p6pDPeyzVQJZuHF8PmT4X9dgrY60HULd0wwdwLQ3FoNEEnoI8BEXfpq19uh96XO-xXDFdvSnbmjCop_I6KjS1NJoVntX6DlZeCzbPiCqYstoa9FcQTQN08d4A8qTi2-q9Vn4O2HUOlwfZ6C_ETluXWX6On8BVqJjmBfpgshhbovEpRdhO1fT17zkIkHmxfz3PQyrp-SW1UlqD6nSWo9-MEXPTTbntep81sPpgEEa7Uw",
    }
    response = requests.post(
        f"https://api.vectara.io/v1/upload?c=2281339541&o=4",
        files={"file": (filename ,file , 'application/octet-stream')},
        verify=True,
        headers=post_headers)

    if response.status_code != 200:
        return response, False
    return response, True

@st.cache_resource()
def uploader(uploaded_file):
    
    if uploaded_file and st.session_state.k1 == 0:

        res = reset_corpus(4)

        # st.write(res)

        binary_file = uploaded_file.read()

        filename = uploaded_file.name 

        response = upload_file(binary_file, filename)

        # st.write(response)

        st.session_state.k1 +=1

        return True


def main():
    k = 0
    st.title("Chat with your documents")
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "png", "jpg", "jpeg"])

    m = uploader(uploaded_file)

    if 1:
    # st.write(response)
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
                    resp = query_vectara(4, prompt, doc_api)
                    msg, texts = extract_from_vectara(resp)
                    # st.write(resp)
                    cid = country_cid[customization_options['country']]
                    # resp = query_vectara(cid, prompt, all_country_api)
                    # msg, texts = extract_from_vectara(resp)
                    if customization_options["use_chatgpt"] == "Yes":
                        cid = country_cid[customization_options['country']]
                        resp1 = query_vectara(cid, prompt, all_country_api)
                        msg1, texts1 = extract_from_vectara(resp1)
                        msg = query_gpt(texts1[:1024], texts[:1024], prompt)

                    st.write(msg)
                    message = {"role": "assistant", "content": msg}
                    st.session_state.messages.append(message) 



if __name__ == "__main__":
    main()
