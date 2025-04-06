import React from "react";
import CandlestickChart from "./components/CandleStickChart";
import "./index.css";

const App = () => {
  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-4xl font-bold mb-6 text-center">Trading Dashboard</h1>

      
        <CandlestickChart />
    </div>
  );
};

export default App;
