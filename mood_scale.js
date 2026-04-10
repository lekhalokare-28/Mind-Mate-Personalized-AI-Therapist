import React, { useState } from "react";

const moodEmojis = [
  { value: 1, emoji: "😞", label: "Very Sad" },
  { value: 2, emoji: "😟", label: "Sad" },
  { value: 3, emoji: "😔", label: "Down" },
  { value: 4, emoji: "😐", label: "Neutral" },
  { value: 5, emoji: "🙂", label: "Slightly Happy" },
  { value: 6, emoji: "😊", label: "Happy" },
  { value: 7, emoji: "😀", label: "Very Happy" },
  { value: 8, emoji: "😄", label: "Excited" },
  { value: 9, emoji: "😁", label: "Overjoyed" },
  { value: 10, emoji: "🤩", label: "Ecstatic" },
];

const JournalPage = ({ userId }) => {
  const [journalEntry, setJournalEntry] = useState("");
  const [mood, setMood] = useState(null); // No default selection

  const handleSubmit = async () => {
    if (mood === null) {
      alert("Please select a mood.");
      return;
    }

    const moodData = {
      userId,
      journalEntry,
      mood,
      timestamp: new Date().toISOString(),
    };

    try {
      const response = await fetch("http://localhost:8000/submit_mood", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(moodData),
      });

      if (response.ok) {
        alert("Mood and journal entry saved!");
        setJournalEntry("");
        setMood(null);
      } else {
        alert("Failed to save data.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Something went wrong.");
    }
  };

  return (
    <div className="max-w-lg mx-auto p-6 bg-white shadow-md rounded-md">
      <h2 className="text-2xl font-bold mb-4">Journal Your Thoughts</h2>
      <textarea
        className="w-full p-2 border rounded mb-3"
        rows="5"
        placeholder="Write about your day..."
        value={journalEntry}
        onChange={(e) => setJournalEntry(e.target.value)}
      />
      
      <label className="block font-semibold mb-2">Select Your Mood</label>
      <div className="flex justify-between mb-3">
        {moodEmojis.map((item) => (
          <button
            key={item.value}
            onClick={() => setMood(item.value)}
            className={`p-2 rounded-full w-12 h-12 text-xl ${
              mood === item.value ? "bg-blue-500 text-white" : "bg-gray-200"
            }`}
            title={item.label}
          >
            {item.emoji}
          </button>
        ))}
      </div>

      <button onClick={handleSubmit} className="w-full bg-blue-500 text-white py-2 rounded mt-3">
        Submit
      </button>
    </div>
  );
};

export default JournalPage;
