import React, { useState } from "react";

const TradingControls = ({ onTrade }) => {
  const [symbol, setSymbol] = useState("AAPL");
  const [quantity, setQuantity] = useState(1);
  const [duration, setDuration] = useState("1d");

  const handleTrade = () => {
    onTrade({ symbol, quantity, duration });
  };

  return (
    <div className="bg-gray-700 p-4 rounded-xl shadow-md mb-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <input
          type="text"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          placeholder="Symbol"
          className="p-2 rounded-lg bg-gray-800 text-white"
        />
        <input
          type="number"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
          placeholder="Quantity"
          className="p-2 rounded-lg bg-gray-800 text-white"
        />
        <select
          value={duration}
          onChange={(e) => setDuration(e.target.value)}
          className="p-2 rounded-lg bg-gray-800 text-white"
        >
          <option value="1d">1 Day</option>
          <option value="5d">5 Days</option>
          <option value="1mo">1 Month</option>
        </select>
      </div>

      <button
        onClick={handleTrade}
        className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
      >
        Execute Trade
      </button>
    </div>
  );
};

export default TradingControls;
