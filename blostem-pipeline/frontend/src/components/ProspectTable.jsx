import { useState } from 'react';
import IntentScoreBar from './IntentScoreBar';
import StatusBadge from './StatusBadge';
import ProspectDetail from './ProspectDetail';
import { formatFunding } from '../utils/formatters';

export default function ProspectTable({ prospects }) {
  const [expandedId, setExpandedId] = useState(null);

  return (
    <div className="space-y-0">
      {prospects.map((prospect) => (
        <div key={prospect.id}>
          <div
            onClick={() => setExpandedId(expandedId === prospect.id ? null : prospect.id)}
            className="border-b border-blostem-border hover:bg-blostem-surface cursor-pointer transition p-4"
          >
            <div className="grid grid-cols-5 gap-4 items-center">
              <div>
                <div className="font-medium text-blostem-text">{prospect.name}</div>
                <div className="text-sm text-blostem-text-muted">{prospect.hq_city} · {formatFunding(prospect.funding_usd)}</div>
              </div>
              <div>
                <div
                  className="px-2 py-0.5 rounded-full text-xs font-medium inline-block"
                  style={{ backgroundColor: '#E6F1FB', color: '#0C447C' }}
                >
                  {prospect.stage}
                </div>
              </div>
              <div className="text-sm text-blostem-text-muted">{prospect.industry}</div>
              <div>
                <IntentScoreBar score={prospect.score} />
              </div>
              <div className="flex gap-2 justify-end">
                <StatusBadge status={prospect.compliance} type="compliance" />
                {prospect.seq_ready && (
                  <div
                    className="px-2 py-0.5 rounded-full text-xs font-medium"
                    style={{ backgroundColor: '#EEEDFE', color: '#3C3489' }}
                  >
                    Ready
                  </div>
                )}
              </div>
            </div>
          </div>

          {expandedId === prospect.id && (
            <ProspectDetail prospect={prospect} />
          )}
        </div>
      ))}
    </div>
  );
}
