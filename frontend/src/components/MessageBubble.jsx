function MessageBubble({ message }) {
  const isUser = message.role === 'user';
  const isError = message.isError;

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
          
          {/* Show structured data for assistant responses */}
          {!isUser && !isError && message.data && (
            <div className="mt-4 pt-4 border-t border-white/20 space-y-3">
              {message.data.location && (
                <div className="flex items-start gap-2">
                  <svg className="w-5 h-5 text-purple-300 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <div>
                    <span className="font-semibold text-purple-200">Location:</span>{' '}
                    <span className="text-purple-100">{message.data.location}</span>
                  </div>
                </div>
              )}
              
              {message.data.weather_info && (
                <div className="flex items-start gap-2">
                  <svg className="w-5 h-5 text-blue-300 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
                  </svg>
                  <div>
                    <span className="font-semibold text-blue-200">Weather:</span>{' '}
                    <span className="text-blue-100">{message.data.weather_info}</span>
                  </div>
                </div>
              )}
              
              {message.data.places_info && message.data.places_info.length > 0 && (
                <div className="flex items-start gap-2">
                  <svg className="w-5 h-5 text-pink-300 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                  <div className="flex-1">
                    <span className="font-semibold text-pink-200 block mb-2">Top Attractions:</span>
                    <div className="space-y-1.5">
                      {message.data.places_info.map((place, idx) => (
                        <div key={idx} className="flex items-center gap-2 text-pink-100 bg-white/10 rounded-lg px-3 py-1.5">
                          <span className="text-pink-300 font-bold text-sm">{idx + 1}.</span>
                          <span>{place}</span>
                        </div>
                      ))}
                    </div>
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
                  <div className="text-sm font-semibold text-purple-200 mb-2">💡 You might also want to:</div>
                  <div className="space-y-2">
                    {message.data.suggestions.map((suggestion, idx) => (
                      <button
                        key={idx}
                        onClick={() => {
                          const input = document.querySelector('textarea[placeholder]');
                          if (input) {
                            input.value = suggestion.query;
                            input.focus();
                            // Trigger form submission
                            const form = input.closest('form');
                            if (form) {
                              const event = new Event('submit', { bubbles: true, cancelable: true });
                              form.dispatchEvent(event);
                            }
                          }
                        }}
                        className="w-full text-left bg-white/10 hover:bg-white/20 rounded-lg px-3 py-2 text-sm text-purple-100 hover:text-white transition-all border border-white/20 hover:border-white/40"
                      >
                        {suggestion.text}
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
