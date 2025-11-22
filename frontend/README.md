# Tourism AI Assistant - Frontend

React + Vite + Tailwind CSS frontend for the Tourism AI chatbot.

## Features

- Clean, modern chat interface
- Real-time communication with FastAPI backend
- Display weather information and tourist attractions
- Responsive design with Tailwind CSS
- Loading states and error handling

## Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure API URL

The frontend is configured to connect to `http://localhost:8000` by default.

If your backend runs on a different URL, update the `API_BASE_URL` in `src/components/ChatInterface.jsx`.

### 3. Run the Development Server

```bash
npm run dev
```

The frontend will be available at: **http://localhost:5173**

## Usage

1. Make sure the backend is running on `http://localhost:8000`
2. Start the frontend development server
3. Open `http://localhost:5173` in your browser
4. Start chatting with the tourism assistant!

### Example Queries

- "What's the weather in Paris?"
- "I'm going to Tokyo, let's plan my trip"
- "Tell me about Bangalore and what's the temperature there"
- "What can I do in London and what's the weather like?"

## Technologies Used

- **React 19**: UI framework
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
