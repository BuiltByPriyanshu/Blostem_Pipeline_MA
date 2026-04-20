export default function IntentSignals({ prospect }) {
  const getSignalColor = (type) => {
    switch (type) {
      case 'hiring':
        return { bg: '#E6F1FB', text: '#0C447C' };
      case 'news':
        return { bg: '#EAF3DE', text: '#27500A' };
      case 'activity':
        return { bg: '#EEEDFE', text: '#3C3489' };
      default:
        return { bg: '#F8F8F6', text: '#6B6A65' };
    }
  };

  return (
    <div className="space-y-3">
      <div className="text-sm text-blostem-text-muted">
        Score breakdown: {prospect.signals.length} signals detected
      </div>
      <div className="space-y-2">
        {prospect.signals.map((sig, idx) => {
          const colors = getSignalColor(sig.signal_type);
          return (
            <div key={idx} className="flex gap-3 items-start">
              <div
                className="px-2 py-0.5 rounded-full text-xs font-medium whitespace-nowrap mt-0.5"
                style={{ backgroundColor: colors.bg, color: colors.text }}
              >
                {sig.signal_type.charAt(0).toUpperCase() + sig.signal_type.slice(1)}
              </div>
              <div className="text-sm text-blostem-text">{sig.description}</div>
            </div>
          );
        })}
      </div>
      <button className="text-sm text-blostem-purple font-medium hover:opacity-80 transition mt-4">
        Generate full sequence for {prospect.name} →
      </button>
    </div>
  );
}
