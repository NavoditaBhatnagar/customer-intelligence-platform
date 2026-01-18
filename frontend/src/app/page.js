"use client";

import { useState } from "react";

export default function Home() {
  const [recency, setRecency] = useState("");
  const [frequency, setFrequency] = useState("");
  const [monetary, setMonetary] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(
        "https://customer-intelligence-platform-1.onrender.com/predict",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
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

  const riskStyles = {
    High: "bg-red-100 text-red-700 border-red-300",
    Medium: "bg-yellow-100 text-yellow-700 border-yellow-300",
    Low: "bg-green-100 text-green-700 border-green-300",
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <div className="w-full max-w-lg bg-white rounded-2xl shadow-xl p-8 text-gray-900">
        {/* Header */}
        <h1 className="text-3xl font-bold text-center mb-2">
          Customer Churn Prediction
        </h1>
        <p className="text-center text-gray-600 mb-8">
          Predict whether a customer is likely to churn
        </p>

        {/* Inputs */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-semibold mb-1">
              Recency (days)
            </label>
            <input
              type="number"
              placeholder="90"
              className="w-full rounded-lg border border-gray-300 px-3 py-2 bg-white text-gray-900 placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              value={recency}
              onChange={(e) => setRecency(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-1">
              Frequency
            </label>
            <input
              type="number"
              placeholder="1"
              className="w-full rounded-lg border border-gray-300 px-3 py-2 bg-white text-gray-900 placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              value={frequency}
              onChange={(e) => setFrequency(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-1">
              Monetary Value
            </label>
            <input
              type="number"
              placeholder="1200"
              className="w-full rounded-lg border border-gray-300 px-3 py-2 bg-white text-gray-900 placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              value={monetary}
              onChange={(e) => setMonetary(e.target.value)}
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
            <h2 className="text-xl font-semibold mb-4">
              Prediction Result
            </h2>

            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span>Churn Prediction</span>
                <span className="font-bold">
                  {result.churn_prediction === 1 ? "Yes" : "No"}
                </span>
              </div>

              <div className="flex justify-between">
                <span>Churn Probability</span>
                <span className="font-bold">
                  {(result.churn_probability * 100).toFixed(1)}%
                </span>
              </div>

              {/* Probability Bar */}
              <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                <div
                  className="h-3 bg-blue-600"
                  style={{
                    width: `${result.churn_probability * 100}%`,
                  }}
                />
              </div>

              {/* Risk Badge */}
              <div
                className={`mt-4 text-center py-2 rounded-lg border font-semibold ${
                  riskStyles[result.risk_level]
                }`}
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
