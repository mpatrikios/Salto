# Salto - AI-Powered Data Explorer

Salto is a Python Flask application that provides an AI-powered business data explorer using Azure OpenAI integration. It allows users to upload, manage, and analyze business data through natural language conversations.

## Features

- 💬 **Conversational Interface**: Ask questions about your business data in natural language
- 🧠 **Azure OpenAI Integration**: Uses GPT models via Azure OpenAI to analyze and interpret data
- 📊 **Business Data Management**: Upload, view, and manage different data sets
- 🔄 **Multi-Instance Support**: Create separate instances for different businesses or projects
- 👤 **Admin Controls**: Secure admin interface for configuration and management
- 🚀 **Demo Data Generation**: Quick-start with AI-generated sample business data

## Requirements

- Python 3.9+
- MongoDB (local or Atlas)
- Azure OpenAI API access

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/salto.git
   cd salto
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the `.env.example` file to `.env` and update the configuration:
   ```bash
   cp .env.example .env
   ```

5. Update the `.env` file with your settings:
   - Set your MongoDB connection string
   - Add your Azure OpenAI API key and endpoint
   - Update the admin password