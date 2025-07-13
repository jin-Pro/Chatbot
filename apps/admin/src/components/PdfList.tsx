import { useEffect, useState } from "react";
import axios from "axios";

interface PdfFile {
  filename: string;
  size_bytes: number;
}

export default function PdfList() {
  const [files, setFiles] = useState<PdfFile[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    axios
      .get<{ files: PdfFile[] }>("http://localhost:8000/list-pdfs")
      .then((res) => {
        setFiles(res.data.files);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Failed to fetch files");
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading PDF files...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>PDF Files</h2>
      {files.length === 0 ? (
        <p>No PDF files found.</p>
      ) : (
        <ul>
          {files.map(({ filename, size_bytes }) => (
            <li key={filename}>
              <button
                onClick={() =>
                  axios.delete(`http://localhost:8000/delete-pdf/${filename}`)
                }
              >
                X
              </button>
              <strong>{filename}</strong> - {(size_bytes / 1024).toFixed(2)} KB
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
