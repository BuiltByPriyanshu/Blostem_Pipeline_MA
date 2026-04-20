import { useState } from 'react';

export default function AddCompanyModal({ isOpen, onClose, onCompanyAdded }) {
  const [formData, setFormData] = useState({
    name: '',
    hq_city: '',
    industry: '',
    stage: '',
    funding_usd: '',
    funding_label: '',
    last_news: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const res = await fetch('/api/prospects/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: formData.name,
          hq_city: formData.hq_city,
          industry: formData.industry,
          stage: formData.stage,
          funding_usd: parseInt(formData.funding_usd) || 0,
          funding_label: formData.funding_label,
          last_news: formData.last_news || null,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setSuccess(`Company "${data.name}" added successfully!`);
        setFormData({
          name: '',
          hq_city: '',
          industry: '',
          stage: '',
          funding_usd: '',
          funding_label: '',
          last_news: '',
        });
        if (onCompanyAdded) onCompanyAdded();
        setTimeout(() => {
          onClose();
        }, 1500);
      } else {
        setError('Failed to add company');
      }
    } catch (err) {
      setError('Error adding company');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-medium text-blostem-text">Add New Company</h2>
          <button
            onClick={onClose}
            className="text-blostem-text-muted hover:text-blostem-text"
          >
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-blostem-text mb-1">
                Company Name *
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-blostem-border rounded-md text-sm bg-white text-blostem-text"
                placeholder="e.g., TechCorp India"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-blostem-text mb-1">
                HQ City *
              </label>
              <input
                type="text"
                name="hq_city"
                value={formData.hq_city}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-blostem-border rounded-md text-sm bg-white text-blostem-text"
                placeholder="e.g., Bangalore"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-blostem-text mb-1">
                Industry *
              </label>
              <input
                type="text"
                name="industry"
                value={formData.industry}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-blostem-border rounded-md text-sm bg-white text-blostem-text"
                placeholder="e.g., SaaS, Fintech"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-blostem-text mb-1">
                Stage *
              </label>
              <select
                name="stage"
                value={formData.stage}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-blostem-border rounded-md text-sm bg-white text-blostem-text"
              >
                <option value="">Select stage</option>
                <option value="Seed">Seed</option>
                <option value="Series A">Series A</option>
                <option value="Series B">Series B</option>
                <option value="Series C">Series C</option>
                <option value="Series D">Series D</option>
                <option value="Series E">Series E</option>
                <option value="Growth">Growth</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-blostem-text mb-1">
                Funding (USD) *
              </label>
              <input
                type="number"
                name="funding_usd"
                value={formData.funding_usd}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-blostem-border rounded-md text-sm bg-white text-blostem-text"
                placeholder="e.g., 5000000"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-blostem-text mb-1">
                Funding Label *
              </label>
              <input
                type="text"
                name="funding_label"
                value={formData.funding_label}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-blostem-border rounded-md text-sm bg-white text-blostem-text"
                placeholder="e.g., $5M Series A"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-blostem-text mb-1">
              Latest News
            </label>
            <textarea
              name="last_news"
              value={formData.last_news}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-blostem-border rounded-md text-sm bg-white text-blostem-text"
              placeholder="e.g., Company raises Series A to expand fintech platform"
              rows="3"
            />
          </div>

          {error && (
            <div className="text-sm text-blostem-red bg-blostem-red-light p-3 rounded-md">
              {error}
            </div>
          )}

          {success && (
            <div className="text-sm text-blostem-green-text bg-blostem-green-light p-3 rounded-md">
              ✓ {success}
            </div>
          )}

          <div className="flex gap-2 pt-4">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 px-4 py-2 bg-blostem-purple text-white rounded-md font-medium hover:opacity-90 transition disabled:opacity-50"
            >
              {loading ? 'Adding...' : 'Add Company'}
            </button>
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-blostem-border text-blostem-text rounded-md font-medium hover:bg-blostem-surface transition"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
