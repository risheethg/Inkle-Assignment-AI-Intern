function LoadingDots() {
  return (
    <div className="flex items-center space-x-3">
      <div className="w-3 h-3 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full animate-bounce shadow-lg" style={{ animationDelay: '0s' }}></div>
      <div className="w-3 h-3 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full animate-bounce shadow-lg" style={{ animationDelay: '0.15s' }}></div>
      <div className="w-3 h-3 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full animate-bounce shadow-lg" style={{ animationDelay: '0.3s' }}></div>
      <span className="text-purple-200 text-sm ml-2">Thinking</span>
    </div>
  );
}

export default LoadingDots;
