import React from "react";

function ResultBox({ result }) {
  if (!result) return null;

  return (
    <div className="result-card">
      <h3>Result</h3>
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
}

export default ResultBox;