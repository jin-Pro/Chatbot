import React, { useState } from "react";
import axios from "axios";

function FileUploader() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files?.[0]) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("파일을 업로드하세요.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await axios.post(
        "http://localhost:8000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      console.log("✅ 업로드 성공:", response.data);
    } catch (error) {
      console.error("❌ 업로드 실패:", error);
    }
  };

  return (
    <div>
      <h2>파일 업로드</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>업로드</button>
    </div>
  );
}

export default FileUploader;
