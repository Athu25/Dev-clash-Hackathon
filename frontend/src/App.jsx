import React from "react";
import CandlestickChart from "./components/CandlestickChart";
import "./index.css";

const App = () => {
  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-4xl font-bold mb-6 text-center">Trading Dashboard</h1>

      <div className="max-w-6xl mx-auto bg-gray-800 p-6 rounded-2xl shadow-lg">
        <div className="bg-blue-500 text-white p-4 text-center">Chart Should Render Below 👇</div>
        <CandlestickChart />
      </div>
    </div>
  );
};

export default App;
