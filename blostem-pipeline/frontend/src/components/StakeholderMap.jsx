import { useState } from 'react';

const ROLE_COLORS = {
  'CEO': '#639922',
  'CTO': '#BA7517',
  'CFO': '#E24B4A',
  'Head of Compliance': '#0C447C',
  'Head of Product': '#3C3489',
  'Head of Partnerships': '#639922',
  'Founder & CEO': '#639922',
};

export default function StakeholderMap({ prospect }) {
  const [generatingFor, setGeneratingFor] = useState(null);

  const handleGenerateSequence = async (persona) => {
    setGeneratingFor(persona);
    try {
      const res = await fetch('/api/sequences/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prospect_id: prospect.id, persona }),
      });
      if (res.ok) {
        alert(`Sequence generated for ${persona}!`);
      }
    } catch (err) {
      alert('Error generating sequence');
    } finally {
      setGeneratingFor(null);
    }
  };

  return (
    <div className="grid grid-cols-3 gap-4">
      {prospect.stakeholders.map((s) => {
        const bgColor = ROLE_COLORS[s.role] || '#639922';
        return (
          <div key={s.id} className="bg-white border border-blostem-border rounded-lg p-4">
            <div className="flex items-center gap-3 mb-3">
              <div
                className="w-10 h-10 rounded-full flex items-center justify-center text-white font-medium text-sm"
                style={{ backgroundColor: bgColor }}
              >
                {s.initials}
              </div>
              <div>
                <div className="font-medium text-blostem-text text-base">{s.name}</div>
                <div className="text-xs text-blostem-text-muted">{s.role}</div>
              </div>
            </div>
            <div className="border-t border-blostem-border pt-3 mb-3">
              <div className="text-xs text-blostem-text-muted mb-1">Outreach angle</div>
              <div className="text-sm text-blostem-text">{s.angle}</div>
            </div>
            <button
              onClick={() => handleGenerateSequence(s.role)}
              disabled={generatingFor === s.role}
              className="w-full text-sm text-blostem-purple font-medium hover:opacity-80 transition"
            >
              {generatingFor === s.role ? 'Generating...' : 'Generate email →'}
            </button>
          </div>
        );
      })}
    </div>
  );
}
