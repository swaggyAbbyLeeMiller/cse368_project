import "../App.css"
export default function AudioPlayer({ audioUrl }) {
  if (!audioUrl) return null;
  return (
    <div style={{height: "auto",
  padding: "10px 10px 10px 10px",
  width: "70%",
  margin: "auto",
  backgroundColor: "white",
  border: "3px solid rgb(180, 81, 0)",
  color:"rgb(180, 81, 0)",
  borderRadius:"5px"}}>
    <div>
      <h3>Listen:</h3>
      <audio controls src={audioUrl}></audio>
    </div>
    </div>
  );
}
