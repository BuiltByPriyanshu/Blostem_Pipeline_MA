import { Link, useLocation } from 'react-router-dom';

export default function Sidebar() {
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <div className="w-[220px] bg-blostem-surface border-r border-blostem-border h-screen flex flex-col p-4 fixed left-0 top-0">
      <div className="flex items-center gap-2 mb-8">
        <div className="w-8 h-8 bg-blostem-purple rounded-lg flex items-center justify-center">
          <span className="text-white font-bold text-sm">⚡</span>
        </div>
        <span className="text-lg font-medium text-blostem-text">Blostem</span>
      </div>
      
      <nav className="flex flex-col gap-2">
        <Link
          to="/"
          className={`px-4 py-2 rounded-sm text-base transition ${
            isActive('/')
              ? 'bg-blostem-purple-light text-blostem-purple'
              : 'text-blostem-text hover:bg-blostem-surface'
          }`}
        >
          Pipeline
        </Link>
        <Link
          to="/activation"
          className={`px-4 py-2 rounded-sm text-base transition ${
            isActive('/activation')
              ? 'bg-blostem-purple-light text-blostem-purple'
              : 'text-blostem-text hover:bg-blostem-surface'
          }`}
        >
          Activation Tracker
        </Link>
        <Link
          to="/sequences"
          className={`px-4 py-2 rounded-sm text-base transition ${
            isActive('/sequences')
              ? 'bg-blostem-purple-light text-blostem-purple'
              : 'text-blostem-text hover:bg-blostem-surface'
          }`}
        >
          Sequence Viewer
        </Link>

        <div className="border-t border-blostem-border my-4"></div>

        <Link
          to="/activity"
          className={`px-4 py-2 rounded-sm text-base transition ${
            isActive('/activity')
              ? 'bg-blostem-purple-light text-blostem-purple'
              : 'text-blostem-text hover:bg-blostem-surface'
          }`}
        >
          Activity Feed
        </Link>
        <Link
          to="/email-history"
          className={`px-4 py-2 rounded-sm text-base transition ${
            isActive('/email-history')
              ? 'bg-blostem-purple-light text-blostem-purple'
              : 'text-blostem-text hover:bg-blostem-surface'
          }`}
        >
          Email History
        </Link>
      </nav>
    </div>
  );
}
