"use client";

import { useState } from "react";

export default function Home() {
  const [recency, setRecency] = useState("");
  const [frequency, setFrequency] = useState("");
  const [monetary, setMonetary] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("https://customer-intelligence-platform-1.onrender.com/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          recency_days: Number(recency),
          frequency: Number(frequency),
          monetary: Number(monetary),
        }),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      alert("Error connecting to backend");
    }

    setLoading(false);
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6 text-center">
          Customer Churn Prediction
        </h1>

        <input
          type="number"
          placeholder="Recency (days)"
          className="w-full p-2 mb-3 border rounded"
          value={recency}
          onChange={(e) => setRecency(e.target.value)}
        />

        <input
          type="number"
          placeholder="Frequency"
          className="w-full p-2 mb-3 border rounded"
          value={frequency}
          onChange={(e) => setFrequency(e.target.value)}
        />

        <input
          type="number"
          placeholder="Monetary Value"
          className="w-full p-2 mb-4 border rounded"
          value={monetary}
          onChange={(e) => setMonetary(e.target.value)}
        />

        <button
          onClick={handlePredict}
          className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
          disabled={loading}
        >
          {loading ? "Predicting..." : "Predict Churn"}
        </button>

        {result && (
          <div className="mt-6 p-4 bg-gray-50 border rounded">
            <p>
              <strong>Churn Prediction:</strong>{" "}
              {result.churn_prediction === 1 ? "Yes" : "No"}
            </p>
            <p>
              <strong>Churn Probability:</strong>{" "}
              {result.churn_probability}
            </p>
          </div>
        )}
      </div>
    </main>
  );
}
