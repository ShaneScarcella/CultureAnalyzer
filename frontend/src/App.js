import React, { useState } from 'react';
import axios from 'axios'; // Import axios
import './App.css';

const Results = ({ data }) => {
  if (!data) return null;

  return (
    <div className="results-section">
      {Object.entries(data).map(([category, matches]) => (
        <div key={category} className="result-category">
          <h2>{category.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</h2>
          <div className="matches-container">
            {matches.map((match, index) => (
              <div key={index} className="match-card">
                <div className="match-name">{match.name}</div>
                <div className="match-score-bar-container">
                  <div 
                    className="match-score-bar" 
                    style={{ width: `${match.score * 100}%` }}
                  ></div>
                </div>
                <div className="match-score-value">{(match.score * 100).toFixed(1)}%</div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};


function App() {
  const [text, setText] = useState('');
  const [file, setFile] = useState(null);
  // New state variables to hold results, loading status, and errors
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleTextAnalysis = async () => {
    if (!text) {
      setError('Please enter some text to analyze.');
      return;
    }
    setIsLoading(true);
    setError('');
    setResults(null);
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/v1/analyze', { text });
      setResults(response.data);
    } catch (err) {
      setError('An error occurred while analyzing the text.');
      console.error(err);
    }
    setIsLoading(false);
  };

  const handleFileAnalysis = async () => {
    if (!file) {
      setError('Please select a file to analyze.');
      return;
    }
    setIsLoading(true);
    setError('');
    setResults(null);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/v1/analyze-file', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setResults(response.data);
    } catch (err) {
      setError('An error occurred while analyzing the file.');
      console.error(err);
    }
    setIsLoading(false);
  };


  return (
    <div className="App">
      <header className="App-header">
        <h1>Culture & Role Fit Analyzer</h1>
        <p>Paste your resume summary or upload a document to see how you match up with different company cultures, roles, and skills.</p>
      </header>
      
      <main className="App-main">
        <div className="input-section">
          <h2>Analyze Your Text</h2>
          <textarea
            className="text-input"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste your resume summary here..."
          />
          <button onClick={handleTextAnalysis} className="analyze-button" disabled={isLoading}>
            {isLoading ? 'Analyzing...' : 'Analyze Text'}
          </button>
        </div>

        <div className="divider">OR</div>

        <div className="input-section">
          <h2>Analyze a Document</h2>
          <input 
            type="file" 
            className="file-input" 
            onChange={(e) => setFile(e.target.files[0])}
          />
          <button onClick={handleFileAnalysis} className="analyze-button" disabled={isLoading}>
            {isLoading ? 'Analyzing...' : 'Upload and Analyze'}
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}
        {isLoading && <div className="loading-spinner"></div>}
        <Results data={results} />
      </main>
    </div>
  );
}

export default App;