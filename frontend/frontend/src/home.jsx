import { useEffect } from "react";
import "./layout.css";

export default function Home() {
  useEffect(() => {
    document.title = "Crop Yield Predictor";

    const link = document.querySelector("link[rel~='icon']");
    if (link) {
      link.href = "/crop.png";
    }
  }, []);

  return (
    <div>
      <div className="top-header">
        <div className="top-header-logo">
            <h1>
                Hello
            </h1>
            <p>hellooo</p>
            
        </div>
      </div>
    </div>
  );
}
