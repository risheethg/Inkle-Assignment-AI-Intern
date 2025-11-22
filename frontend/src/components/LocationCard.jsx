import { useState } from 'react';

function LocationCard({ location, onExplore }) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div 
      className="relative overflow-hidden rounded-xl bg-gradient-to-br from-purple-500/20 to-pink-500/20 backdrop-blur-sm border border-white/30 p-4 transition-all duration-300 hover:scale-[1.02] hover:shadow-xl group"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-to-br from-purple-400 to-pink-500 flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
          <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>
        <div className="flex-1">
          <div className="font-semibold text-purple-200 mb-1 flex items-center gap-2">
            <span>Location</span>
            <span className="text-xs bg-purple-500/30 px-2 py-1 rounded-full">Confirmed</span>
          </div>
          <div className="text-white text-lg font-bold mb-2">{location}</div>
          
          {isHovered && (
            <button
              onClick={() => onExplore && onExplore(location)}
              className="mt-2 px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg text-sm font-medium hover:from-purple-600 hover:to-pink-600 transition-all shadow-lg hover:shadow-purple-500/50 animate-fadeIn"
            >
              🗺️ Explore More
            </button>
          )}
        </div>
      </div>

      {/* Animated background */}
      <div className="absolute inset-0 bg-gradient-to-r from-purple-400/0 via-pink-400/0 to-purple-400/0 opacity-0 group-hover:opacity-20 transition-opacity duration-300 pointer-events-none" />
    </div>
  );
}

export default LocationCard;
