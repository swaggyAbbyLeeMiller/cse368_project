import { useState } from "react";
import UploadForm from "./components/UploadForm";
import SummaryDisplay from "./components/SummaryDisplay";
import AudioPlayer from "./components/AudioPlayer";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        textAlign: "center",
        gap: "20px",
        padding: "20px",
      }}
    >
      <h1>SummA.I.ry - Lecture Summarizer</h1>
      <UploadForm onResult={setResult} />
      <SummaryDisplay summary={result} />
      <AudioPlayer audioUrl={result?.audio_url} />
    </div>
  );
}

export default App;
