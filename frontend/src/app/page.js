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
      const response = await fetch(
        "https://customer-intelligence-platform-1.onrender.com/predict",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            recency_days: Number(recency),
            frequency: Number(frequency),
            monetary: Number(monetary),
          }),
        }
      );

      const data = await response.json();
      setResult(data);
    } catch (error) {
      alert("Error connecting to backend");
    }

    setLoading(false);
  };

  const riskColor =
    result?.risk_level === "High"
      ? "bg-red-100 text-red-700"
      : result?.risk_level === "Medium"
      ? "bg-yellow-100 text-yellow-700"
      : "bg-green-100 text-green-700";

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4">
      <div className="bg-white w-full max-w-lg rounded-2xl shadow-xl p-8">
        {/* Header */}
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-2">
          Customer Churn Prediction
        </h1>
        <p className="text-center text-gray-500 mb-8">
          Enter customer behavior metrics to predict churn risk
        </p>

        {/* Inputs */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Recency (days since last transaction)
            </label>
            <input
              type="number"
              className="w-full rounded-lg border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={recency}
              onChange={(e) => setRecency(e.target.value)}
              placeholder="e.g. 90"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Frequency (number of purchases)
            </label>
            <input
              type="number"
              className="w-full rounded-lg border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={frequency}
              onChange={(e) => setFrequency(e.target.value)}
              placeholder="e.g. 1"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Monetary Value (total spend)
            </label>
            <input
              type="number"
              className="w-full rounded-lg border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={monetary}
              onChange={(e) => setMonetary(e.target.value)}
              placeholder="e.g. 1200"
            />
          </div>
        </div>

        {/* Button */}
        <button
          onClick={handlePredict}
          disabled={loading}
          className="w-full mt-6 bg-blue-600 text-white py-3 rounded-xl font-semibold hover:bg-blue-700 transition disabled:opacity-60"
        >
          {loading ? "Predicting..." : "Predict Churn"}
        </button>

        {/* Results */}
        {result && (
          <div className="mt-8 border-t pt-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
              Prediction Result
            </h2>

            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Churn Prediction</span>
                <span className="font-semibold">
                  {result.churn_prediction === 1 ? "Yes" : "No"}
                </span>
              </div>

              <div className="flex justify-between">
                <span className="text-gray-600">Churn Probability</span>
                <span className="font-semibold">
                  {result.churn_probability}
                </span>
              </div>

              <div
                className={`mt-4 text-center py-2 rounded-lg font-semibold ${riskColor}`}
              >
                Risk Level: {result.risk_level}
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
