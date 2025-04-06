import React, { useEffect, useState } from "react";
import {
  ChartCanvas,
  Chart,
  CandlestickSeries,
  XAxis,
  YAxis,
  EdgeIndicator,
  CrossHairCursor,
  MouseCoordinateX,
  MouseCoordinateY,
  OHLCTooltip,
  discontinuousTimeScaleProvider,
  LineSeries,
} from "react-financial-charts";
import { format } from "d3-format";
import { timeFormat } from "d3-time-format";

const generateCandle = (baseDate, offset) => {
  const date = new Date(baseDate);
  date.setDate(date.getDate() + offset);
  const open = 100 + Math.sin(offset / 5) * 10 + Math.random() * 5;
  const close = open + (Math.random() - 0.5) * 10;
  const high = Math.max(open, close) + Math.random() * 5;
  const low = Math.min(open, close) - Math.random() * 5;
  const volume = Math.floor(Math.random() * 2000 + 500);
  return { date, open, high, low, close, volume };
};

const CandlestickChart = () => {
  const [fullData, setFullData] = useState(() =>
    Array.from({ length: 60 }, (_, i) => generateCandle(new Date(2024, 0, 1), i))
  );
  const [visibleRange, setVisibleRange] = useState("1M");
  const [timeframe, setTimeframe] = useState("1min");
  const [buyPoint, setBuyPoint] = useState(null);
  const [sellPoint, setSellPoint] = useState(null);

  useEffect(() => {
    const interval = setInterval(() => {
      setFullData((prev) => [
        ...prev.slice(-99),
        generateCandle(prev[prev.length - 1].date, 1),
      ]);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const filteredData = (() => {
    if (visibleRange === "1W") return fullData.slice(-7);
    if (visibleRange === "1M") return fullData.slice(-30);
    if (visibleRange === "3M") return fullData.slice(-90);
    return fullData;
  })();

  const xScaleProvider = discontinuousTimeScaleProvider.inputDateAccessor((d) => d.date);
  const { data, xScale, xAccessor, displayXAccessor } = xScaleProvider(filteredData);

  const start = xAccessor(data[0]);
  const end = xAccessor(data[data.length - 1]);
  const xExtents = [start, end + 1];

  const handleBuy = () => {
    const lastCandle = data[data.length - 1];
    setBuyPoint({ date: lastCandle.date, price: lastCandle.close });
    setSellPoint(null);
  };

  const handleSell = () => {
    const lastCandle = data[data.length - 1];
    setSellPoint({ date: lastCandle.date, price: lastCandle.close });
  };

  const profitLoss =
    buyPoint && sellPoint ? (sellPoint.price - buyPoint.price).toFixed(2) : null;

  return (
    <div className="p-6 border rounded-2xl bg-white shadow-xl max-w-[1100px] mx-auto">
      <div className="flex flex-wrap justify-between items-center mb-6 gap-4">
        <div className="flex items-center gap-2">
          <label className="font-semibold">Timeline:</label>
          <select
            value={timeframe}
            onChange={(e) => setTimeframe(e.target.value)}
            className="border px-3 py-1 rounded-md text-sm"
          >
            <option value="1min">1min</option>
            <option value="5min">5min</option>
            <option value="15min">15min</option>
            <option value="1H">1H</option>
            <option value="1D">1D</option>
          </select>
        </div>

        <div className="flex gap-2">
          {["1W", "1M", "3M", "ALL"].map((range) => (
            <button
              key={range}
              onClick={() => setVisibleRange(range)}
              className={`px-4 py-1 rounded-lg border text-sm font-medium ${
                visibleRange === range
                  ? "bg-blue-600 text-white"
                  : "bg-gray-100 hover:bg-gray-200"
              }`}
            >
              {range}
            </button>
          ))}
        </div>

        <div className="flex gap-3">
          <button
            onClick={handleBuy}
            className="bg-green-600 hover:bg-green-700 text-white px-5 py-1.5 rounded-lg text-sm font-semibold"
          >
            Buy
          </button>
          <button
            onClick={handleSell}
            className="bg-red-600 hover:bg-red-700 text-white px-5 py-1.5 rounded-lg text-sm font-semibold"
          >
            Sell
          </button>
        </div>
      </div>

      {profitLoss && (
        <div
          className={`text-sm font-medium mb-4 ${
            profitLoss >= 0 ? "text-green-600" : "text-red-600"
          }`}
        >
          Profit/Loss: {profitLoss}
        </div>
      )}

      <ChartCanvas
        height={500}
        width={1000}
        ratio={1}
        margin={{ left: 50, right: 50, top: 10, bottom: 30 }}
        data={data}
        xScale={xScale}
        xAccessor={xAccessor}
        displayXAccessor={displayXAccessor}
        xExtents={xExtents}
      >
        <Chart id={1} yExtents={(d) => [d.high, d.low]}>
          <XAxis showGridLines gridLinesStroke="#eee" />
          <YAxis showGridLines gridLinesStroke="#eee" />
          <MouseCoordinateX displayFormat={timeFormat("%Y-%m-%d")} />
          <MouseCoordinateY displayFormat={format(".2f")} />
          <CandlestickSeries />
          <EdgeIndicator
            itemType="last"
            orient="right"
            edgeAt="right"
            yAccessor={(d) => d.close}
            fill={(d) => (d.close > d.open ? "#6BA583" : "#FF0000")}
          />
          <OHLCTooltip origin={[0, 0]} />
          {buyPoint && (
            <LineSeries yAccessor={() => buyPoint.price} stroke="green" strokeDasharray="4 2" />
          )}
          {sellPoint && (
            <LineSeries yAccessor={() => sellPoint.price} stroke="red" strokeDasharray="4 2" />
          )}
        </Chart>

        <CrossHairCursor />
      </ChartCanvas>
    </div>
  );
};

export default CandlestickChart;
