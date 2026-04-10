//THIS FILE CONTAINS THE CODE WHICH ALLOWS USERS TO ADD EMERGENCY CONTACT DETAILS IN THE SIGNUP PAGE 




import React, { useState } from "react";

const Signup = () => {
  const [name, setName] = useState("LEKHA ");
  const [email, setEmail] = useState("123@GMAIL.COM");
  const [password, setPassword] = useState("12345");
  const [emergencyContact, setEmergencyContact] = useState("9090909090");

  const handleSignup = async (e) => {
    e.preventDefault();
    
    const userData = {
      id: Date.now().toString(), // Generate unique ID
      name,
      email,
      password,
      emergency_contact: emergencyContact
    };

    try {
      const response = await fetch("http://localhost:8000/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData),
      });

      if (response.ok) {
        alert("Signup successful!");
      } else {
        alert("Signup failed. Try again.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Something went wrong.");
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white shadow-md rounded-md">
      <h2 className="text-2xl font-bold mb-4">Sign Up</h2>
      <form onSubmit={handleSignup}>
        <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required className="w-full p-2 mb-3 border rounded"/>
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required className="w-full p-2 mb-3 border rounded"/>
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required className="w-full p-2 mb-3 border rounded"/>
        <input type="tel" placeholder="Emergency Contact (Phone Number)" value={emergencyContact} onChange={(e) => setEmergencyContact(e.target.value)} required className="w-full p-2 mb-3 border rounded"/>
        <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded">Sign Up</button>
      </form>
    </div>
  );
};

export default Signup;
