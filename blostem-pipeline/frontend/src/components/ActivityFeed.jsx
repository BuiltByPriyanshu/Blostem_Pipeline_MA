const ACTION_COLORS = {
  email_sent: { bg: 'bg-blostem-blue-light', text: 'text-blostem-blue', icon: '✉️' },
  sequence_generated: { bg: 'bg-blostem-purple-light', text: 'text-blostem-purple', icon: '✨' },
  compliance_checked: { bg: 'bg-blostem-green-light', text: 'text-blostem-green-text', icon: '✓' },
  prospect_viewed: { bg: 'bg-blostem-amber-light', text: 'text-blostem-amber-text', icon: '👁️' },
  sequence_viewed: { bg: 'bg-blostem-amber-light', text: 'text-blostem-amber-text', icon: '👁️' },
};

const formatTime = (timestamp) => {
  try {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    
    return date.toLocaleDateString();
  } catch {
    return timestamp;
  }
};

export default function ActivityFeed({ actions = [], limit = 20, onRefresh }) {
  const displayActions = actions.slice(0, limit);

  const getActionStyle = (actionType) => {
    return ACTION_COLORS[actionType] || {
      bg: 'bg-blostem-surface',
      text: 'text-blostem-text-secondary',
      icon: '•',
    };
  };

  if (displayActions.length === 0) {
    return (
      <div className="text-center py-8 text-blostem-text-muted">
        <p className="text-sm">No activity yet</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {displayActions.map((action) => {
        const style = getActionStyle(action.action_type);
        return (
          <div
            key={action.id}
            className={`${style.bg} border border-blostem-border rounded-lg p-3 flex items-start gap-3`}
          >
            <div className={`${style.text} text-lg flex-shrink-0 mt-0.5`}>
              {style.icon}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between gap-2">
                <div className="flex-1">
                  <p className="text-sm font-medium text-blostem-text">
                    {action.description}
                  </p>
                  {action.entity_name && (
                    <p className="text-xs text-blostem-text-muted mt-1">
                      {action.entity_name}
                    </p>
                  )}
                </div>
                <p className="text-xs text-blostem-text-muted flex-shrink-0 whitespace-nowrap">
                  {formatTime(action.created_at)}
                </p>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
