import { useState, useEffect } from 'react';
import StatusBadge from '../components/StatusBadge';

export default function EmailHistoryPage() {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState('');
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(0);
  const [total, setTotal] = useState(0);
  const [sortBy, setSortBy] = useState('sent_at');
  const [sortOrder, setSortOrder] = useState('desc');
  const [selectedEmail, setSelectedEmail] = useState(null);

  const limit = 20;

  useEffect(() => {
    fetchEmails();
  }, [status, search, page, sortBy, sortOrder]);

  const fetchEmails = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({
        limit,
        offset: page * limit,
        sort_by: sortBy,
        sort_order: sortOrder,
      });
      if (status) params.append('status', status);
      if (search) params.append('search', search);

      const res = await fetch(`/api/email/history?${params}`);
      if (res.ok) {
        const data = await res.json();
        setEmails(data.items);
        setTotal(data.total);
      } else {
        setError('Failed to load email history');
      }
    } catch (err) {
      setError('Error loading email history');
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = async (emailId) => {
    try {
      const res = await fetch(`/api/email/retry/${emailId}`, { method: 'POST' });
      if (res.ok) {
        alert('Email resent successfully');
        fetchEmails();
      } else {
        alert('Failed to resend email');
      }
    } catch (err) {
      alert('Error resending email');
    }
  };

  const totalPages = Math.ceil(total / limit);

  return (
    <div className="ml-[220px] p-8 min-h-screen bg-blostem-bg">
      <div className="mb-8">
        <h1 className="text-xl font-medium text-blostem-text mb-1">Email history</h1>
        <p className="text-sm text-blostem-text-muted">All sent emails and delivery status</p>
      </div>

      <div className="mb-6 flex gap-4">
        <select
          value={status}
          onChange={(e) => {
            setStatus(e.target.value);
            setPage(0);
          }}
          className="px-4 py-2 border border-blostem-border rounded-md text-base bg-white text-blostem-text"
        >
          <option value="">All statuses</option>
          <option value="success">Sent successfully</option>
          <option value="failed">Failed</option>
        </select>

        <input
          type="text"
          placeholder="Search by email or subject..."
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
          <div className="bg-white border border-blostem-border rounded-lg overflow-hidden">
            <table className="w-full">
              <thead className="bg-blostem-surface border-b border-blostem-border">
                <tr>
                  <th className="px-4 py-3 text-left text-sm font-medium text-blostem-text">
                    Recipient
                  </th>
                  <th className="px-4 py-3 text-left text-sm font-medium text-blostem-text">
                    Subject
                  </th>
                  <th className="px-4 py-3 text-left text-sm font-medium text-blostem-text">
                    Status
                  </th>
                  <th className="px-4 py-3 text-left text-sm font-medium text-blostem-text">
                    Sent at
                  </th>
                  <th className="px-4 py-3 text-left text-sm font-medium text-blostem-text">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                {emails.map((email) => (
                  <tr key={email.id} className="border-b border-blostem-border hover:bg-blostem-surface transition">
                    <td className="px-4 py-3 text-sm text-blostem-text">{email.to_email}</td>
                    <td className="px-4 py-3 text-sm text-blostem-text truncate max-w-xs">
                      {email.subject}
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <StatusBadge
                        status={email.success ? 'passed' : 'failed'}
                        type="compliance"
                      />
                    </td>
                    <td className="px-4 py-3 text-sm text-blostem-text-muted">
                      {new Date(email.sent_at).toLocaleDateString()} {new Date(email.sent_at).toLocaleTimeString()}
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <div className="flex gap-2">
                        <button
                          onClick={() => setSelectedEmail(email)}
                          className="px-3 py-1 text-xs bg-blostem-blue text-white rounded hover:opacity-90 transition"
                        >
                          View
                        </button>
                        {!email.success && (
                          <button
                            onClick={() => handleRetry(email.id)}
                            className="px-3 py-1 text-xs bg-blostem-amber-light text-blostem-amber-text rounded hover:opacity-90 transition"
                          >
                            Retry
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {emails.length === 0 && (
              <div className="text-center py-8 text-blostem-text-muted">
                No emails found
              </div>
            )}
          </div>

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

      {selectedEmail && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-medium text-blostem-text">Email details</h2>
              <button
                onClick={() => setSelectedEmail(null)}
                className="text-blostem-text-muted hover:text-blostem-text"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <p className="text-xs text-blostem-text-muted mb-1">To</p>
                <p className="text-sm text-blostem-text">{selectedEmail.to_email}</p>
              </div>

              <div>
                <p className="text-xs text-blostem-text-muted mb-1">Subject</p>
                <p className="text-sm text-blostem-text">{selectedEmail.subject}</p>
              </div>

              <div>
                <p className="text-xs text-blostem-text-muted mb-1">Status</p>
                <StatusBadge
                  status={selectedEmail.success ? 'passed' : 'failed'}
                  type="compliance"
                />
              </div>

              <div>
                <p className="text-xs text-blostem-text-muted mb-1">Sent at</p>
                <p className="text-sm text-blostem-text">
                  {new Date(selectedEmail.sent_at).toLocaleString()}
                </p>
              </div>

              {selectedEmail.resend_id && (
                <div>
                  <p className="text-xs text-blostem-text-muted mb-1">Resend ID</p>
                  <p className="text-sm text-blostem-text font-mono">{selectedEmail.resend_id}</p>
                </div>
              )}

              <div>
                <p className="text-xs text-blostem-text-muted mb-1">Preview</p>
                <div className="bg-blostem-surface p-3 rounded-md text-sm text-blostem-text whitespace-pre-wrap">
                  {selectedEmail.body_snippet}
                </div>
              </div>
            </div>

            <div className="mt-6 flex gap-2">
              {!selectedEmail.success && (
                <button
                  onClick={() => {
                    handleRetry(selectedEmail.id);
                    setSelectedEmail(null);
                  }}
                  className="flex-1 px-4 py-2 bg-blostem-amber-light text-blostem-amber-text rounded-md font-medium hover:opacity-90 transition"
                >
                  Retry send
                </button>
              )}
              <button
                onClick={() => setSelectedEmail(null)}
                className="flex-1 px-4 py-2 border border-blostem-border text-blostem-text rounded-md font-medium hover:bg-blostem-surface transition"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
