import { useState } from 'react';
import { useProspects } from '../hooks/useProspects';
import ProspectTable from '../components/ProspectTable';
import MetricCard from '../components/MetricCard';
import AddCompanyModal from '../components/AddCompanyModal';

export default function Pipeline() {
  const { prospects, loading, error, refetch } = useProspects();
  const [stageFilter, setStageFilter] = useState('all');
  const [sortBy, setSortBy] = useState('score');
  const [isModalOpen, setIsModalOpen] = useState(false);

  let filtered = prospects;
  if (stageFilter !== 'all') {
    filtered = prospects.filter(p => p.stage === stageFilter);
  }

  if (sortBy === 'score') {
    filtered = [...filtered].sort((a, b) => b.score - a.score);
  } else if (sortBy === 'name') {
    filtered = [...filtered].sort((a, b) => a.name.localeCompare(b.name));
  }

  const hotCount = prospects.filter(p => p.score >= 80).length;
  const avgScore = prospects.length > 0 ? Math.round(prospects.reduce((sum, p) => sum + p.score, 0) / prospects.length) : 0;
  const seqReady = prospects.filter(p => p.seq_ready).length;
  const compliancePassed = prospects.filter(p => p.compliance === 'passed').length;

  if (loading) return <div className="p-8 text-blostem-text-muted">Loading...</div>;
  if (error) return <div className="p-8 text-blostem-red">Error: {error}</div>;

  return (
    <div className="ml-[220px] p-8 min-h-screen bg-blostem-bg">
      <div className="mb-8">
        <h1 className="text-xl font-medium text-blostem-text mb-1">Prospect pipeline</h1>
        <p className="text-sm text-blostem-text-muted">Ranked by intent score · {prospects.length} prospects</p>
      </div>

      <div className="grid grid-cols-4 gap-3 mb-8">
        <MetricCard label="Hot prospects" value={hotCount} />
        <MetricCard label="Avg intent score" value={avgScore} />
        <MetricCard label="Sequences ready" value={seqReady} />
        <MetricCard label="Compliance passed" value={compliancePassed} />
      </div>

      <div className="flex gap-4 mb-6 items-center justify-between">
        <div className="flex gap-4">
          <select
            value={stageFilter}
            onChange={(e) => setStageFilter(e.target.value)}
            className="px-3 py-2 border border-blostem-border rounded-md text-sm bg-white text-blostem-text"
          >
            <option value="all">All stages</option>
            <option value="Series A">Series A</option>
            <option value="Series B">Series B</option>
            <option value="Series C">Series C</option>
            <option value="Series D">Series D</option>
            <option value="Series E">Series E</option>
          </select>
        </div>
        <div className="flex gap-4 items-center">
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-3 py-2 border border-blostem-border rounded-md text-sm bg-white text-blostem-text"
          >
            <option value="score">Sort by score</option>
            <option value="name">Sort by name</option>
          </select>
          <button
            onClick={() => setIsModalOpen(true)}
            className="px-4 py-2 bg-blostem-purple text-white rounded-md font-medium hover:opacity-90 transition"
          >
            + Add Company
          </button>
        </div>
      </div>

      <div className="bg-white border border-blostem-border rounded-lg overflow-hidden">
        <ProspectTable prospects={filtered} />
      </div>

      <AddCompanyModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onCompanyAdded={() => {
          if (refetch) refetch();
        }}
      />
    </div>
  );
}
