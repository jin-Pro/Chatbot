/* eslint-disable @typescript-eslint/no-unused-vars */
import { useState } from "react";
import axios from "axios";

export default function QuestionForm() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!question.trim()) return alert("질문을 입력해주세요.");

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const res = await axios.post("http://localhost:8000/ask", {
        question: question.trim(),
      });
      setResponse(res.data);
    } catch (e) {
      setError("서버 요청 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: "auto" }}>
      <h2>질문 입력</h2>
      <textarea
        rows={5}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="질문을 입력하세요"
        style={{ width: "100%", padding: 8, fontSize: 16 }}
      />
      <button
        onClick={handleSubmit}
        disabled={loading}
        style={{ marginTop: 10, padding: "8px 16px", fontSize: 16 }}
      >
        {loading ? "전송 중..." : "질문하기"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {response && (
        <div style={{ marginTop: 20, whiteSpace: "pre-wrap" }}>
          <h3>응답 결과:</h3>
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
