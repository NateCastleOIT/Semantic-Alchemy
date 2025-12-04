import { useState, useEffect } from 'react';
import './App.css';
import { api } from './api';
import type { Element, Stats, CombineResponse } from './types';

function App() {
  const [elements, setElements] = useState<Element[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [slot1, setSlot1] = useState<Element | null>(null);
  const [slot2, setSlot2] = useState<Element | null>(null);
  const [result, setResult] = useState<CombineResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load elements and stats on mount
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [elementsData, statsData] = await Promise.all([
        api.getElements(),
        api.getStats(),
      ]);
      setElements(elementsData);
      setStats(statsData);
    } catch (err) {
      setError('Failed to connect to backend. Make sure the FastAPI server is running on port 8000.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleElementClick = (element: Element) => {
    if (!slot1) {
      setSlot1(element);
    } else if (!slot2) {
      setSlot2(element);
    } else {
      // If both slots filled, replace slot1
      setSlot1(element);
      setSlot2(null);
    }
    // Clear result when selecting new elements
    setResult(null);
  };

  const handleCombine = async () => {
    if (!slot1 || !slot2) return;

    try {
      const response = await api.combineElements(slot1.id, slot2.id);
      setResult(response);

      // If successful, reload elements to show new discovery
      if (response.success) {
        const updatedElements = await api.getElements();
        setElements(updatedElements);
        const updatedStats = await api.getStats();
        setStats(updatedStats);
      }
    } catch (err) {
      setError('Failed to combine elements');
      console.error(err);
    }
  };

  const handleClear = () => {
    setSlot1(null);
    setSlot2(null);
    setResult(null);
  };

  if (loading) {
    return (
      <div className="app">
        <div className="loading">Loading Alchemy Lab...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app">
        <div className="error">
          <h2>Error</h2>
          <p>{error}</p>
          <button onClick={loadData} className="clear-button" style={{ marginTop: '20px' }}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Semantic Alchemy Lab</h1>
        {stats && (
          <div className="stats">
            <div className="stat-item">
              Total Elements: {stats.total_elements}
            </div>
            <div className="stat-item">
              Base Elements: {stats.base_elements}
            </div>
            <div className="stat-item">
              Discovered: {stats.discovered_elements}
            </div>
          </div>
        )}
      </header>

      <div className="game-container">
        {/* Elements Panel */}
        <div className="elements-panel">
          <h2>Your Elements</h2>
          <div className="elements-grid">
            {elements.map((element) => (
              <div
                key={element.id}
                className={`element-card ${
                  (slot1?.id === element.id || slot2?.id === element.id) ? 'selected' : ''
                }`}
                onClick={() => handleElementClick(element)}
                title={element.definition}
              >
                <div
                  className="element-icon"
                  dangerouslySetInnerHTML={{ __html: element.emoji }}
                />
                <div className="element-name">{element.name}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Combination Panel */}
        <div className="combination-panel">
          <div className="combination-area">
            {/* Slot 1 */}
            <div
              className={`combination-slot ${slot1 ? 'filled' : ''}`}
              onClick={() => slot1 && setSlot1(null)}
            >
              {slot1 ? (
                <>
                  <div
                    className="slot-icon"
                    dangerouslySetInnerHTML={{ __html: slot1.emoji }}
                  />
                  <div className="slot-name">{slot1.name}</div>
                </>
              ) : (
                <div style={{ opacity: 0.5 }}>Click an element</div>
              )}
            </div>

            <div className="plus-sign">+</div>

            {/* Slot 2 */}
            <div
              className={`combination-slot ${slot2 ? 'filled' : ''}`}
              onClick={() => slot2 && setSlot2(null)}
            >
              {slot2 ? (
                <>
                  <div
                    className="slot-icon"
                    dangerouslySetInnerHTML={{ __html: slot2.emoji }}
                  />
                  <div className="slot-name">{slot2.name}</div>
                </>
              ) : (
                <div style={{ opacity: 0.5 }}>Click an element</div>
              )}
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <button
                className="combine-button"
                onClick={handleCombine}
                disabled={!slot1 || !slot2}
              >
                Combine!
              </button>
              <button
                className="clear-button"
                onClick={handleClear}
              >
                Clear
              </button>
            </div>
          </div>
        </div>

        {/* Result Panel - Persistent on the right */}
        <div className="result-panel">
          <h2>Last Result</h2>
          {result ? (
            <div className={`result-area ${result.success ? 'success' : 'failure'}`}>
              {result.success ? (
                <>
                  <div
                    className="result-icon"
                    dangerouslySetInnerHTML={{ __html: result.result?.emoji || '' }}
                  />
                  <div className="result-name">{result.result?.name}</div>
                  <div className="result-definition">{result.result?.definition}</div>
                  {result.was_discovered && (
                    <div className="result-badge">NEW DISCOVERY!</div>
                  )}
                </>
              ) : (
                <>
                  <div style={{ fontSize: '3em', marginBottom: '10px' }}>❌</div>
                  <div>{result.message}</div>
                </>
              )}
            </div>
          ) : (
            <div className="result-placeholder">
              Combine elements to see results here
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
