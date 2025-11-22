export async function evaluateCandidate(formData) {
  const response = await fetch("http://localhost:8090/evaluate", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`HTTP error: ${response.status}`);
  }

  return await response.json();
}
