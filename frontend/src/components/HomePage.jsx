import React, { useState } from "react";
import "./HomePage.css";
import Spinner from "./Spinner"

function HomePage() {
  const [githubUrl, setGithubUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!githubUrl) return alert("Please enter a GitHub URL.");
    setLoading(true);

    try {
      const BASE_URL = import.meta.env.VITE_API_URL;
      const response = await fetch(`${BASE_URL}/init-chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo_url: githubUrl }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(`Server returned ${response.status} ${data.detail[0].msg}`);
        }

        if (!data.message) {
        throw new Error("Response does not contain a message.");
        }

      //console.log("API response:", data);

      setTimeout(() => {
        setLoading(false);
        window.open("/chat", "_blank");
      }, 5000);
    } catch (error) {
      //console.error(error);
      alert(`Error: ${error}`);
      setLoading(false);
    }
  };

  return (
    <div className="homepage-container">
      <h1 className="homepage-title">RepoWhisper</h1>
      <p className="homepage-subtitle">Chat with any public GitHub repository in seconds.</p>
      <div className="form-container">
        <input
          type="text"
          placeholder="Enter GitHub repository URL..."
          value={githubUrl}
          onChange={(e) => setGithubUrl(e.target.value)}
          className="repo-input"
          disabled={loading}
        />
        <button
          onClick={handleSubmit}
          className="analyze-btn"
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Analyze Repo"}
        </button>
      </div>

      {loading && (
        <div className="loading-overlay">
          <Spinner />
          <p className="loading-text">Analyzing repository, please wait...</p>
        </div>
      )}
    </div>
  );
}

export default HomePage;
