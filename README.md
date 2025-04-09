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

5. Set up MongoDB connection
   ```
   # Install Homebrew (if not already installed)
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install MongoDB
   brew tap mongodb/brew
   brew install mongodb-community
   
   # Start MongoDB service
   brew services start mongodb-community
   ```

7. To run application
    ```bash
   python run.py
   ```
