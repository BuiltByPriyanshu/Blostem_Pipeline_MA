export default function SparkLine({ data, status = 'active' }) {
  const maxValue = Math.max(...data, 1);
  const barColor = status === 'critical' ? '#E24B4A' : status === 'stalled' ? '#BA7517' : '#639922';
  const zeroColor = '#D3D1C7';

  return (
    <div className="flex items-end gap-0.5 h-7">
      {data.map((value, idx) => (
        <div
          key={idx}
          className="flex-1 rounded-sm"
          style={{
            height: value === 0 ? '4px' : `${(value / maxValue) * 100}%`,
            backgroundColor: value === 0 ? zeroColor : barColor,
            minHeight: '4px',
          }}
        />
      ))}
    </div>
  );
}
