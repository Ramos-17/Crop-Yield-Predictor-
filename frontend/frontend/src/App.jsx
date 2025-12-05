import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./home";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Initial screen (homepage) */}
        <Route path="/" element={<Home />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
