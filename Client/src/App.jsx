import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import ResultBox from "./components/ResultBox";

import "./App.css";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="container">
      <UploadForm onResult={setResult} />
      <ResultBox result={result} />
    </div>
  );
}

export default App;
