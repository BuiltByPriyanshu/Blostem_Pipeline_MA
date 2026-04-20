import { useState } from 'react';
import StakeholderMap from './StakeholderMap';
import IntentSignals from './IntentSignals';

export default function ProspectDetail({ prospect }) {
  const [activeTab, setActiveTab] = useState('stakeholders');

  return (
    <div className="bg-blostem-surface border-b border-blostem-border p-4">
      <div className="flex gap-4 mb-4 border-b border-blostem-border pb-3">
        <button
          onClick={() => setActiveTab('stakeholders')}
          className={`text-base font-medium pb-2 border-b-2 transition ${
            activeTab === 'stakeholders'
              ? 'border-blostem-purple text-blostem-purple'
              : 'border-transparent text-blostem-text-secondary'
          }`}
        >
          Stakeholder map
        </button>
        <button
          onClick={() => setActiveTab('signals')}
          className={`text-base font-medium pb-2 border-b-2 transition ${
            activeTab === 'signals'
              ? 'border-blostem-purple text-blostem-purple'
              : 'border-transparent text-blostem-text-secondary'
          }`}
        >
          Intent signals
        </button>
      </div>

      {activeTab === 'stakeholders' && <StakeholderMap prospect={prospect} />}
      {activeTab === 'signals' && <IntentSignals prospect={prospect} />}
    </div>
  );
}
