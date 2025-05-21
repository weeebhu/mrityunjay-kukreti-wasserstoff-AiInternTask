import React, { useState } from "react";
import './QueryChat.css';

export default function QueryChat() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

const handleQuery = async () => {
  if (!query) return;
  setLoading(true);
  try {
    const res = await fetch("https://mrityunjay-kukreti-wasserstoff.onrender.com/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, top_k: 5 })
    });

    console.log("Raw response:", res);
    if (!res.ok) {
      const errorText = await res.text();
      console.error("Server Error:", errorText);
      return;
    }

    const data = await res.json();
    console.log("Parsed response:", data);
    setAnswer(data.answer);
    setSources(data.sources);
  } catch (err) {
    console.error("Error fetching answer:", err);
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Research Chatbot</h1>
      <textarea
        className="w-full p-4 border rounded mb-4"
        rows="4"
        placeholder="Ask a research question..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      ></textarea>
      <button
        className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
        onClick={handleQuery}
        disabled={loading}
      >
        {loading ? "Thinking..." : "Submit Query"}
      </button>

      {answer && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold mb-2">Answer:</h2>
          <p className="bg-gray-100 p-4 rounded whitespace-pre-wrap">{answer}</p>

          <h3 className="text-lg mt-4">Sources:</h3>
          <ul className="list-disc list-inside">
            {sources.map((src, idx) => (
              <li key={idx}>{src}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}