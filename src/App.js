import React, { useState } from "react";
import axios from "axios";
import "./index";

function App() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [darkMode, setDarkMode] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file to upload!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (res.status === 200) {
        setResponse(res.data);
      } else {
        alert("Error uploading video: " + res.statusText);
      }
    } catch (err) {
      console.error(err);
      alert(
        err.response?.data?.error || "An unknown error occurred during upload."
      );
    }
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <div className={`app-container ${darkMode ? "dark-mode" : ""}`}>
      <header className="header">
        <h1>🎥 Video Violence Detection System</h1>
        <div className="toggle-switch">
          <input
            type="checkbox"
            id="darkModeToggle"
            checked={darkMode}
            onChange={toggleDarkMode}
          />
          <label htmlFor="darkModeToggle"></label>
        </div>
      </header>
      <div className="cards-container">
        {/* Upload Section */}
        <div className="card upload-card">
          <h2>Upload Video</h2>
          <p>Upload a video to check for violence detection.</p>
          <input type="file" onChange={handleFileChange} accept="video/*" />
          <button className="upload-button" onClick={handleUpload}>
            Upload Video
          </button>
        </div>
        {/* Result Section */}
        <div className="card result-card">
          <h2>Results</h2>
          {response ? (
            response.violence_detected ? (
              <div className="result-content detected">
                <p>🚨 Violence Detected!</p>
                <img
                  src={`http://127.0.0.1:5000/uploads/${response.frame_path}`}
                  alt="Violence Frame"
                  className="result-image"
                />
              </div>
            ) : (
              <div className="result-content not-detected">
                <p>✅ No Violence Detected!</p>
              </div>
            )
          ) : (
            <p className="placeholder-text">
              Results will appear here after upload.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
