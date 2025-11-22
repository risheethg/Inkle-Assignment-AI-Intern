import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import MessageBubble from './MessageBubble';
import LoadingDots from './LoadingDots';
import ThinkingDropdown from './ThinkingDropdown';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

function ChatInterface() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hey there! I\'m TravelMate, your AI travel companion. Ask me about weather conditions or discover amazing places to visit anywhere in the world!',
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentReasoning, setCurrentReasoning] = useState([]);
  const [isThinkingComplete, setIsThinkingComplete] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    const queryText = inputValue;
    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setCurrentReasoning([]);
    setIsThinkingComplete(false);

    try {
      // Build conversation history
      const conversationHistory = messages
        .filter(msg => !msg.timestamp || messages.indexOf(msg) > 0)
        .map(msg => ({
          role: msg.role,
          content: msg.content
        }));

      // Use EventSource for SSE streaming
      const eventSource = new EventSource(
        `${API_BASE_URL}/tourism/chat/stream?${new URLSearchParams({
          query: queryText,
          conversation_history: JSON.stringify(conversationHistory)
        })}`
      );

      // Use fetch with streaming instead
      const response = await fetch(`${API_BASE_URL}/tourism/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: queryText,
          conversation_history: conversationHistory,
        }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let buffer = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6));
            
            if (data.type === 'reasoning') {
              setCurrentReasoning(prev => [...prev, data.data]);
            } else if (data.type === 'complete') {
              setIsThinkingComplete(true);
              const assistantMessage = {
                role: 'assistant',
                content: data.data.final_response,
                data: data.data,
                reasoning: currentReasoning,
                timestamp: new Date(),
              };
              setMessages((prev) => [...prev, assistantMessage]);
              setCurrentReasoning([]);
            } else if (data.type === 'error') {
              throw new Error(data.message);
            }
          }
        }
      }
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: error.message || 'Oops! I\'m having trouble connecting. Please make sure the backend server is running on http://localhost:8000',
        isError: true,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
      setCurrentReasoning([]);
    } finally {
      setIsLoading(false);
      setIsThinkingComplete(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const quickPrompts = [
    "Weather in Paris?",
    "Best places in Tokyo?",
    "Plan my Bali trip"
  ];

  return (
    <div className="max-w-5xl mx-auto">
      <div className="bg-white/10 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 overflow-hidden">
        {/* Chat Messages */}
        <div className="h-[calc(100vh-350px)] min-h-[400px] max-h-[600px] overflow-y-auto p-4 md:p-6 space-y-4 scroll-smooth">
          {messages.map((message, index) => (
            <MessageBubble key={index} message={message} />
          ))}
          {isLoading && (
            <>
              <ThinkingDropdown 
                reasoningSteps={currentReasoning} 
                isComplete={isThinkingComplete} 
              />
              <div className="flex justify-start animate-fadeIn">
                <div className="bg-white/20 backdrop-blur-md rounded-2xl px-5 py-4 border border-white/30">
                  <LoadingDots />
                </div>
              </div>
            </>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Quick Prompts */}
        {messages.length === 1 && !isLoading && (
          <div className="px-4 md:px-6 pb-4">
            <p className="text-purple-200 text-sm mb-2 font-medium">Quick examples:</p>
            <div className="flex flex-wrap gap-2">
              {quickPrompts.map((prompt, idx) => (
                <button
                  key={idx}
                  onClick={() => setInputValue(prompt)}
                  className="px-4 py-2 bg-white/10 hover:bg-white/20 text-purple-100 rounded-full text-sm border border-white/20 transition-all duration-200 hover:scale-105"
                >
                  {prompt}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input Form */}
        <form
          onSubmit={handleSubmit}
          className="border-t border-white/20 p-4 md:p-6 bg-white/5"
        >
          <div className="flex flex-col sm:flex-row gap-3">
            <div className="flex-1 relative">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about weather or discover places..."
                className="w-full px-6 py-4 bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent text-white placeholder-purple-200/50 transition-all"
                disabled={isLoading}
              />
              <div className="absolute right-4 top-1/2 -translate-y-1/2 text-purple-300/50">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>
            <button
              type="submit"
              disabled={isLoading || !inputValue.trim()}
              className="w-full sm:w-auto px-6 md:px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-2xl font-semibold hover:from-purple-600 hover:to-pink-600 disabled:from-gray-600 disabled:to-gray-600 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-purple-500/50 hover:scale-105 active:scale-95 flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              )}
              <span>{isLoading ? 'Thinking...' : 'Send'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default ChatInterface;
