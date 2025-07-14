import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from langchain.llms import LlamaCpp
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Setup paths
MODEL_PATH = "./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
TEMP_EXCEL_PATH = "./temp_upload.xlsx"

# Page setup
st.set_page_config(page_title="Excel AI Assistant", layout="wide")
st.title("📊 Excel Data Chat + Visualization with Mistral")

# Upload Excel
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls", "csv"])
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    df.to_csv(TEMP_EXCEL_PATH, index=False)  # Save as CSV to simplify

    st.success("Data uploaded and saved!")
    st.dataframe(df)

    # Display summary
    st.subheader("🔍 Data Summary")
    st.write(df.describe())

    # Display column types
    st.write("**Columns and types:**")
    st.write(df.dtypes)

    # Select chart
    st.subheader("📈 Generate a Chart")
    chart_type = st.selectbox("Select chart type", ["Bar", "Line", "Pie"])
    col1 = st.selectbox("X-axis / Labels", df.columns)
    col2 = None
    if chart_type in ["Bar", "Line"]:
        col2 = st.selectbox("Y-axis / Values", df.select_dtypes(include=['int64', 'float64']).columns)

    if st.button("Generate Chart"):
        fig, ax = plt.subplots()
        if chart_type == "Bar":
            ax.bar(df[col1], df[col2])
        elif chart_type == "Line":
            ax.plot(df[col1], df[col2])
        elif chart_type == "Pie":
            df[col1].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
        st.pyplot(fig)

# Load model if data uploaded
if os.path.exists(TEMP_EXCEL_PATH):
    st.subheader("🤖 Ask Questions about the Data")

    # Load DataFrame
    df = pd.read_csv(TEMP_EXCEL_PATH)

    with st.spinner("Loading model..."):
        llm = LlamaCpp(
            model_path=MODEL_PATH,
            temperature=0.5,
            max_tokens=512,
            top_p=0.95,
            n_ctx=4096,
            n_batch=64,
            verbose=False,
        )

    # Initialize memory and conversation
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory()

    if "conversation" not in st.session_state:
        st.session_state.conversation = ConversationChain(
            llm=llm,
            memory=st.session_state.memory,
            verbose=False
        )

    # User input
    user_prompt = st.text_input("Ask a question about the dataset (e.g., 'What’s the average sales?')")

    if user_prompt:
        try:
            # Append schema to context to help the model
            schema_hint = f"Dataset columns: {', '.join(df.columns)}.\n"
            full_prompt = schema_hint + "Question: " + user_prompt
            response = st.session_state.conversation.predict(input=full_prompt)
            st.markdown("#### 🤖 Response:")
            st.write(response)
        except Exception as e:
            st.error(f"LLM error: {e}")

    # Button to clear memory
    if st.button("🧹 Reset Chat"):
        st.session_state.memory.clear()
        st.success("Conversation memory cleared.")

