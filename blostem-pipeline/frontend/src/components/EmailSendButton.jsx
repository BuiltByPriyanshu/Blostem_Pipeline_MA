import { useState } from 'react';

export default function EmailSendButton({ sequenceId, emailIndex, prospectName, stakeholders, onSent }) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedStakeholder, setSelectedStakeholder] = useState(null);
  const [isSending, setIsSending] = useState(false);
  const [message, setMessage] = useState('');

  const handleSend = async () => {
    if (!selectedStakeholder) {
      setMessage('Please select a stakeholder');
      return;
    }

    setIsSending(true);
    setMessage('');

    try {
      const res = await fetch('/api/email/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sequence_id: sequenceId,
          email_index: emailIndex,
          recipient_email: selectedStakeholder.email,
          prospect_name: prospectName,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        if (data.sent) {
          setMessage(`✓ Email sent to ${selectedStakeholder.name}`);
          setIsOpen(false);
          setSelectedStakeholder(null);
          if (onSent) onSent();
        } else {
          setMessage('Failed to send email. Check API key.');
        }
      } else {
        setMessage('Error sending email');
      }
    } catch (err) {
      setMessage('Network error');
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="px-3 py-1 text-sm bg-blostem-blue text-white rounded-md hover:opacity-90 transition"
      >
        Send email
      </button>

      {isOpen && (
        <div className="absolute top-full right-0 mt-2 w-64 bg-white border border-blostem-border rounded-lg shadow-lg p-4 z-50">
          <div className="mb-3">
            <label className="block text-sm font-medium text-blostem-text mb-2">
              Send to:
            </label>
            <select
              value={selectedStakeholder?.id || ''}
              onChange={(e) => {
                const sh = stakeholders.find(s => s.id === parseInt(e.target.value));
                setSelectedStakeholder(sh);
              }}
              className="w-full px-3 py-2 border border-blostem-border rounded-md text-sm bg-white text-blostem-text"
            >
              <option value="">Select stakeholder...</option>
              {stakeholders.map(sh => (
                <option key={sh.id} value={sh.id}>
                  {sh.name} ({sh.role})
                </option>
              ))}
            </select>
          </div>

          {message && (
            <div className={`text-xs p-2 rounded-md mb-3 ${
              message.startsWith('✓')
                ? 'bg-blostem-green-light text-blostem-green-text'
                : 'bg-blostem-red-light text-blostem-red'
            }`}>
              {message}
            </div>
          )}

          <div className="flex gap-2">
            <button
              onClick={handleSend}
              disabled={isSending || !selectedStakeholder}
              className="flex-1 px-3 py-2 bg-blostem-purple text-white text-sm rounded-md hover:opacity-90 transition disabled:opacity-50"
            >
              {isSending ? 'Sending...' : 'Send'}
            </button>
            <button
              onClick={() => {
                setIsOpen(false);
                setMessage('');
              }}
              className="flex-1 px-3 py-2 border border-blostem-border text-sm rounded-md text-blostem-text hover:bg-blostem-surface transition"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
