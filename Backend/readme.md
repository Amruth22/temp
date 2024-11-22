# Intipal Chat Application

Intipal is a chat-based application that leverages a Python Flask backend and a React frontend to answer user queries using AI and document retrieval.

## Prerequisites

Ensure the following are installed:

- **Python** (>= 3.9)
- **Node.js** (>= 14.x)
- **npm** or **yarn**
- **pip** for Python package management

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/cresolindiateam/palnar_GPT.git
cd palnar_GPT
```

### 2. Backend Setup (Python Flask)

#### Navigate to the Backend Directory
```bash
cd Backend
```

#### Install Python Dependencies

Create a virtual environment:(optional)
```bash
python -m venv venv
source venv/bin/activate   # On Windows, use venv\Scripts\activate
```

Install the required packages:
```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

Add your OpenAI API key to the .env file:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

#### Run the Flask Server
```bash
python app.py
```
The backend will run at [http://127.0.0.1:5000](http://127.0.0.1:5000).

### 3. Frontend Setup (React)

#### Navigate to the Frontend Directory
```bash
cd frontend
```

#### Install Node Dependencies
```bash
npm install
```

#### Start the Frontend Development Server
```bash
npm run dev
```
The frontend will run at [http://localhost:3000](http://localhost:3000).

---

## API Endpoints

### Flask Backend

#### Ask a Question
- **Endpoint**: `/ask`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "question": "What is Cybba?"
  }
  ```
- **Response**:
  ```json
  {
    "answer": "Cybba is a performance-driven technology company."
  }
  ```

#### Health Check
- **Endpoint**: `/health`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "status": "healthy"
  }
  ```

---

## Troubleshooting

- Ensure Python and Node.js versions meet the prerequisites.
- If `pip install` fails, upgrade pip:
  ```bash
  pip install --upgrade pip
  ```
- Check if the `.env` file is correctly configured with your OpenAI API key.
