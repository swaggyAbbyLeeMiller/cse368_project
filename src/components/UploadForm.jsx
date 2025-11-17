import { useState } from "react";
import axios from "axios";
import "../App.css"

export default function UploadForm({ onResult }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      // The backend should return JSON with summary_text and audio_url
      onResult(response.data);
    } catch (err) {
      console.error(err);
      setError("Upload failed. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <label className="upload">
      <input type="file" onChange={handleFileChange} />
      </label>
      <br />
      <button onClick={handleUpload} disabled={loading} className="button" style={{ marginTop: "10px" }}>
        {loading ? "Uploading..." : "Upload"}
      </button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
