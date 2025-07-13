import { useEffect, useState } from "react";
// import viteLogo from "/vite.svg";
import axios from "axios";

function App() {
  const [text, setText] = useState("");

  useEffect(() => {
    axios.get<string>("http://localhost:8000").then((res) => {
      console.log("res : ", res);
      setText(res.data);
    });
  }, []);

  return <div>{text}</div>;
}

export default App;
