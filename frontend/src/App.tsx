import axios from "axios";
import { useState } from "react";

function App() {
  const [question, setQuestion] = useState<string>("");
  const [answer, setAnswer] = useState<string>("");
  const [context, setContext] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const handleClick = async (): Promise<void> => {
     if (!question.trim()) return;

    try {
          setLoading(true);
          setAnswer("");
          setContext([]);
          const response = await axios.post(
            "http://127.0.0.1:8000/ask",
            { question }
          );

          setAnswer(response.data.answer);
          setContext(response.data.retrieved_context);
          console.log("Backend response:", response.data);
      } catch (error) {
            console.error("Error calling backend:", error);
      }finally {
            setLoading(false);
      }
  };

  return (
  <div className="container">
    <h1>AI RAG Research Assistant</h1>

    <div className="card">
      <h3>Ask a Question</h3>

      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask something about RAG..."
      />

      <button onClick={handleClick} disabled={loading}>
        {loading ? "Generating..." : "Ask"}
      </button>
    </div>

    {answer && (
      <div className="card">
        <h3>Answer</h3>
        <p>{answer}</p>
      </div>
    )}

    {context.length > 0 && (
      <div className="card">
        <h4>Retrieved Context</h4>
        <ul>
          {context.map((doc, index) => (
            <li key={index}>{doc}</li>
          ))}
        </ul>
      </div>
    )}
  </div>
);
}

export default App;