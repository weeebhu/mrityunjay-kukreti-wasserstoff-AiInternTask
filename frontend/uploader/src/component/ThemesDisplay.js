import React, { useState } from "react";
import "./ThemesDisplay.css";

const ThemesDisplay = ({ themes }) => {
  const [openThemes, setOpenThemes] = useState({});

  const toggleTheme = (themeName) => {
    setOpenThemes((prev) => ({
      ...prev,
      [themeName]: !prev[themeName],
    }));
  };

  // Group filenames by theme
  const groupedThemes = themes.reduce((acc, item) => {
    if (!acc[item.theme]) acc[item.theme] = [];
    acc[item.theme].push(item.filename);
    return acc;
  }, {});

  if (!themes || themes.length === 0) {
    return <p className="loading-text">No themes available yet.</p>;
  }

  return (
    <div className="themes-container">
      {Object.entries(groupedThemes).map(([themeName, filenames]) => (
        <div className="theme-card" key={themeName}>
          <div
            className="theme-header"
            onClick={() => toggleTheme(themeName)}
          >
            <span>{themeName}</span>
            <span className={`arrow ${openThemes[themeName] ? "open" : ""}`}>
              ▶
            </span>
          </div>
          {openThemes[themeName] && (
            <ul className="theme-documents">
              {filenames.map((filename, idx) => (
                <li key={idx}>{filename}</li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </div>
  );
};

export default ThemesDisplay;
