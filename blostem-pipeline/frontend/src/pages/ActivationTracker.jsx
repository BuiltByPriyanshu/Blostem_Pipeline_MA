import { useState } from 'react';
import { useActivation } from '../hooks/useActivation';
import PartnerRow from '../components/PartnerRow';
import MetricCard from '../components/MetricCard';

export default function ActivationTracker() {
  const { partners, loading, error, reengage, refetch } = useActivation();
  const [filterStatus, setFilterStatus] = useState('all');
  const [expandedId, setExpandedId] = useState(null);

  let filtered = partners;
  if (filterStatus === 'stalled') {
    filtered = partners.filter(p => p.status === 'stalled');
  } else if (filterStatus === 'active') {
    filtered = partners.filter(p => p.status === 'active');
  }

  const activeCount = partners.filter(p => p.status === 'active').length;
  const stalledCount = partners.filter(p => p.status === 'stalled' || p.status === 'critical').length;
  const avgActivation = partners.length > 0 ? Math.round(partners.reduce((sum, p) => sum + p.activation_pct, 0) / partners.length) : 0;
  const reengagementSent = 0; // Would track from DB

  const handleReengage = async (partnerId) => {
    try {
      const result = await reengage(partnerId);
      alert('Re-engagement email generated!');
      refetch();
    } catch (err) {
      alert('Error generating re-engagement email');
    }
  };

  if (loading) return <div className="p-8 text-blostem-text-muted">Loading...</div>;
  if (error) return <div className="p-8 text-blostem-red">Error: {error}</div>;

  return (
    <div className="ml-[220px] p-8 min-h-screen bg-blostem-bg">
      <div className="mb-8">
        <h1 className="text-xl font-medium text-blostem-text mb-1">Activation tracker</h1>
        <p className="text-sm text-blostem-text-muted">Signed partners · post-onboarding health</p>
      </div>

      <div className="grid grid-cols-4 gap-3 mb-8">
        <MetricCard label="Active" value={activeCount} />
        <MetricCard label="Stalled" value={stalledCount} />
        <MetricCard label="Avg activation %" value={avgActivation} />
        <MetricCard label="Re-engagement sent" value={reengagementSent} />
      </div>

      <div className="flex gap-2 mb-6">
        {['all', 'stalled', 'active'].map(status => (
          <button
            key={status}
            onClick={() => setFilterStatus(status)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition ${
              filterStatus === status
                ? 'bg-blostem-purple text-white'
                : 'bg-blostem-surface text-blostem-text border border-blostem-border'
            }`}
          >
            {status.charAt(0).toUpperCase() + status.slice(1)}
          </button>
        ))}
      </div>

      <div className="bg-white border border-blostem-border rounded-lg overflow-hidden">
        {filtered.map(partner => (
          <PartnerRow
            key={partner.id}
            partner={partner}
            isExpanded={expandedId === partner.id}
            onExpand={(id) => setExpandedId(expandedId === id ? null : id)}
            onReengage={handleReengage}
          />
        ))}
      </div>
    </div>
  );
}
