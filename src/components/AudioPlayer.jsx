import "../App.css"
export default function AudioPlayer({ audioUrl }) {
  if (!audioUrl) return null;
  return (
    <div>
      <h3>Listen:</h3>
      <audio controls src={audioUrl}></audio>
    </div>
  );
}
