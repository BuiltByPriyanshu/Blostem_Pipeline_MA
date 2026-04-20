import { useState, useEffect } from 'react';
import { useProspects } from '../hooks/useProspects';
import StatusBadge from '../components/StatusBadge';
import EmailSendButton from '../components/EmailSendButton';

const PERSONAS = ['CTO', 'CFO', 'Head of Compliance', 'Head of Product'];

export default function SequenceViewer() {
  const { prospects, loading, error } = useProspects();
  const [selectedProspectId, setSelectedProspectId] = useState(null);
  const [activePersona, setActivePersona] = useState('CTO');
  const [sequences, setSequences] = useState({});
  const [generatingPersona, setGeneratingPersona] = useState(null);

  const selectedProspect = prospects.find(p => p.id === selectedProspectId);

  const handleGenerateSequence = async (persona) => {
    if (!selectedProspectId) return;
    setGeneratingPersona(persona);
    try {
      const res = await fetch('/api/sequences/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prospect_id: selectedProspectId, persona }),
      });
      if (res.ok) {
        const data = await res.json();
        setSequences(prev => ({
          ...prev,
          [persona]: data,
        }));
      }
    } catch (err) {
      alert('Error generating sequence');
    } finally {
      setGeneratingPersona(null);
    }
  };

  if (loading) return <div className="p-8 text-blostem-text-muted">Loading...</div>;
  if (error) return <div className="p-8 text-blostem-red">Error: {error}</div>;

  return (
    <div className="ml-[220px] p-8 min-h-screen bg-blostem-bg">
      <div className="mb-8">
        <h1 className="text-xl font-medium text-blostem-text mb-1">Outreach sequences</h1>
        <p className="text-sm text-blostem-text-muted">AI-generated · compliance-checked</p>
      </div>

      <div className="mb-8">
        <select
          value={selectedProspectId || ''}
          onChange={(e) => {
            setSelectedProspectId(parseInt(e.target.value) || null);
            setSequences({});
          }}
          className="px-4 py-2 border border-blostem-border rounded-md text-base bg-white text-blostem-text"
        >
          <option value="">Select a prospect...</option>
          {prospects.map(p => (
            <option key={p.id} value={p.id}>{p.name}</option>
          ))}
        </select>
      </div>

      {selectedProspect && (
        <div>
          <div className="mb-6 flex items-center gap-4">
            <div>
              <div className="text-lg font-medium text-blostem-text">{selectedProspect.name}</div>
              <div className="text-sm text-blostem-text-muted">{selectedProspect.stage} · {selectedProspect.industry}</div>
            </div>
            <StatusBadge status={selectedProspect.compliance} type="compliance" />
          </div>

          <div className="flex gap-2 mb-6 border-b border-blostem-border pb-4">
            {PERSONAS.map(persona => (
              <button
                key={persona}
                onClick={() => setActivePersona(persona)}
                className={`px-4 py-2 text-base font-medium transition ${
                  activePersona === persona
                    ? 'border-b-2 border-blostem-purple text-blostem-purple'
                    : 'text-blostem-text-secondary'
                }`}
              >
                {persona}
              </button>
            ))}
          </div>

          {!sequences[activePersona] ? (
            <button
              onClick={() => handleGenerateSequence(activePersona)}
              disabled={generatingPersona === activePersona}
              className="px-4 py-2 bg-blostem-purple text-white rounded-md font-medium hover:opacity-90 transition"
            >
              {generatingPersona === activePersona ? 'Generating...' : 'Generate sequence'}
            </button>
          ) : (
            <div className="space-y-4">
              {[1, 2, 3].map(num => {
                const emailKey = `email_${num}`;
                const email = sequences[activePersona][emailKey];
                const dayLabels = {
                  1: 'Initial outreach',
                  2: 'Day 5 follow-up',
                  3: 'Day 12 nudge',
                };
                return (
                  <div key={num} className="bg-white border border-blostem-border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div className="font-medium text-blostem-text">Email {num} — {dayLabels[num]}</div>
                      <div className="flex items-center gap-2">
                        <StatusBadge status={sequences[activePersona].compliance} type="compliance" />
                        {selectedProspect.stakeholders.length > 0 && (
                          <EmailSendButton
                            sequenceId={sequences[activePersona].id}
                            emailIndex={num}
                            prospectName={selectedProspect.name}
                            stakeholders={selectedProspect.stakeholders}
                          />
                        )}
                      </div>
                    </div>
                    <div className="bg-blostem-surface p-3 rounded-md mb-3 text-sm text-blostem-text whitespace-pre-wrap">
                      {email}
                    </div>
                    {sequences[activePersona].compliance === 'review' && (
                      <div className="text-xs text-blostem-amber-text bg-blostem-amber-light p-2 rounded-md">
                        Review needed — check compliance flags
                      </div>
                    )}
                  </div>
                );
              })}
              <div className="text-xs text-blostem-text-muted bg-blostem-surface p-3 rounded-md">
                Fixed Deposits are subject to market risks. Please read all scheme-related documents carefully before investing.
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
