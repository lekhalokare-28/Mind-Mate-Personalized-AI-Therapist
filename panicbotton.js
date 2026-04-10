import React, { useState } from "react";

const PanicButton = () => {
  const [isConfirming, setIsConfirming] = useState(false);

  const sendPanicAlert = async () => {
    try {
      const response = await fetch("http://localhost:8000/send_alert", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId: "user_123" }), // Replace with actual user ID
      });
  
      if (response.ok) {
        alert("Emergency alert sent!");
      } else {
        alert("Failed to send alert. Try again.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error sending alert.");
    }
  };
  

  return (
    <div className="fixed bottom-5 right-5">
      {isConfirming ? (
        <div className="bg-red-500 text-white p-3 rounded-lg">
          <p>Are you sure?</p>
          <button className="bg-white text-red-500 px-3 py-1 rounded" onClick={sendPanicAlert}>Yes</button>
          <button className="ml-2 text-white" onClick={() => setIsConfirming(false)}>No</button>
        </div>
      ) : (
        <button
          className="bg-red-600 text-white px-4 py-2 rounded-full shadow-lg hover:bg-red-700"
          onClick={() => setIsConfirming(true)}
        >
          🚨 Panic Button
        </button>
      )}
    </div>
  );
};

export default PanicButton;
