import React, { useState } from 'react';
import './App.css';

function App() {
  const [inputCode, setInputCode] = useState('');
  const [output, setOutput] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleConvert = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/convert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input_code: inputCode, target_language: 'typescript' }),
      });
      const data = await response.json();
      setOutput(data);
    } catch (error) {
      console.error('Error:', error);
      setOutput({ error: 'Failed to connect to backend' });
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>Selenium to Playwright</h1>

      <div className="converter-box">
        {/* Left Panel: Input */}
        <div className="code-panel">
          <div className="panel-title">
            <span>☕</span> Java Selenium
          </div>
          <div className="editor-wrapper">
            <textarea
              value={inputCode}
              onChange={(e) => setInputCode(e.target.value)}
              placeholder="// Paste your Selenium Java code here...
driver.get('https://example.com');
driver.findElement(By.id('login')).click();"
              spellCheck="false"
              className="code-input"
            />
          </div>
        </div>

        {/* Right Panel: Output */}
        <div className="code-panel">
          <div className="panel-title">
            <span>🎭</span> Playwright TypeScript
          </div>
          <div className="editor-wrapper">
            <textarea
              readOnly
              value={output?.converted_code || '// Converted code will appear here...'}
              className="code-output"
              spellCheck="false"
            />
          </div>
        </div>

        {/* Action Button */}
        <div className="actions-bar">
          <button onClick={handleConvert} disabled={loading} className="convert-btn">
            {loading ? (
              <>
                <span>⚙️</span> Converting...
              </>
            ) : (
              <>
                <span>⚡</span> Convert Logic
              </>
            )}
          </button>
        </div>
      </div>

      {/* Logs Section */}
      {output && (output.logs || output.error) && (
        <div className="logs-section">
          {output.error && <div className="log-item log-error">❌ {output.error}</div>}
          {output.logs && output.logs.map((log, i) => (
            <div key={i} className={`log-item log-${log.level}`}>
              {log.level === 'info' ? 'ℹ️' : log.level === 'warning' ? '⚠️' : '❌'} {log.message}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;

