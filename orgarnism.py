import os
import streamlit as st
from groq import Groq

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="SUBALO",
    page_icon="🧬",
    layout="centered"
)

# -----------------------------
# Get Groq API key
# -----------------------------
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is not set.")
    st.info(
        "Set your Groq API key as an environment variable before running the app."
    )
    st.stop()

client = Groq(api_key=api_key)

# -----------------------------
# System instructions
# -----------------------------
SYSTEM_PROMPT = """
You are BioBot, an educational AI assistant specializing in living organisms.

Your main areas of expertise include:
- Biology
- Zoology
- Botany
- Microbiology
- Mycology
- Anatomy and physiology
- Cell biology
- Genetics
- Evolution
- Ecology
- Taxonomy and biological classification
- Biodiversity
- Reproduction
- Nutrition
- Respiration
- Adaptation
- Animal behavior
- Plant biology
- Microorganisms
- Conservation biology

Answer questions clearly and accurately.

Rules:
1. Explain difficult biological concepts in simple language when appropriate.
2. Give examples whenever they improve understanding.
3. For classification questions, provide the relevant taxonomic levels when possible.
4. Distinguish between established scientific facts and uncertain or debated claims.
5. Never invent scientific facts.
6. If a question is unrelated to biology or living organisms, politely explain
   that you specialize in biology and offer to answer a biology-related question.
7. Do not diagnose diseases or replace a qualified medical professional.
8. For medical or health questions, provide general educational information and
   recommend consulting an appropriate healthcare professional when necessary.
9. Use scientific names in italics conceptually, for example Homo sapiens.
10. Structure longer answers with headings and bullet points.
"""

# -----------------------------
# App title
# -----------------------------
st.title("🧬 BioBot")
st.subheader("Your AI Assistant for Living Organisms")

st.write(
    "Ask me about animals, plants, fungi, microorganisms, cells, "
    "genetics, evolution, ecology, and more."
)

# -----------------------------
# Initialize chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

# -----------------------------
# Display previous messages
# -----------------------------
for message in st.session_state.messages:
    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat input
# -----------------------------
user_question = st.chat_input(
    "Ask a question about living organisms..."
)

if user_question:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_question)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    # Generate response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.3,
                max_tokens=1500
            )

            answer = response.choices[0].message.content

            response_placeholder.markdown(answer)

            # Save assistant response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as e:
            error_message = f"Sorry, an error occurred: {str(e)}"
            response_placeholder.error(error_message)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("🧬 BioBot")

    st.write("### Topics I can answer")

    st.markdown("""
    - 🐘 Animals
    - 🌱 Plants
    - 🍄 Fungi
    - 🦠 Microorganisms
    - 🔬 Cells
    - 🧬 Genetics
    - 🦴 Anatomy
    - ❤️ Physiology
    - 🌍 Ecology
    - 🐒 Evolution
    - 🧪 Microbiology
    - 📚 Taxonomy
    - 🌳 Biodiversity
    - ♻️ Conservation
    """)

    st.divider()

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        st.rerun()
