import { useState } from 'react';
import InteractivePlace from './InteractivePlace';
import WeatherCard from './WeatherCard';
import LocationCard from './LocationCard';

function MessageBubble({ message, onSuggestionClick }) {
  const isUser = message.role === 'user';
  const isError = message.isError;
  const [copiedText, setCopiedText] = useState(false);

  const handleCopyMessage = () => {
    navigator.clipboard.writeText(message.content);
    setCopiedText(true);
    setTimeout(() => setCopiedText(false), 2000);
  };

  const handleLearnMore = (place) => {
    if (onSuggestionClick) {
      onSuggestionClick(`Tell me more about ${place}`);
    }
  };

  const handleExploreLocation = (location) => {
    if (onSuggestionClick) {
      onSuggestionClick(`What are the best things to do in ${location}?`);
    }
  };

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-fadeIn`}>
      <div className={`flex gap-2 md:gap-3 max-w-[95%] md:max-w-[85%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-8 h-8 md:w-10 md:h-10 rounded-full flex items-center justify-center ${
          isUser 
            ? 'bg-gradient-to-br from-purple-500 to-pink-500' 
            : 'bg-gradient-to-br from-blue-500 to-purple-500'
        } shadow-lg`}>
          {isUser ? (
            <svg className="w-4 h-4 md:w-6 md:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          ) : (
            <svg className="w-4 h-4 md:w-6 md:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          )}
        </div>

        {/* Message Content */}
        <div
          className={`rounded-2xl px-3 md:px-5 py-2 md:py-3 shadow-lg ${
            isUser
              ? 'bg-gradient-to-br from-purple-500 to-pink-500 text-white'
              : isError
              ? 'bg-red-500/20 text-red-100 border border-red-400/50 backdrop-blur-md'
              : 'bg-white/20 text-white border border-white/30 backdrop-blur-md'
          }`}
        >
          {/* Main content - clean it up by removing markdown formatting */}
          <div className="whitespace-pre-wrap break-words leading-relaxed text-sm md:text-base">
            {isUser 
              ? message.content 
              : message.content
                  .replace(/\*\*/g, '') // Remove bold markers
                  .replace(/\*/g, '')   // Remove italic markers
                  .split('\n')
                  .filter(line => 
                    !line.includes('Weather:') && 
                    !line.includes('Location:') && 
                    !line.trim().match(/^\d+\./)
                  )
                  .join('\n')
                  .trim()
            }
          </div>

          {/* Copy button for assistant messages */}
          {!isUser && !isError && (
            <button
              onClick={handleCopyMessage}
              className="mt-2 inline-flex items-center gap-1 px-3 py-1 bg-white/10 hover:bg-white/20 rounded-lg text-xs text-purple-200 hover:text-white transition-all border border-white/20 hover:border-white/40"
            >
              {copiedText ? (
                <>
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Copied!</span>
                </>
              ) : (
                <>
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                  </svg>
                  <span>Copy</span>
                </>
              )}
            </button>
          )}
          
          {/* Show structured data for assistant responses */}
          {!isUser && !isError && message.data && (
            <div className="mt-4 pt-4 border-t border-white/20 space-y-3">
              {message.data.location && (
                <LocationCard 
                  location={message.data.location} 
                  onExplore={handleExploreLocation}
                />
              )}
              
              {message.data.weather_info && (
                <WeatherCard weatherInfo={message.data.weather_info} />
              )}
              
              {message.data.places_info && message.data.places_info.length > 0 && (
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <svg className="w-5 h-5 text-pink-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                    <span className="font-semibold text-pink-200">Top Attractions</span>
                    <span className="text-xs bg-pink-500/30 px-2 py-1 rounded-full text-pink-200">
                      {message.data.places_info.length} places
                    </span>
                  </div>
                  <div className="space-y-2">
                    {message.data.places_info.map((place, idx) => (
                      <InteractivePlace
                        key={idx}
                        place={place}
                        index={idx}
                        onLearnMore={handleLearnMore}
                      />
                    ))}
                  </div>
                </div>
              )}
              
              {/* Reasoning Trace */}
              {message.data.reasoning_trace && message.data.reasoning_trace.length > 0 && (
                <div className="mt-4 pt-4 border-t border-white/20">
                  <button 
                    onClick={() => {
                      const details = document.getElementById(`reasoning-${message.timestamp.getTime()}`);
                      details.style.display = details.style.display === 'none' ? 'block' : 'none';
                    }}
                    className="flex items-center gap-2 text-sm text-purple-200 hover:text-purple-100 transition-colors"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <span className="font-semibold">Show Agent Thinking ({message.data.reasoning_trace.length} steps)</span>
                  </button>
                  <div id={`reasoning-${message.timestamp.getTime()}`} style={{display: 'none'}} className="mt-3 space-y-2">
                    {message.data.reasoning_trace.map((step, idx) => (
                      <div key={idx} className="bg-white/10 rounded-lg p-3 border border-white/20">
                        <div className="flex items-center gap-2 mb-1">
                          <div className="w-6 h-6 rounded-full bg-purple-500/30 flex items-center justify-center text-xs font-bold text-purple-200">
                            {idx + 1}
                          </div>
                          <span className="font-semibold text-purple-200">{step.agent}</span>
                        </div>
                        <div className="text-sm text-purple-100 ml-8">
                          <div className="font-medium">{step.action}</div>
                          <div className="text-xs text-purple-300 mt-1 italic">{step.reason}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Proactive Suggestions */}
              {message.data.suggestions && message.data.suggestions.length > 0 && (
                <div className="mt-4 pt-4 border-t border-white/20">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="w-6 h-6 rounded-full bg-yellow-500/30 flex items-center justify-center">
                      <span className="text-sm">💡</span>
                    </div>
                    <span className="text-sm font-semibold text-purple-200">You might also want to:</span>
                  </div>
                  <div className="grid grid-cols-1 gap-2">
                    {message.data.suggestions.map((suggestion, idx) => (
                      <button
                        key={idx}
                        onClick={() => onSuggestionClick && onSuggestionClick(suggestion.query)}
                        className="group relative w-full text-left bg-gradient-to-r from-purple-500/10 to-pink-500/10 hover:from-purple-500/20 hover:to-pink-500/20 rounded-xl px-4 py-3 text-sm text-purple-100 hover:text-white transition-all duration-300 border border-white/20 hover:border-white/40 cursor-pointer overflow-hidden"
                      >
                        <div className="flex items-center gap-3">
                          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-purple-400 to-pink-500 flex items-center justify-center text-white text-xs font-bold shadow-lg group-hover:scale-110 transition-transform">
                            {idx + 1}
                          </div>
                          <span className="flex-1 font-medium">{suggestion.text}</span>
                          <svg 
                            className="w-5 h-5 text-purple-300 group-hover:translate-x-1 transition-transform" 
                            fill="none" 
                            stroke="currentColor" 
                            viewBox="0 0 24 24"
                          >
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                          </svg>
                        </div>
                        <div className="absolute inset-0 bg-gradient-to-r from-purple-400/0 via-pink-400/0 to-purple-400/0 opacity-0 group-hover:opacity-20 transition-opacity duration-300" />
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
          
          <div className={`text-xs mt-2 flex items-center gap-1 ${
            isUser ? 'text-purple-200' : 'text-purple-300'
          }`}>
            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        </div>
      </div>
    </div>
  );
}

export default MessageBubble;
