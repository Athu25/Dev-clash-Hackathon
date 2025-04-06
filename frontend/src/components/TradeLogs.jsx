import React from "react";

const TradeLogs = ({ logs }) => {
  return (
    <div className="bg-gray-700 p-4 rounded-xl shadow-md mt-6">
      <h2 className="text-xl font-semibold mb-2">Trade Logs</h2>
      <ul className="space-y-2 max-h-48 overflow-y-auto">
        {logs.map((log, index) => (
          <li key={index} className="bg-gray-800 p-2 rounded-md">
            {log.symbol.toUpperCase()} | Qty: {log.quantity} | Duration: {log.duration}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TradeLogs;
