import { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Tourism AI Assistant
          </h1>
          <p className="text-gray-600">
            Plan your trip with AI-powered weather and places recommendations
          </p>
        </header>
        <ChatInterface />
      </div>
    </div>
  );
}

export default App;
