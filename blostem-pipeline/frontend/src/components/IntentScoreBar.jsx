import { getScoreColor } from '../utils/formatters';

export default function IntentScoreBar({ score }) {
  const colors = getScoreColor(score);
  const percentage = (score / 100) * 100;

  return (
    <div className="flex items-center gap-3">
      <div className="flex-1 h-1.5 bg-blostem-border rounded-sm overflow-hidden">
        <div
          className="h-full rounded-sm transition-all"
          style={{ width: `${percentage}%`, backgroundColor: colors.bar }}
        />
      </div>
      <div
        className="px-2 py-0.5 rounded-full text-xs font-medium"
        style={{ backgroundColor: colors.fill, color: colors.text }}
      >
        {score}
      </div>
    </div>
  );
}
