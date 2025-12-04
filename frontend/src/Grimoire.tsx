import { useState } from 'react';
import type { Element } from './types';
import { ElementDetail } from './ElementDetail';

interface GrimoireProps {
  elements: Element[];
  onClose: () => void;
}

export function Grimoire({ elements, onClose }: GrimoireProps) {
  const [selectedElement, setSelectedElement] = useState<Element | null>(null);

  const handleElementClick = (element: Element) => {
    setSelectedElement(element);
  };

  const handleCloseDetail = () => {
    setSelectedElement(null);
  };

  return (
    <div className="grimoire-overlay" onClick={onClose}>
      <div className="grimoire-modal" onClick={(e) => e.stopPropagation()}>
        <div className="grimoire-header">
          <h1>Grimoire of Elements</h1>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>

        <div className="grimoire-content">
          {/* Stats Overview */}
          <div className="grimoire-stats">
            <div className="stat">
              <span className="stat-label">Total Discovered:</span>
              <span className="stat-value">{elements.length}</span>
            </div>
            <div className="stat">
              <span className="stat-label">Base Elements:</span>
              <span className="stat-value">{elements.filter(e => e.is_base).length}</span>
            </div>
            <div className="stat">
              <span className="stat-label">Derived Elements:</span>
              <span className="stat-value">{elements.filter(e => !e.is_base).length}</span>
            </div>
          </div>

          {/* Element Grid */}
          <div className="grimoire-grid">
            {elements.map((element) => (
              <div
                key={element.id}
                className={`grimoire-element-card ${element.is_base ? 'base' : 'derived'}`}
                onClick={() => handleElementClick(element)}
                title="Click to view details"
              >
                <div
                  className="grimoire-element-icon"
                  dangerouslySetInnerHTML={{ __html: element.emoji }}
                />
                <div className="grimoire-element-name">{element.name}</div>
                {element.parent_a_name && element.parent_b_name && (
                  <div className="grimoire-element-formula">
                    {element.parent_a_name} + {element.parent_b_name}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Element Detail Modal */}
      {selectedElement && (
        <ElementDetail element={selectedElement} onClose={handleCloseDetail} />
      )}
    </div>
  );
}
