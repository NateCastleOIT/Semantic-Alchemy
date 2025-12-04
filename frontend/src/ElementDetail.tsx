import type { Element } from './types';

interface ElementDetailProps {
  element: Element;
  onClose: () => void;
}

export function ElementDetail({ element, onClose }: ElementDetailProps) {
  return (
    <div className="element-detail-overlay" onClick={onClose}>
      <div className="element-detail-modal" onClick={(e) => e.stopPropagation()}>
        <button className="close-button detail-close" onClick={onClose}>✕</button>

        <div className="element-detail-content">
          {/* Large Spell Circle */}
          <div className="element-detail-circle">
            <div
              className="detail-spell-circle"
              dangerouslySetInnerHTML={{ __html: element.emoji }}
            />
          </div>

          {/* Element Information */}
          <div className="element-detail-info">
            <h2 className="detail-name">{element.name}</h2>

            {element.is_base && (
              <div className="detail-badge base-badge">Base Element</div>
            )}

            {!element.is_base && element.parent_a_name && element.parent_b_name && (
              <div className="detail-lineage">
                <div className="lineage-label">Created From:</div>
                <div className="lineage-formula">
                  <span className="parent-name">{element.parent_a_name}</span>
                  <span className="plus">+</span>
                  <span className="parent-name">{element.parent_b_name}</span>
                </div>
              </div>
            )}

            <div className="detail-section">
              <h3>Description</h3>
              <p className="detail-description">{element.definition}</p>
            </div>

            {element.tags.length > 0 && (
              <div className="detail-section">
                <h3>Properties</h3>
                <div className="detail-tags">
                  {element.tags.map((tag, index) => (
                    <span key={index} className="detail-tag">{tag}</span>
                  ))}
                </div>
              </div>
            )}

            {element.behavior_hints.length > 0 && (
              <div className="detail-section">
                <h3>Behaviors</h3>
                <div className="detail-behaviors">
                  {element.behavior_hints.map((behavior, index) => (
                    <span key={index} className="detail-behavior">
                      {behavior}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
