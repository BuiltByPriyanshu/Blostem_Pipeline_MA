import { useState, useEffect } from 'react';

export function useActivation() {
  const [partners, setPartners] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/activation/pipeline")
      .then(r => {
        if (!r.ok) throw new Error(r.statusText);
        return r.json();
      })
      .then(data => {
        setPartners(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const reengage = async (partnerId) => {
    try {
      const res = await fetch(`/api/activation/reengage/${partnerId}`, {
        method: "POST",
      });
      if (!res.ok) throw new Error(res.statusText);
      const data = await res.json();
      return data;
    } catch (err) {
      throw err;
    }
  };

  const refetch = () => {
    setLoading(true);
    fetch("/api/activation/pipeline")
      .then(r => {
        if (!r.ok) throw new Error(r.statusText);
        return r.json();
      })
      .then(data => {
        setPartners(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  };

  return { partners, loading, error, reengage, refetch };
}
