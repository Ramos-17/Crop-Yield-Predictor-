import { useEffect } from "react";

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
      <h1>Crop Yield Predictor </h1>
      <p>This is the homepage</p>
    </div>
  );
}
