export default function MetricCard({ label, value }) {
  return (
    <div className="bg-blostem-surface rounded-md p-4 border border-blostem-border">
      <div className="text-xs text-blostem-text-secondary mb-2">{label}</div>
      <div className="text-xl font-medium text-blostem-text">{value}</div>
    </div>
  );
}
