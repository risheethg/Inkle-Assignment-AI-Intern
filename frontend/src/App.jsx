import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
  return (
    <div className="fixed inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmZmZmYiIGZpbGwtb3BhY2l0eT0iMC4wNSI+PHBhdGggZD0iTTM2IDE0YzIuMjEgMCA0IDEuNzkgNCA0cy0xLjc5IDQtNCA0LTQtMS43OS00LTQgMS43OS00IDQtNHptMC0yYy0zLjMxIDAtNiAyLjY5LTYgNnMyLjY5IDYgNiA2IDYtMi42OSA2LTYtMi42OS02LTYtNnoiLz48L2c+PC9nPjwvc3ZnPg==')] opacity-40"></div>
      
      <div className="relative z-10 h-full w-full flex flex-col">
        <header className="flex-shrink-0 text-center py-3 px-4">
          <div className="inline-flex items-center gap-2 mb-1">
            <div className="w-10 h-10 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 flex items-center justify-center shadow-lg">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h1 className="text-3xl md:text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-400 to-purple-400">
              TravelMate AI
            </h1>
          </div>
          <p className="text-purple-200 text-sm md:text-base">
            Your intelligent travel companion for weather insights and destination discoveries
          </p>
        </header>
        
        <div className="flex-1 w-full overflow-hidden px-4 pb-4">
          <ChatInterface />
        </div>
      </div>
    </div>
  );
}

export default App;
