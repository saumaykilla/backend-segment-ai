
# Segment AI Backend

This is the backend API for the Segment AI project. It handles authentication, data storage, and interacts with Google Gemini via LangChain to fetch behavioral insights.

## Features

- User authentication and authorization using Supabase  
- Secure backend built with Python FastAPI  
- Integration with Google Gemini using LangChain for AI-powered analysis  

## Getting Started

### Prerequisites

- Python 3.9 or higher  
- Access to a Supabase project  
- Google Cloud API key with access to Google Gemini  

### Environment Variables

Create a `.env` file in the root of this project and add the following variables:

```env
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-anon-key
GOOGLE_API_KEY=your-google-api-key
```

### Installation

1. Clone this repository:

```bash
git clone https://github.com/saumaykilla/backend-segment-ai.git
cd backend-segment-ai
```

2. (Optional) Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the backend server:

```bash
uvicorn main:app --reload
```

By default, the server runs at [http://localhost:8000](http://localhost:8000).

## API Endpoints

Describe your main API endpoints here or link to your API docs.

## Contributing

Feel free to submit issues or pull requests. For major changes, please open an issue to discuss first.

## License

MIT License
