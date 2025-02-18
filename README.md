# PDF Assistant with LangChain

This project demonstrates a question-answering system using Astra DB and LangChain, powered by Vector Search. The system allows you to query PDF documents and get relevant answers using OpenAI's language models.

## Prerequisites

1. **Serverless Cassandra with Vector Search** database on [Astra DB](https://astra.datastax.com)
   - Follow [this guide](https://docs.datastax.com/en/astra-serverless/docs/vector-search/quickstart.html#_prepare_for_using_your_vector_database) to prepare your database.
   - Obtain a DB Token with the role _Database Administrator_.
   - Copy your Database ID.

2. **OpenAI API Key**
   - Get your API key from [OpenAI](https://cassio.org/start_here/#llm-access).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/pdf_assistant_langchain.git
   cd pdf_assistant_langchain

Based on the content of the script, we can structure the GitHub repository as follows:  
pdf_assistant_langchain/
├── README.md
├── requirements.txt
└── pdf_assistant_langchain.py


Install the required dependencies:
pip install -r requirements.txt

## Usage
1.Update the following variables in pdf_assistant_langchain.py with your credentials:
ASTRA_DB_APPLICATION_TOKEN = "your_astra_db_application_token"
ASTRA_DB_ID = "your_astra_db_id"
ASTRA_DB_REGION = "your_astra_db_region"
OPENAI_API_KEY = "your_openai_api_key"
2.Run the script:
python pdf_assistant_langchain.py
3.Enter your questions when prompted. Type 'quit' to exit the interactive loop.

## Features
Query a PDF document for answers.
Generate multiple-choice questions (MCQs) based on the answers.
Retrieve and display the most relevant documents.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
## License
This project is licensed under the MIT License. See the LICENSE file for details.
