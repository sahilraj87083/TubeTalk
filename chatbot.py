from llm import *
from data_loader import * 
from prompt_template import *
from pre_processing import *

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


from langchain_community.vectorstores import Chroma 
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda , RunnableBranch

import streamlit as st



st.set_page_config(
    page_title = "TubeTalk",
    page_icon = "🤖",
    layout="centered"
)

st.title("TubeTalk")

if "video_id" not in st.session_state:
    st.session_state.video_id = None
    st.session_state.full_transcript = None
    st.session_state.transcript_language = None
    st.session_state.vector_store = None
    st.session_state.retriever = None
    st.session_state.main_chain = None
    st.session_state.chat_history = [{"role": "assistant", "content": "Hello! I'm TubeTalk, your AI assistant. Please share a YouTube URL to get started."}]

for message in st.session_state.chat_history:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(message["content"])


user_input = st.chat_input("Send a YouTube URL or ask a question...")


if user_input:

    st.session_state.chat_history.append({"role": "user", "content": user_input})
    

    with st.chat_message("user"):
        st.markdown(user_input)

    video_id = get_youtube_id(user_input)

    if video_id and video_id != st.session_state.video_id:
        st.session_state.video_id = video_id
        

        try :
            # Fetch transcript and language code of the yt video
            full_transcript , transcript_language  = get_transcript(video_id)
            st.session_state.full_transcript = full_transcript
            st.session_state.transcript_language = transcript_language
            

            # Split transcript into chunks
            chunks = text_spilliter(st.session_state.full_transcript)

            # Create vector store
            vector_store = Chroma.from_documents(chunks, embedding_model)
            st.session_state.vector_store = vector_store


            # Create retriever
            retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
            st.session_state.retriever = retriever

            # check the language code of the existing transcript then set the prompt accordingly

            parallel_chain = RunnableParallel({
                "context": retriever | RunnableLambda(format_docs),
                "question": RunnablePassthrough()
            })

            st.session_state.main_chain = parallel_chain | template | model | parser

            st.session_state.chat_history.append({"role": "assistant", "content": "Transcript fetched and processed! You can now ask questions related to the video."})

            with st.chat_message("assistant"):
                st.markdown("Transcript fetched and processed! You can now ask questions related to the video.")            

        except NoTranscriptFound :
            st.write("No captions found for this video.")

        except TranscriptsDisabled :
            st.write("No captions available for this video.")

    else :
        if st.session_state.main_chain is None :
            st.session_state.chat_history.append({"role": "assistant", "content": "Please share a valid YouTube URL with captions to get started."})

            with st.chat_message("assistant"):
                st.markdown("Please share a valid YouTube URL with captions to get started.")

        else :
            # Process the question through the main chain
            response = st.session_state.main_chain.invoke(user_input)

            answer_text = response["text"] if isinstance(response, dict) else str(response)
            st.session_state.chat_history.append({"role": "assistant", "content": answer_text})

            with st.chat_message("assistant"):
                st.markdown(answer_text)
    

