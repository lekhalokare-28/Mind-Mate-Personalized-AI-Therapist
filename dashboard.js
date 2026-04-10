//This React component:
//Fetches mood ratings from the backend
//Updates the dashboard dynamically
//Displays a line graph of mood changes over 7 days


import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import "chart.js/auto";

const Dashboard = ({ userId }) => {
  const [moodData, setMoodData] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:8000/weekly_mood/${userId}`)
      .then((res) => res.json())
      .then((data) => {
        setMoodData(data.weekly_mood);
      })
      .catch((err) => console.error("Error fetching mood data:", err));
  }, [userId]); // Re-fetch data when userId changes

  // Prepare data for the chart
  const dates = moodData.map((entry) => new Date(entry.date).toLocaleDateString());
  const moods = moodData.map((entry) => entry.mood);

  const chartData = {
    labels: dates,
    datasets: [
      {
        label: "Mood Rating (1-10)",
        data: moods,
        fill: false,
        backgroundColor: "blue",
        borderColor: "blue",
      },
    ],
  };

  return (
    <div className="max-w-lg mx-auto p-6 bg-white shadow-md rounded-md">
      <h2 className="text-2xl font-bold mb-4">Your Weekly Mood Analysis</h2>
      {moodData.length > 0 ? (
        <Line data={chartData} />
      ) : (
        <p>No mood data available for this week.</p>
      )}
    </div>
  );
};

export default Dashboard;
