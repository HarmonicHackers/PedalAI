import { useState } from "react";
// import reactLogo from "./assets/react.svg";
// import viteLogo from "/vite.svg";

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

import { useRef } from "react";

function Chat({
  reloadAudioFile,
  sessionId,
}: {
  reloadAudioFile: () => Promise<void>;
  sessionId: string;
}) {
  const [messages, setMessages] = useState<Message[]>(defaultMessages);
  const [currentText, setCurrentText] = useState("");
  const scrollContainer = useRef<HTMLDivElement>(null);

  async function sendMessage(message: string) {
    setCurrentText("");
    setMessages((messages) => [
      ...messages,
      { role: "user", content: message },
    ]);
    const response = await fetch(`/api/${sessionId}/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        messages: [...messages, { role: "user", content: currentText }],
      }),
    });
    if (!response.ok) {
      throw new Error(response.statusText);
    }

    const data = await response.json();
    setMessages((messages) => [...messages, data.message]);
    scrollContainer.current?.scrollTo(0, scrollContainer.current?.scrollHeight);
    await reloadAudioFile();
  }

  return (
    <div className="flex flex-col w-full">
      <div
        ref={scrollContainer}
        className="flex flex-col w-full h-72 overflow-y-scroll"
      >
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${
              message.role === "user" ? "justify-end" : "justify-start"
            } my-2`}
          >
            <div
              className={`max-w-[60%] p-2 rounded-lg ${
                message.role === "user"
                  ? "bg-[#DCF8C6] text-black"
                  : "bg-white text-black"
              } shadow-sm`}
            >
              {message.content}
            </div>
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          type="text"
          className="p-2 rounded-lg  bg-white text-black shadow-sm border flex-1"
          value={currentText}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendMessage(currentText);
            }
          }}
          onChange={(e) => setCurrentText(e.target.value)}
        />
        <button
          className=" p-2 rounded-lg border-none bg-black text-white shadow-sm"
          onClick={() => sendMessage(currentText)}
        >
          Send
        </button>
      </div>
    </div>
  );
}

import { useEffect } from "react";

import { Donut, Silver, HighContrast, White } from "react-dial-knob";

function App() {
  const [blob, setBlob] = useState<Blob>();
  const [sessionId, setSessionId] = useState<string>();
  const [value, setValue] = useState(0);

  useEffect(() => {
    async function fetchSessionId() {
      const res = await fetch("/api");
      const data = await res.json();
      setSessionId(data["session_id"]);
    }
    fetchSessionId();
  }, []);

  async function uploadFile(file: File) {
    const data = new FormData();
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
    const resFile = await fetch(`/api/${sessionId}/download`);
    const uploadedfile = await resFile.blob();
    setBlob(uploadedfile);
  }

  if (!sessionId) {
    return <div>Loading...</div>;
  }

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 ">
        {blob ? (
          <Waveform audio={blob} />
        ) : (
          <div className="flex flex-col items-center justify-center h-full">
            <span>Choose a file to upload or drag and drop a file here</span>
            <input
              type="file"
              accept="audio/*"
              onChange={(e) => {
                if (e.target.files && e.target.files[0]) {
                  uploadFile(e.target.files[0]);
                }
              }}
            />
          </div>
        )}
      </div>
      <div className="flex-1 bg-zinc-100 grid grid-cols-2 gap-2">
        <div className="flex flex-col gap-4 p-5">
          <div className="bg-white p-2 rounded-lg text-black flex items-center justify-between shadow-sm">
            <span>EffectName</span>
            <div className="flex items-center gap-2">
              <White
                diameter={60}
                min={0}
                max={100}
                step={1}
                value={value}
                onValueChange={setValue}
                ariaLabelledBy={"my-label"}
                style={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                }}
              >
                <label className="text-center" id={"my-label"}>
                  Some label
                </label>
              </White>
            </div>
          </div>
        </div>

        <Chat reloadAudioFile={reloadAudioFile} sessionId={sessionId} />
      </div>
    </div>
  );
}

export default App;
