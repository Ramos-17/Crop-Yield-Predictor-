import { useEffect, useState } from "react";
import "./layout.css";

export default function Home() {
  // Set page title + favicon
  useEffect(() => {
    document.title = "Croply";

    const link = document.querySelector("link[rel~='icon']");
    if (link) {
      link.href = "/crop.png";
    }
  }, []);

  // --- State for form + prediction ---
  const [formData, setFormData] = useState({
    Area: "",
    Item: "",
    average_rain_fall_mm_per_year: "",
    pesticides_tonnes: "",
    avg_temp: "",
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setPrediction(null);

    try {
      const payload = {
        Area: formData.Area,
        Item: formData.Item,
        average_rain_fall_mm_per_year: Number(
          formData.average_rain_fall_mm_per_year
        ),
        pesticides_tonnes: Number(formData.pesticides_tonnes),
        avg_temp: Number(formData.avg_temp),
      };

      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Server error: " + response.status);
      }

      const data = await response.json();
      setPrediction(data.predicted_yield);
    } catch (err) {
      console.error(err);
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="background-image">
      <div className="background-tint">
        <div className="top-header">
          <div className="center-container">
            <div className="logo-div-group">
              <div className="logo-div">
                <img className="logo" src="/crop.png" alt="Crop Logo" />
              </div>
              <div className="header-text-container">
                <h1 className="header">Croply</h1>
                <h2 className="subheader">Crop Prediction Made Easy</h2>
              </div>
            </div>
          </div>
        </div>

        {/* Simple form + prediction area (your teammate can style this later) */}
        <div className="center-container" style={{ padding: "2rem" }}>
          <form onSubmit={handleSubmit} className="prediction-form">
            <div>
              <label>Area (Country):</label>
              <input
                type="text"
                name="Area"
                value={formData.Area}
                onChange={handleChange}
                placeholder="India"
                required
              />
            </div>

            <div>
              <label>Item (Crop):</label>
              <input
                type="text"
                name="Item"
                value={formData.Item}
                onChange={handleChange}
                placeholder="Maize"
                required
              />
            </div>

            <div>
              <label>Average Rainfall (mm/year):</label>
              <input
                type="number"
                name="average_rain_fall_mm_per_year"
                value={formData.average_rain_fall_mm_per_year}
                onChange={handleChange}
                required
              />
            </div>

            <div>
              <label>Pesticides (tonnes):</label>
              <input
                type="number"
                name="pesticides_tonnes"
                value={formData.pesticides_tonnes}
                onChange={handleChange}
                required
              />
            </div>

            <div>
              <label>Average Temperature (°C):</label>
              <input
                type="number"
                name="avg_temp"
                value={formData.avg_temp}
                onChange={handleChange}
                required
              />
            </div>

            <button type="submit" disabled={loading}>
              {loading ? "Predicting..." : "Predict Yield"}
            </button>
          </form>

          {error && <p style={{ color: "red" }}>{error}</p>}

          {prediction !== null && (
            <div style={{ marginTop: "1rem" }}>
              <h2>Predicted Yield</h2>
              <p>{prediction.toFixed(2)} hg/ha</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}