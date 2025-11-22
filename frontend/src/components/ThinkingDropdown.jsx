import { useState, useEffect } from 'react';

function ThinkingDropdown({ reasoningSteps, isComplete }) {
  const [isExpanded, setIsExpanded] = useState(true);
  const [animatedSteps, setAnimatedSteps] = useState([]);

  useEffect(() => {
    // Animate new steps as they come in
    if (reasoningSteps.length > animatedSteps.length) {
      const newSteps = reasoningSteps.slice(animatedSteps.length);
      newSteps.forEach((step, index) => {
        setTimeout(() => {
          setAnimatedSteps(prev => [...prev, step]);
        }, index * 100);
      });
    }
  }, [reasoningSteps]);

  if (animatedSteps.length === 0) return null;

  return (
    <div className="mb-4">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center gap-2 text-sm font-medium text-purple-200 hover:text-purple-100 transition-colors w-full"
      >
        <div className="flex items-center gap-2 flex-1">
          <div className={`transition-transform duration-200 ${isExpanded ? 'rotate-90' : ''}`}>
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </div>
          <div className="flex items-center gap-2">
            {!isComplete && (
              <div className="w-4 h-4 border-2 border-purple-300 border-t-transparent rounded-full animate-spin" />
            )}
            <span>
              {isComplete ? '✓ Thinking complete' : 'Thinking...'}
            </span>
            <span className="text-purple-300">({animatedSteps.length} steps)</span>
          </div>
        </div>
      </button>

      {isExpanded && (
        <div className="mt-3 space-y-2 animate-fadeIn">
          {animatedSteps.map((step, idx) => (
            <div
              key={idx}
              className="flex items-start gap-3 bg-white/5 rounded-lg p-3 border border-white/10 animate-slideIn"
              style={{ animationDelay: `${idx * 50}ms` }}
            >
              <div className="flex-shrink-0">
                {idx < animatedSteps.length - 1 || isComplete ? (
                  <div className="w-6 h-6 rounded-full bg-purple-500/30 flex items-center justify-center">
                    <svg className="w-4 h-4 text-purple-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                ) : (
                  <div className="w-6 h-6 rounded-full bg-purple-500/30 flex items-center justify-center">
                    <div className="w-3 h-3 bg-purple-400 rounded-full animate-pulse" />
                  </div>
                )}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-semibold text-purple-200 text-sm">{step.agent}</span>
                </div>
                <div className="text-sm text-purple-100">{step.action}</div>
                <div className="text-xs text-purple-300 mt-1 italic">{step.reason}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ThinkingDropdown;
