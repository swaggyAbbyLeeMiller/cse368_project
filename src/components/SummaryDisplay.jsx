import "../App.css";

export default function SummaryDisplay({ summary }) {
  if (!summary) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(summary.summary_text);
    alert("Copied to clipboard!");
  };

  return (
    <div style={{height: "auto",
  padding: "10px 10px 10px 10px",
  width: "70%",
  margin: "auto",
  backgroundColor: "white",
  border: "3px solid rgb(180, 81, 0)",
  color:"rgb(180, 81, 0)",
  borderRadius:"5px"}}>
     
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
          backgroundColor: "rgb(180, 81, 0)",
          color: "white",
          border: "1px solid white",
          borderRadius: "6px",
          cursor: "pointer",
          fontWeight: "bold",
          
        }}
      >
        Copy Text
      </button>
    </div>
    </div>
  );
}
