import { useState } from 'react';
import StatusBadge from './StatusBadge';
import SparkLine from './SparkLine';
import { formatDaysAgo } from '../utils/formatters';

export default function PartnerRow({ partner, onExpand, isExpanded, onReengage }) {
  const [reengagingId, setReengagingId] = useState(null);

  const handleReengage = async () => {
    setReengagingId(partner.id);
    try {
      await onReengage(partner.id);
    } finally {
      setReengagingId(null);
    }
  };

  return (
    <div>
      <div
        onClick={() => onExpand(partner.id)}
        className="border-b border-blostem-border hover:bg-blostem-surface cursor-pointer transition p-4"
      >
        <div className="grid grid-cols-6 gap-4 items-center">
          <div>
            <div className="font-medium text-blostem-text">{partner.name}</div>
            <div className="text-sm text-blostem-text-muted">{partner.contact_name} · {partner.contact_role}</div>
          </div>
          <div className="text-sm text-blostem-text">{partner.signed_at}</div>
          <div>
            <div className="text-sm text-blostem-text">{formatDaysAgo(partner.days_silent)}</div>
            {partner.days_silent > 0 && (
              <div className="text-xs text-blostem-red">{partner.days_silent}d silent</div>
            )}
          </div>
          <div className="flex items-center gap-2">
            <div className="flex-1 h-1.5 bg-blostem-border rounded-sm overflow-hidden">
              <div
                className="h-full bg-blostem-green rounded-sm"
                style={{ width: `${partner.activation_pct}%` }}
              />
            </div>
            <div className="text-sm font-medium text-blostem-text w-12 text-right">{partner.activation_pct}%</div>
          </div>
          <div>
            <StatusBadge status={partner.status} />
          </div>
          <div className="flex items-center justify-between">
            <SparkLine data={partner.api_call_trend} status={partner.status} />
            {partner.status === 'active' ? (
              <span className="text-sm text-blostem-text-muted">—</span>
            ) : (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleReengage();
                }}
                disabled={reengagingId === partner.id}
                className="text-sm text-blostem-purple font-medium hover:opacity-80 transition"
              >
                {reengagingId === partner.id ? 'Generating...' : 'Re-engage'}
              </button>
            )}
          </div>
        </div>
      </div>

      {isExpanded && (
        <div className="bg-blostem-surface border-b border-blostem-border p-4">
          <div className="text-sm text-blostem-text-muted mb-4">
            {partner.milestones.filter(m => m.done).length} of {partner.milestones.length} milestones complete
          </div>
          <div className="space-y-3">
            {partner.milestones.map((m, idx) => (
              <div key={idx} className="flex items-center gap-3">
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: m.done ? '#639922' : '#D3D1C7' }}
                />
                <div className="text-sm text-blostem-text">{m.label}</div>
              </div>
            ))}
          </div>
          {partner.status !== 'active' && (
            <div className="mt-4 p-3 rounded-md" style={{ backgroundColor: partner.status === 'critical' ? '#FCEBEB' : '#FAEEDA' }}>
              <div className="text-sm font-medium" style={{ color: partner.status === 'critical' ? '#791F1F' : '#633806' }}>
                Stall detected: {partner.stall_reason}
              </div>
              <div className="text-sm mt-1" style={{ color: partner.status === 'critical' ? '#791F1F' : '#633806' }}>
                {partner.recommendation}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
