# Personalized Content Agent

This repository contains the code for a personalized content generation agent built using CrewAI, Pydantic, and Streamlit. The agent takes user search history as input, processes it to remove duplicates and prioritize recent searches, and then generates a structured, personalized content output.

## 🖥️ User Interface
<img src="/data/sample1.png" alt="sample1" />
<img src="/data/sample2.png" alt="sample2" />

## Features

*   **Personalized Content Generation:** Creates content tailored to user search queries.
*   **Recent Search Prioritization:** Focuses on the most recent searches for more relevant content.
*   **Duplicate Query Handling:** Avoids redundancy by removing duplicate search terms.
*   **Structured Output:** Uses Pydantic models to ensure a consistent and well-defined output format.
*   **Streamlit Interface:** Provides a user-friendly web interface for easy interaction.
*   **Sample Inputs:** Includes predefined sample inputs for quick testing and demonstration.

## Technologies Used

*   **CrewAI:** For agent orchestration and task management.
*   **Pydantic:** For data validation and structuring.
*   **Streamlit:** For creating the web interface.
*   **Python:** The primary programming language.
*   **LLM (e.g., Groq):** For natural language processing and content generation (you'll need to configure your own LLM).

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/santhosh-anbazhagan/personalized-content-agent.git
    cd personalized-content-agent
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    Make sure your `requirements.txt` file includes:

    ```
    crewai
    pydantic
    streamlit
    # Add any other dependencies, including your LLM library (e.g., groq)
    ```

4.  **Configure your LLM:**

    You need to configure your LLM (e.g., Groq) credentials and initialize the LLM instance in the Python code. Replace the placeholder `llm` with your actual LLM object. For Example if you are using groq you need to install groq and set the API key.

    ```bash
    pip install groq
    ```

    Set you api key
    ```python
    import os
    os.environ["GROQ_API_KEY"] = "YOUR_API_KEY"
    from groq import Groq
    llm = Groq()
    ```

5.  **Run the Streamlit app:**

    ```bash
    streamlit run app.py
    ```

## Usage

1.  Open the Streamlit app in your web browser (usually at `http://localhost:8501`).
2.  Select a sample input from the dropdown or enter your own comma-separated search history in the specified format (`YYYY-MM-DD HH:MM:SS query`).
3.  Click the "Generate Personalized Content" button.
4.  The generated content will be displayed on the page.

## Input Format

The input should be a comma-separated string of search entries, where each entry is in the format: