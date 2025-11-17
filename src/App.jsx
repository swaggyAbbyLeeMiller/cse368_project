import { useState } from "react";
import UploadForm from "./components/UploadForm";
import SummaryDisplay from "./components/SummaryDisplay";
import AudioPlayer from "./components/AudioPlayer";
import Background from "./components/Background";
import "./App.css"

function App() {
  const [result, setResult] = useState(null);

  return (
    <>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Text:ital@0;1&family=Quicksand:wght@300..700&family=Space+Grotesk:wght@300..700&display=swap" rel="stylesheet"></link>
  
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "75vh",
        textAlign: "center",
        gap: "20px",
        padding: "20px",
        zIndex: 10, position: "relative" ,
        background:"none",
      }}
    >
      <h1>SummA.I.ry - Lecture Summarizer</h1>
      <UploadForm onResult={setResult} />
      <SummaryDisplay summary={result} />
      <AudioPlayer audioUrl={result?.audio_url} />
    </div>
     <Background> </Background>
    </>
  );
}

export default App;
