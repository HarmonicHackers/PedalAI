import { useState } from "react";
// import reactLogo from "./assets/react.svg";
// import viteLogo from "/vite.svg";
import "./App.css";

import Waveform from "./components/waveform";

type Message = {
  role: "user" | "assistant";
  content: string;
};

const defaultMessages: Message[] = [
  {
    role: "assistant",
    content: "Hello I am pedalAI assistant",
  },
];

function Chat({ reloadAudioFile }: { reloadAudioFile: () => Promise<void> }) {
  const [messages, setMessages] = useState<Message[]>(defaultMessages);
  const [currentText, setCurrentText] = useState("");

  async function sendMessage(message: string) {
    setMessages([...messages, { role: "user", content: message }]);
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        messages,
      }),
    });
    if (!response.ok) {
      throw new Error(response.statusText);
    }

    const data = await response.json();
    setMessages([...messages, data.message]);
    await reloadAudioFile();
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", width: "100%" }}>
      {messages.map((message, index) => (
        <div
          key={index}
          style={{
            display: "flex",
            justifyContent: message.role === "user" ? "flex-end" : "flex-start",
            color: message.role === "user" ? "#000" : "#000",
            margin: "10px 0",
          }}
        >
          <div
            style={{
              maxWidth: "60%",
              padding: "10px",
              borderRadius: "10px",
              backgroundColor: message.role === "user" ? "#DCF8C6" : "#FFF",
              color: message.role === "user" ? "#000" : "#000",
              boxShadow: "0 1px 2px rgba(0, 0, 0, 0.1)",
            }}
          >
            {message.content}
          </div>
        </div>
      ))}
      <input
        type="text"
        style={{
          // width: "100%",
          padding: "10px",
          borderRadius: "10px",
          border: "none",
          backgroundColor: "#FFF",
          color: "#000",
          boxShadow: "0 1px 2px rgba(0, 0, 0, 0.1)",
        }}
        onChange={(e) => setCurrentText(e.target.value)}
      />
      <button
        style={{
          width: "100%",
          padding: "10px",
          borderRadius: "10px",
          border: "none",
          backgroundColor: "#000",
          color: "#FFF",
          boxShadow: "0 1px 2px rgba(0, 0, 0, 0.1)",
        }}
        onClick={() => sendMessage(currentText)}
      >
        Send
      </button>
    </div>
  );
}

import { useEffect } from "react";

function App() {
  const [blob, setBlob] = useState<Blob>();
  const [sessionId, setSessionId] = useState<string>();

  useEffect(() => {
    async function fetchSessionId() {
      const res = await fetch("/api");
      const data = await res.json();
      setSessionId(data["session_id"]);
    }
    fetchSessionId();
  }, []);

  async function uploadFile(file: File) {
    var data = new FormData();
    data.append("file", file);
    const res = await fetch(`/api/${sessionId}/upload`, {
      method: "POST",
      body: data,
    });
    if (!res.ok) {
      throw new Error(res.statusText);
    }

    await reloadAudioFile();
  }

  async function reloadAudioFile() {
    const resFile = await fetch("/api/download", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const uploadedfile = await resFile.blob();
    setBlob(uploadedfile);
  }

  if (!sessionId) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gridGap: "10px",
          padding: "10px",
          width: "calc(100vw - 20px)",
        }}
      >
        <div>
          <input
            type="file"
            accept="audio/*"
            onChange={(e) => {
              if (e.target.files && e.target.files[0]) {
                uploadFile(e.target.files[0]);
              }
            }}
          />
          {blob && <Waveform audio={blob} />}
        </div>
        <div>
          <Chat reloadAudioFile={reloadAudioFile} />
        </div>
      </div>
    </div>
  );
}

export default App;
