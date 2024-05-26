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
    content:
      "Hello hackers 🤟 ! I am Pedal, your music effect assistant! 🎶 \n\nImport a track and let's build together! 🚀",
  },
];

import { useRef } from "react";

function cleanString(str: string) {
  // replace all _ by  space and put the first letter in uppercase
  const cleanedStr = str.replace(/_/g, " ");
  return cleanedStr.charAt(0).toUpperCase() + cleanedStr.slice(1);
}

function Chat({
  reloadAudioFile,
  sessionId,
  percentages,
}: {
  reloadAudioFile: () => Promise<void>;
  sessionId: string;
  percentages: [number, number];
}) {
  const [messages, setMessages] = useState<Message[]>(defaultMessages);
  const [currentText, setCurrentText] = useState("");
  const [loading, setLoading] = useState(false);
  const [recommendedTools, setRecommendedTools] = useState<any[]>([]);
  const scrollContainer = useRef<HTMLDivElement>(null);

  async function sendMessage(message: string, visibleText: string) {
    setRecommendedTools([]);
    setCurrentText("");
    setLoading(true);
    setMessages((messages) => [
      ...messages,
      { role: "user", content: visibleText },
    ]);
    const response = await fetch(`/api/${sessionId}/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        messages: [...messages, { role: "user", content: message }],
        percentage_begin: percentages[0],
        percentage_end: percentages[1],
      }),
    });
    if (!response.ok) {
      throw new Error(response.statusText);
    }
    setLoading(false);

    const data = await response.json();
    console.log(data);
    setMessages((messages) => [...messages, data.message]);
    setRecommendedTools(data.tool_recommendations);
    await reloadAudioFile();
  }

  useEffect(() => {
    scrollContainer.current?.scrollTo(0, scrollContainer.current?.scrollHeight);
  }, [messages]);

  function callfunctiontool(myTool: any) {
    sendMessage(
      "USE THE FOLLOWING " + JSON.stringify(myTool.function),
      "Apply the suggested " + cleanString(myTool.function.name).toLowerCase()
    );
  }

  async function rollback() {
    setMessages((messages) => [
      ...messages,
      {
        role: "user",
        content: "Rollback last added effects",
      },
      {
        role: "assistant",
        content: "Ok I will rollback the last added effects",
      },
    ]);
    setRecommendedTools([]);
    const res = await fetch(`/api/${sessionId}/rollback`, {
      method: "POST",
    });
    if (!res.ok) {
      throw new Error(res.statusText);
    }
    await reloadAudioFile();
  }

  return (
    <div className="flex flex-col w-full p-2 relative">
      <span className="text-black text-lg font-bold">AI Chat</span>
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
                  ? "bg-green-600 text-white"
                  : "bg-white text-black"
              } shadow-sm`}
            >
              <p>{message.content}</p>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-center items-center h-full ">
            <div className="flex items-center justify-center">
              <div className="animate-spin">
                <div className="h-4 w-4 border-t-2 border-b-2 border-black"></div>
              </div>
            </div>
          </div>
        )}
      </div>
      {recommendedTools.length > 0 && (
        <div className="flex flex-col items-center justify-center h-full">
          <span>Recommended effects</span>
          <div className="flex flex-col gap-2">
            {recommendedTools.map((tool, index) => (
              <button
                onClick={() => callfunctiontool(tool)}
                key={index}
                className="flex items-center justify-center gap-2"
              >
                <div className="p-2 rounded-lg bg-white text-black shadow-sm">
                  {cleanString(tool.function.name)}
                </div>
              </button>
            ))}
          </div>
        </div>
      )}
      {messages.length > 1 && (
        <div className="pb-2">
          <button
            className=" p-1 rounded-lg border-none bg-black text-white shadow-sm "
            onClick={() => {
              rollback();
            }}
          >
            Rollback last added effects
          </button>
        </div>
      )}
      <div className="flex gap-2">
        <input
          type="text"
          placeholder="Ask me anything regarding music effects ! ✨"
          className="p-2 rounded-lg  bg-white text-black shadow-sm border flex-1"
          value={currentText}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendMessage(currentText, currentText);
            }
          }}
          onChange={(e) => setCurrentText(e.target.value)}
        />
        <button
          disabled={loading}
          className=" p-2 rounded-lg border-none bg-green-600 text-white shadow-sm"
          onClick={() => sendMessage(currentText, currentText)}
        >
          Send
        </button>
      </div>
    </div>
  );
}

import { useEffect } from "react";

import { Donut, Silver, HighContrast, White } from "react-dial-knob";
import Home from "./components/home";

function App() {
  const [blob, setBlob] = useState<Blob>();
  const [sessionId, setSessionId] = useState<string>();
  const [value, setValue] = useState(0);

  async function startNewSession() {
    const res = await fetch("/api");
    const data = await res.json();
    setSessionId(data["session_id"]);

    console.log("start new session", data["session_id"]);
    localStorage.setItem("sessionId", data["session_id"]);
  }

  async function restoreLastSession() {
    const sessionId = localStorage.getItem("sessionId");
    if (sessionId) {
      console.log("restore last session", sessionId);
      setSessionId(sessionId);
      reloadAudioFile();
      // startNewSession();
    }
  }

  useEffect(() => {
    reloadAudioFile();
  }, [sessionId]);

  // useEffect(() => {
  //   if (localStorage.getItem("sessionId")) {
  //     startNewSession();
  //   }
  // }, []);

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
    if (!resFile.ok) {
      throw new Error(resFile.statusText);
    }
    const uploadedfile = await resFile.blob();
    setBlob(uploadedfile);
  }

  const [selectedPercentages, setSelectedPercentages] = useState<
    [number, number]
  >([0, 100]);
  if (!sessionId) {
    return (
      <Home
        startSession={startNewSession}
        restoreSession={restoreLastSession}
      />
    );
    // return (
    //   <div className="flex flex-col items-center gap-2 justify-center h-screen">
    //     <button
    //       className=" p-2 rounded-lg border-none bg-black text-white shadow-sm"
    //       onClick={startNewSession}
    //     >
    //       Start New Session
    //     </button>
    //     <button
    //       className=" p-2 rounded-lg border-none bg-black text-white shadow-sm"
    //       onClick={restoreLastSession}
    //     >
    //       Restore Last Session
    //     </button>
    //   </div>
    // );
  }

  function downloadFile(file: Blob) {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(file);
    a.download = "pedalAi.wav";
    a.click();
  }

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 ">
        {blob ? (
          <Waveform
            audio={blob}
            value={selectedPercentages}
            setValue={setSelectedPercentages}
          />
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
      <div className="relative bg-black">
        <div className="absolute inset-0 flex items-center justify-center h-full w-full">
          <div className="bg-gradient-to-r bg-green-500 to-green-100 blur-[120px] h-[300px] w-[300px] " />
        </div>
        <div className="relative">
          <button
            disabled={!blob}
            onClick={() => {
              if (!blob) {
                return;
              }
              downloadFile(blob);
            }}
            className=" p-2 rounded-lg border-none bg-green-600 text-white shadow-sm"
          >
            Download
          </button>
        </div>
        <Chat
          reloadAudioFile={reloadAudioFile}
          sessionId={sessionId}
          percentages={selectedPercentages}
        />
      </div>
    </div>
  );
}

export default App;
