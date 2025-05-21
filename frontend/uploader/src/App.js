import Uploader from './component/Uploader'
import QueryChat from './component/QueryChat'
import './App.css'
import ThemesDisplay from './component/ThemesDisplay';
import { useEffect, useState } from 'react';


function App() {
  const [detectedThemes, setDetectedThemes] = useState([]);

  useEffect(() => {
    // Fetch detected themes from backend
    fetch("https://mrityunjay-kukreti-wasserstoff.onrender.com/themes")
      .then((res) => res.json())
      .then((data) => setDetectedThemes(data.themes || []))
      .catch((err) => console.error("Error fetching themes:", err));
  }, []);
  return (
    <div className="app-container">
      <div className="left-panel">
        <Uploader />
        <ThemesDisplay themes={detectedThemes} />
      </div>
      <div className="chat-box">
        <QueryChat />
      </div>
    </div>
  );
}
export default App;