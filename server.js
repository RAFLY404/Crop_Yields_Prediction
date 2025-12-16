const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const { spawn } = require("child_process");
const { Pool } = require("pg");
require("dotenv").config();

const app = express();
app.use(cors());
app.use(bodyParser.json());

// DATABASE CONFIG
const pool = new Pool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_DATABASE,
  port: process.env.DB_PORT,
});

async function savePrediction(prediction, area, items, year) {
  await pool.query("INSERT INTO predictions (prediction_value, area, items, year) VALUES ($1, $2, $3, $4)", [prediction , area, items, year]);
}

app.post("/predict", (req, res) => {
  const python = spawn("python", ["predict.py"]);

  let output = "";
  let errorOutput = "";

  python.stdin.write(JSON.stringify(req.body));
  python.stdin.end();


  python.stdout.on("data", (data) => {
    output += data.toString();
  });

  python.stderr.on("data", (data) => {
    errorOutput += data.toString();
  });

  python.on("close", async () => {
    if (errorOutput.trim()) {
      return res.status(500).json({ python_error: errorOutput });
    }

    try {
      const result = JSON.parse(output.trim());

      await savePrediction(result.prediction , req.body.Area, req.body.Item, req.body.Year );

      return res.json(result);
    } catch (err) {
      return res.status(500).json({
        node_error: "Invalid JSON from Python",
        raw_output: output,
      });
    }
  });

  python.on("error", (err) => {
    return res.status(500).json({ python_start_error: err.message });
  });
});

app.get("/get-prediction", async (req, res) => {
  try {
    const result = await pool.query("SELECT * FROM predictions ORDER BY created_at DESC");

    res.json(result.rows);
  } catch (err) {
    console.error("Error executing query", err.stack);
    res.status(500).json({ error: "Failed to fetch prediction" });
  }
});

app.listen(5000, () => {
  console.log("Server running on http://localhost:5000");
});
