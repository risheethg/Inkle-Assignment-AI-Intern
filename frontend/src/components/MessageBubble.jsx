function MessageBubble({ message }) {
  const isUser = message.role === 'user';
  const isError = message.isError;

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          isUser
            ? 'bg-indigo-600 text-white'
            : isError
            ? 'bg-red-100 text-red-800 border border-red-300'
            : 'bg-gray-100 text-gray-800'
        }`}
      >
        <div className="whitespace-pre-wrap break-words">
          {message.content}
        </div>
        
        {/* Show structured data for assistant responses */}
        {!isUser && !isError && message.data && (
          <div className="mt-3 pt-3 border-t border-gray-200 text-sm">
            {message.data.location && (
              <div className="mb-2">
                <span className="font-semibold">Location:</span>{' '}
                <span className="text-gray-600">{message.data.location}</span>
              </div>
            )}
            
            {message.data.weather_info && (
              <div className="mb-2">
                <span className="font-semibold">Weather:</span>{' '}
                <span className="text-gray-600">{message.data.weather_info}</span>
              </div>
            )}
            
            {message.data.places_info && message.data.places_info.length > 0 && (
              <div>
                <span className="font-semibold">Places to visit:</span>
                <ul className="list-disc list-inside mt-1 text-gray-600">
                  {message.data.places_info.map((place, idx) => (
                    <li key={idx}>{place}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
        
        <div className={`text-xs mt-2 ${isUser ? 'text-indigo-200' : 'text-gray-500'}`}>
          {message.timestamp.toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}

export default MessageBubble;
