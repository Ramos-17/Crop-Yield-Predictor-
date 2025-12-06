import { useEffect } from "react";
import "./layout.css";

export default function Home() {
  useEffect(() => {
    document.title = "Croply";

    const link = document.querySelector("link[rel~='icon']");
    if (link) {
      link.href = "/crop.png";
    }
  }, []);

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
      </div>
    </div>
  );
}
