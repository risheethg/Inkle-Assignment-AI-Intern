import { useState, useEffect } from 'react';

function WelcomeModal() {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    // Check if user has seen the welcome modal before
    const hasSeenWelcome = localStorage.getItem('hasSeenWelcome');
    if (!hasSeenWelcome) {
      setIsOpen(true);
    }
  }, []);

  const handleClose = () => {
    localStorage.setItem('hasSeenWelcome', 'true');
    setIsOpen(false);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
      <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-purple-500/30">
        {/* Header */}
        <div className="sticky top-0 bg-gradient-to-r from-purple-600 to-pink-600 p-6 rounded-t-2xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-white/20 flex items-center justify-center">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white">Welcome to TravelMate AI! 🌍</h2>
                <p className="text-purple-100 text-sm">Your intelligent travel companion</p>
              </div>
            </div>
            <button
              onClick={handleClose}
              className="text-white/80 hover:text-white transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* What I Can Do */}
          <div>
            <h3 className="text-xl font-semibold text-purple-300 mb-3 flex items-center gap-2">
              <span className="text-2xl">✨</span>
              What I Can Do For You
            </h3>
            <div className="space-y-3">
              <FeatureItem 
                icon="🌤️"
                title="Real-Time Weather Updates"
                description="Get current temperature and precipitation forecasts for any location worldwide"
              />
              <FeatureItem 
                icon="🗺️"
                title="Discover Top Attractions"
                description="Find the best tourist spots, landmarks, and hidden gems in any city"
              />
              <FeatureItem 
                icon="📅"
                title="Multi-Day Trip Planning"
                description="Get complete itineraries with day-by-day schedules and time-optimized activities"
              />
              <FeatureItem 
                icon="🤖"
                title="Multi-Agent AI System"
                description="Powered by LangGraph with specialized Weather, Places, and Planning agents"
              />
              <FeatureItem 
                icon="💬"
                title="Conversational Memory"
                description="I remember your conversation context for more natural follow-up questions"
              />
              <FeatureItem 
                icon="💡"
                title="Smart Suggestions"
                description="Proactive follow-up suggestions based on your interests and queries"
              />
            </div>
          </div>

          {/* Example Queries */}
          <div className="bg-purple-500/10 rounded-xl p-4 border border-purple-500/20">
            <h3 className="text-lg font-semibold text-purple-300 mb-2 flex items-center gap-2">
              <span className="text-xl">💭</span>
              Try Asking Me:
            </h3>
            <ul className="space-y-2 text-purple-100 text-sm">
              <li className="flex items-start gap-2">
                <span className="text-purple-400 mt-0.5">•</span>
                <span>"What's the weather like in Paris?"</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-purple-400 mt-0.5">•</span>
                <span>"Show me the best places to visit in Tokyo"</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-purple-400 mt-0.5">•</span>
                <span>"Plan a 3-day trip to Bali"</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-purple-400 mt-0.5">•</span>
                <span>"Tell me more about the Eiffel Tower"</span>
              </li>
            </ul>
          </div>

          {/* Pro Tips */}
          <div className="bg-pink-500/10 rounded-xl p-4 border border-pink-500/20">
            <h3 className="text-lg font-semibold text-pink-300 mb-2 flex items-center gap-2">
              <span className="text-xl">🎯</span>
              Pro Tips:
            </h3>
            <ul className="space-y-2 text-pink-100 text-sm">
              <li className="flex items-start gap-2">
                <span className="text-pink-400 mt-0.5">✓</span>
                <span>Watch the <strong>thinking process</strong> dropdown to see how I analyze your queries</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-pink-400 mt-0.5">✓</span>
                <span>Click on <strong>suggestion buttons</strong> for quick follow-up questions</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-pink-400 mt-0.5">✓</span>
                <span>Use <strong>"Learn More"</strong> buttons on places to get detailed information</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-pink-400 mt-0.5">✓</span>
                <span>I maintain context - feel free to ask follow-up questions naturally</span>
              </li>
            </ul>
          </div>

          {/* CTA Button */}
          <button
            onClick={handleClose}
            className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-[1.02]"
          >
            Let's Start Exploring! 🚀
          </button>
        </div>
      </div>
    </div>
  );
}

function FeatureItem({ icon, title, description }) {
  return (
    <div className="flex items-start gap-3 p-3 rounded-lg bg-slate-800/50 border border-slate-700/50 hover:border-purple-500/30 transition-colors">
      <span className="text-2xl flex-shrink-0">{icon}</span>
      <div>
        <h4 className="font-semibold text-white text-sm">{title}</h4>
        <p className="text-slate-300 text-xs mt-0.5">{description}</p>
      </div>
    </div>
  );
}

export default WelcomeModal;
