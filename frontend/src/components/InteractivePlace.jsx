import { useState } from 'react';

function InteractivePlace({ place, index, onLearnMore }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      className={`group relative overflow-hidden rounded-xl transition-all duration-300 ${
        isHovered ? 'scale-[1.02] shadow-xl' : 'scale-100'
      }`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div
        className={`bg-gradient-to-br from-pink-500/20 to-purple-500/20 backdrop-blur-sm border border-white/30 p-4 cursor-pointer transition-all duration-300 ${
          isExpanded ? 'pb-6' : ''
        }`}
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-start gap-3 flex-1">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-pink-400 to-purple-500 flex items-center justify-center text-white font-bold shadow-lg">
              {index + 1}
            </div>
            <div className="flex-1">
              <div className="font-semibold text-white text-base mb-1">{place}</div>
              {isExpanded && (
                <div className="mt-3 space-y-2 animate-fadeIn">
                  <p className="text-sm text-purple-200 italic">
                    Click "Learn More" to discover details about this attraction!
                  </p>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onLearnMore && onLearnMore(place);
                    }}
                    className="mt-2 px-4 py-2 bg-gradient-to-r from-pink-500 to-purple-500 text-white rounded-lg text-sm font-medium hover:from-pink-600 hover:to-purple-600 transition-all shadow-lg hover:shadow-pink-500/50"
                  >
                    🔍 Learn More
                  </button>
                </div>
              )}
            </div>
          </div>
          <svg
            className={`w-5 h-5 text-purple-300 transition-transform duration-300 flex-shrink-0 ${
              isExpanded ? 'rotate-180' : 'rotate-0'
            }`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>
      
      {/* Hover effect border */}
      <div
        className={`absolute inset-0 pointer-events-none border-2 border-pink-400/0 rounded-xl transition-all duration-300 ${
          isHovered ? 'border-pink-400/50' : ''
        }`}
      />
    </div>
  );
}

export default InteractivePlace;
