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
