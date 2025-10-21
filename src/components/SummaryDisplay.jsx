export default function SummaryDisplay({ summary }) {
  if (!summary) return null;
  return (
    <div>
      <h2>Summary:</h2>
      <p>{summary.summary_text}</p>
    </div>
  );
}
