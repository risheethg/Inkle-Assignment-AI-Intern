import { useState, useEffect } from 'react';

function LoadingDots() {
  const [dots, setDots] = useState('');
  const messages = [
    'Analyzing your request',
    'Gathering information',
    'Processing data',
    'Preparing response'
  ];
  const [messageIndex, setMessageIndex] = useState(0);

  useEffect(() => {
    const dotsInterval = setInterval(() => {
      setDots(prev => prev.length >= 3 ? '' : prev + '.');
    }, 400);

    const messageInterval = setInterval(() => {
      setMessageIndex(prev => (prev + 1) % messages.length);
    }, 2000);

    return () => {
      clearInterval(dotsInterval);
      clearInterval(messageInterval);
    };
  }, []);

  return (
    <div className="space-y-3">
      <div className="flex items-center space-x-3">
        <div className="w-3 h-3 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full animate-bounce shadow-lg" style={{ animationDelay: '0s' }}></div>
        <div className="w-3 h-3 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full animate-bounce shadow-lg" style={{ animationDelay: '0.15s' }}></div>
        <div className="w-3 h-3 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full animate-bounce shadow-lg" style={{ animationDelay: '0.3s' }}></div>
      </div>
      <div className="text-purple-200 text-sm font-medium animate-pulse">
        {messages[messageIndex]}{dots}
      </div>
    </div>
  );
}

export default LoadingDots;
