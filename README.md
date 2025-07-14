# AI-analysits
## Excel AI Assistant

A Streamlit-based web application that allows users to upload Excel or CSV files, visualize data through charts, and interact with the dataset using natural language queries powered by the Mistral-7B language model.

## Features
- **File Upload**: Upload Excel (`.xlsx`, `.xls`) or CSV (`.csv`) files for analysis.
- **Data Visualization**: Generate bar, line, or pie charts based on user-selected columns.
- **Data Summary**: View basic statistics and column data types of the uploaded dataset.
- **Natural Language Queries**: Ask questions about the dataset (e.g., "What’s the average sales?") using the Mistral-7B model.
- **Conversation Memory**: Maintains context for follow-up questions, with an option to reset the conversation.

## Tech Stack
- **Python Libraries**:
  - `pandas`: Data manipulation and analysis.
  - `streamlit`: Web application framework.
  - `matplotlib`: Chart generation.
  - `langchain`: Integration with LLMs for conversational AI.
  - `llama-cpp-python`: Interface for running the Mistral-7B model locally.
- **Model**: Mistral-7B-Instruct (Q4_K_M quantized, stored in `./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf`).
- **Package Manager**: `uv` for managing Python environments and dependencies.

## Prerequisites
- Python 3.12
- `uv` installed (install via `pip install uv` or follow [uv installation guide](https://github.com/astral-sh/uv)).
- A compatible GPU (recommended) for running the Mistral-7B model efficiently.
- The Mistral-7B model file (`mistral-7b-instruct-v0.1.Q4_K_M.gguf`) downloaded and placed in the `./models/` directory.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/excel-ai-assistant.git
   cd excel-ai-assistant
