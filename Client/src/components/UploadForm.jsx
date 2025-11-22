import React, { useState } from "react";
import { evaluateCandidate } from "../Api";

function UploadForm({ onResult }) {
  const [jdName, setJdName] = useState("");
  const [jdFile, setJdFile] = useState(null);
  const [resumeFile, setResumeFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const submitForm = async () => {
    if (!jdName || !jdFile || !resumeFile) {
      alert("Please fill all fields");
      return;
    }

    const formData = new FormData();
    formData.append("jd_name", jdName);
    formData.append("jd_file", jdFile);
    formData.append("resume_file", resumeFile);

    setLoading(true);

    try {
      const data = await evaluateCandidate(formData);
      onResult(data);
    } catch (err) {
      onResult({ error: err.message });
    }

    setLoading(false);
  };

  return (
    <div className="card">
      <h2>JD–Resume Evaluator</h2>

      <label>JD Name</label>
      <input
        type="text"
        value={jdName}
        onChange={(e) => setJdName(e.target.value)}
        placeholder="e.g., python_dev_2025"
      />

      <label>Upload Job Description (PDF)</label>
      <input type="file" accept="application/pdf" onChange={(e) => setJdFile(e.target.files[0])} />

      <label>Upload Resume (PDF)</label>
      <input type="file" accept="application/pdf" onChange={(e) => setResumeFile(e.target.files[0])} />

      <button onClick={submitForm} disabled={loading}>
        {loading ? "Processing..." : "Evaluate"}
      </button>
    </div>
  );
}

export default UploadForm;
