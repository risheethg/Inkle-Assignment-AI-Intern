import { useState } from 'react';

function WeatherCard({ weatherInfo }) {
  const [showDetails, setShowDetails] = useState(false);

  // Parse weather info to extract temperature if present
  const hasTemperature = weatherInfo && /\d+°[CF]/.test(weatherInfo);

  return (
    <div className="relative overflow-hidden rounded-xl bg-gradient-to-br from-blue-500/20 to-cyan-500/20 backdrop-blur-sm border border-white/30 p-4 transition-all duration-300 hover:scale-[1.01] hover:shadow-xl group">
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-to-br from-blue-400 to-cyan-500 flex items-center justify-center shadow-lg">
          <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
          </svg>
        </div>
        <div className="flex-1">
          <div className="font-semibold text-blue-200 mb-1 flex items-center gap-2">
            <span>Weather Information</span>
            {hasTemperature && (
              <span className="text-xs bg-blue-500/30 px-2 py-1 rounded-full">Live Data</span>
            )}
          </div>
          <div className="text-blue-100 text-sm leading-relaxed">{weatherInfo}</div>
          
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="mt-3 text-xs text-blue-300 hover:text-blue-200 flex items-center gap-1 transition-colors"
          >
            <svg className={`w-4 h-4 transition-transform ${showDetails ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
            <span>{showDetails ? 'Hide' : 'Show'} Details</span>
          </button>

          {showDetails && (
            <div className="mt-3 p-3 bg-white/10 rounded-lg animate-fadeIn space-y-2">
              <div className="text-xs text-blue-200">
                <div className="flex items-center gap-2 mb-1">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span className="font-semibold">Weather Tips:</span>
                </div>
                <ul className="ml-6 space-y-1 text-blue-100">
                  <li>• Check hourly forecasts for better planning</li>
                  <li>• Pack appropriate clothing for the weather</li>
                  <li>• Plan indoor alternatives for rainy days</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Animated background gradient on hover */}
      <div className="absolute inset-0 bg-gradient-to-r from-blue-400/0 via-cyan-400/0 to-blue-400/0 opacity-0 group-hover:opacity-20 transition-opacity duration-300 pointer-events-none" />
    </div>
  );
}

export default WeatherCard;
