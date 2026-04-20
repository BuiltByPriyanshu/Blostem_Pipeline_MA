export const formatDaysAgo = (days) => {
  if (days === 0) return "Today";
  if (days === 1) return "Yesterday";
  return `${days} days ago`;
};

export const formatFunding = (usd) => {
  if (!usd) return "$0";
  if (usd >= 1_000_000_000) return `$${(usd/1e9).toFixed(1)}B`;
  if (usd >= 1_000_000) return `$${Math.round(usd/1e6)}M`;
  return `$${usd.toLocaleString()}`;
};

export const getScoreColor = (score) => {
  if (score >= 80) return { bar: "#639922", fill: "#EAF3DE", text: "#27500A" };
  if (score >= 60) return { bar: "#BA7517", fill: "#FAEEDA", text: "#633806" };
  return { bar: "#E24B4A", fill: "#FCEBEB", text: "#791F1F" };
};

export const getStatusColor = (status) => {
  switch (status) {
    case "active":
      return { bg: "#EAF3DE", text: "#27500A", border: "#639922" };
    case "stalled":
      return { bg: "#FAEEDA", text: "#633806", border: "#BA7517" };
    case "critical":
      return { bg: "#FCEBEB", text: "#791F1F", border: "#E24B4A" };
    case "new":
      return { bg: "#E6F1FB", text: "#0C447C", border: "#0C447C" };
    default:
      return { bg: "#F8F8F6", text: "#6B6A65", border: "#E8E7E2" };
  }
};

export const getComplianceColor = (status) => {
  if (status === "passed") return { bg: "#EAF3DE", text: "#27500A" };
  if (status === "review") return { bg: "#FAEEDA", text: "#633806" };
  return { bg: "#F8F8F6", text: "#6B6A65" };
};
