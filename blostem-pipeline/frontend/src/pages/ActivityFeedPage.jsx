import { useState, useEffect } from 'react';
import ActivityFeed from '../components/ActivityFeed';

const ACTION_TYPES = [
  { value: '', label: 'All actions' },
  { value: 'email_sent', label: 'Emails sent' },
  { value: 'sequence_generated', label: 'Sequences generated' },
  { value: 'compliance_checked', label: 'Compliance checks' },
  { value: 'prospect_viewed', label: 'Prospects viewed' },
  { value: 'sequence_viewed', label: 'Sequences viewed' },
];

export default function ActivityFeedPage() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionType, setActionType] = useState('');
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(0);
  const [total, setTotal] = useState(0);
  const [stats, setStats] = useState(null);

  const limit = 20;

  useEffect(() => {
    fetchActivities();
    fetchStats();
    const interval = setInterval(fetchActivities, 30000); // Auto-refresh every 30s
    return () => clearInterval(interval);
  }, [actionType, search, page]);

  const fetchActivities = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({
        limit,
        offset: page * limit,
      });
      if (actionType) params.append('action_type', actionType);
      if (search) params.append('search', search);

      const res = await fetch(`/api/activity/feed?${params}`);
      if (res.ok) {
        const data = await res.json();
        setActivities(data.items);
        setTotal(data.total);
      } else {
        setError('Failed to load activities');
      }
    } catch (err) {
      setError('Error loading activities');
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const res = await fetch('/api/activity/stats');
      if (res.ok) {
        const data = await res.json();
        setStats(data);
      }
    } catch (err) {
      console.error('Error loading stats:', err);
    }
  };

  const handleRefresh = () => {
    setPage(0);
    fetchActivities();
    fetchStats();
  };

  const totalPages = Math.ceil(total / limit);

  return (
    <div className="ml-[220px] p-8 min-h-screen bg-blostem-bg">
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-xl font-medium text-blostem-text mb-1">Activity feed</h1>
            <p className="text-sm text-blostem-text-muted">All system actions and events</p>
          </div>
          <button
            onClick={handleRefresh}
            className="px-4 py-2 bg-blostem-purple text-white rounded-md font-medium hover:opacity-90 transition"
          >
            Refresh
          </button>
        </div>

        {stats && (
          <div className="grid grid-cols-4 gap-4 mb-6">
            <div className="bg-white border border-blostem-border rounded-lg p-4">
              <p className="text-xs text-blostem-text-muted mb-1">Total actions</p>
              <p className="text-2xl font-medium text-blostem-text">{stats.total_actions}</p>
            </div>
            <div className="bg-white border border-blostem-border rounded-lg p-4">
              <p className="text-xs text-blostem-text-muted mb-1">Today</p>
              <p className="text-2xl font-medium text-blostem-text">{stats.actions_today}</p>
            </div>
            <div className="bg-white border border-blostem-border rounded-lg p-4">
              <p className="text-xs text-blostem-text-muted mb-1">Emails sent</p>
              <p className="text-2xl font-medium text-blostem-text">{stats.emails_sent}</p>
            </div>
            <div className="bg-white border border-blostem-border rounded-lg p-4">
              <p className="text-xs text-blostem-text-muted mb-1">Sequences</p>
              <p className="text-2xl font-medium text-blostem-text">{stats.sequences_generated}</p>
            </div>
          </div>
        )}
      </div>

      <div className="mb-6 flex gap-4">
        <select
          value={actionType}
          onChange={(e) => {
            setActionType(e.target.value);
            setPage(0);
          }}
          className="px-4 py-2 border border-blostem-border rounded-md text-base bg-white text-blostem-text"
        >
          {ACTION_TYPES.map((type) => (
            <option key={type.value} value={type.value}>
              {type.label}
            </option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Search activities..."
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setPage(0);
          }}
          className="flex-1 px-4 py-2 border border-blostem-border rounded-md text-base bg-white text-blostem-text placeholder-blostem-text-muted"
        />
      </div>

      {loading && <div className="text-center py-8 text-blostem-text-muted">Loading...</div>}
      {error && <div className="text-center py-8 text-blostem-red">{error}</div>}

      {!loading && !error && (
        <>
          <ActivityFeed actions={activities} limit={limit} />

          {totalPages > 1 && (
            <div className="mt-6 flex items-center justify-between">
              <p className="text-sm text-blostem-text-muted">
                Showing {page * limit + 1} to {Math.min((page + 1) * limit, total)} of {total}
              </p>
              <div className="flex gap-2">
                <button
                  onClick={() => setPage(Math.max(0, page - 1))}
                  disabled={page === 0}
                  className="px-4 py-2 border border-blostem-border rounded-md text-blostem-text hover:bg-blostem-surface transition disabled:opacity-50"
                >
                  Previous
                </button>
                <div className="flex items-center gap-2">
                  {Array.from({ length: Math.min(5, totalPages) }).map((_, i) => {
                    const pageNum = i;
                    return (
                      <button
                        key={pageNum}
                        onClick={() => setPage(pageNum)}
                        className={`px-3 py-2 rounded-md transition ${
                          page === pageNum
                            ? 'bg-blostem-purple text-white'
                            : 'border border-blostem-border text-blostem-text hover:bg-blostem-surface'
                        }`}
                      >
                        {pageNum + 1}
                      </button>
                    );
                  })}
                </div>
                <button
                  onClick={() => setPage(Math.min(totalPages - 1, page + 1))}
                  disabled={page >= totalPages - 1}
                  className="px-4 py-2 border border-blostem-border rounded-md text-blostem-text hover:bg-blostem-surface transition disabled:opacity-50"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
