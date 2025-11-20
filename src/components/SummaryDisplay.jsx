import "../App.css";

export default function SummaryDisplay({ summary }) {
  if (!summary) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(summary.summary_text);
    alert("Copied to clipboard!");
  };

  return (
    <div style={{ marginTop: "20px" }}>
      <h2>Summary:</h2>

      <p style={{ whiteSpace: "pre-wrap" }}>
        {summary.summary_text}
      </p>

      <button
        onClick={handleCopy}
        style={{
          marginTop: "10px",
          padding: "6px 14px",
          backgroundColor: "#4caf50",
          color: "white",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer",
          fontWeight: "bold",
        }}
      >
        Copy Text
      </button>
    </div>
  );
}
