import streamlit as st
from api_client import api_client

st.set_page_config(
    page_title="HR Policy Assistant | ITI RAG Project",
    page_icon="📚",
    layout="wide"
)

# Sidebar with system status and instructions
with st.sidebar:
    st.title("📚 Document Assistant")
    st.caption("Grounded HR Policy Question-Answering")
    
    st.divider()
    
    # Check backend connection status
    health = api_client.check_health()
    if health.get("status") == "healthy":
        st.success("● Backend Online")
        st.write(f"**Indexed Chunks:** {health.get('chunks_indexed', 'N/A')}")
    else:
        st.error("○ Backend Offline")
        st.caption("Ensure `uvicorn app.main:app` is running on port 8000.")

    st.divider()
    st.markdown("""
    **Indexed Sources:**
    - 11 Verified Digital Handbooks
    - Strict Context Grounding
    - Local LLM via Ollama (`llama3.2`)
    """)

# Main Chat Header
st.header("🏢 Employee Handbook RAG Assistant")
st.markdown("Ask policy questions regarding leave, working hours, benefits, or conduct to receive cited answers grounded in indexed company handbooks.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📄 View Cited Sources"):
                for src in msg["sources"]:
                    st.markdown(f"- {src}")

# Handle new user input
if prompt := st.chat_input("Ask a question about handbook policies..."):
    # Append user question
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant answer with loading state
    with st.chat_message("assistant"):
        with st.spinner("Searching document index and synthesizing answer..."):
            result = api_client.send_query(prompt)

        if result["success"]:
            answer_text = result["data"]["answer"]
            sources_list = result["data"]["sources"]

            st.markdown(answer_text)
            if sources_list:
                with st.expander("📄 View Cited Sources"):
                    for src in sources_list:
                        st.markdown(f"- {src}")

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer_text,
                "sources": sources_list
            })
        else:
            st.error(result["error"])