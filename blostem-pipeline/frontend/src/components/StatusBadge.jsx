import { getStatusColor, getComplianceColor } from '../utils/formatters';

export default function StatusBadge({ status, type = 'status' }) {
  const colors = type === 'compliance' ? getComplianceColor(status) : getStatusColor(status);
  const label = status.charAt(0).toUpperCase() + status.slice(1);

  return (
    <div
      className="px-2 py-0.5 rounded-full text-xs font-medium inline-block"
      style={{ backgroundColor: colors.bg, color: colors.text }}
    >
      {label}
    </div>
  );
}
