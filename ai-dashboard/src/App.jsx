import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

function App() {
  const [metrics, setMetrics] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [history, setHistory] = useState([]);

  const fetchMetrics = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/metrics");

      setMetrics(res.data);
      setLastUpdated(new Date().toLocaleTimeString());

      // Keep last 10 data points
      setHistory((prev) => [
        ...prev.slice(-9),
        {
          time: new Date().toLocaleTimeString(),
          avg: res.data.average_response_time || 0
        }
      ]);
    } catch (error) {
      console.error("Error fetching metrics:", error);
    }
  };

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  const formatSeconds = (value, precision = 3) =>
    typeof value === "number" ? `${value.toFixed(precision)} sec` : "--";

  const formatPercent = (value, precision = 2) =>
    typeof value === "number" ? `${value.toFixed(precision)}%` : "--";

  if (!metrics)
    return (
      <div className="loading">
        <div className="loading-card">
          <span className="loader" />
          <h2>Loading Dashboard...</h2>
          <p>Fetching live AI metrics</p>
        </div>
      </div>
    );

  return (
    <div className="dashboard">
      <div className="shape shape-left" />
      <div className="shape shape-right" />

      <div className="dashboard-shell">
        <div className="header">
          <div>
            <h1>AI Observability Dashboard</h1>
            <p className="subtitle">
              Live reliability and latency metrics for your AI service.
            </p>
          </div>
          <span className="refresh">Updated: {lastUpdated}</span>
        </div>

        <div className="cards">
          <div className="card glow">
            <h3>Total Requests</h3>
            <p>{metrics.total_requests ?? "--"}</p>
          </div>

          <div className="card">
            <h3>Average Response Time</h3>
            <p>{formatSeconds(metrics.average_response_time)}</p>
          </div>

          <div className="card success">
            <h3>Fastest Request</h3>
            <p>{formatSeconds(metrics.fastest_request)}</p>
          </div>

          <div className="card warning">
            <h3>Slowest Request</h3>
            <p>{formatSeconds(metrics.slowest_request)}</p>
          </div>

          <div className="card danger">
            <h3>Failure Rate</h3>
            <p>{formatPercent(metrics.failure_rate_percent)}</p>
          </div>
        </div>

        <div className="chart-container">
          <div className="chart-header">
            <h2>Response Time Trend</h2>
            <span>Last 10 samples</span>
          </div>

          <ResponsiveContainer width="100%" height={360}>
            <LineChart data={history}>
              <CartesianGrid strokeDasharray="3 3" stroke="#d8dfec" />
              <XAxis dataKey="time" stroke="#7b879e" tickMargin={8} />
              <YAxis
                stroke="#7b879e"
                tickMargin={8}
                tickFormatter={(value) => `${value.toFixed(2)}s`}
              />
              <Tooltip
                contentStyle={{
                  background: "#fffdf8",
                  border: "1px solid #d2d9e6",
                  borderRadius: "12px"
                }}
              />
              <Line
                type="monotone"
                dataKey="avg"
                stroke="#0f766e"
                strokeWidth={3}
                activeDot={{ r: 5, strokeWidth: 0 }}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default App;
