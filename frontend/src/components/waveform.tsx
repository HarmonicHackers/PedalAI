import React, { useState, useEffect, useRef } from "react";
// import PropTypes from "prop-types";
import WaveSurfer from "wavesurfer.js";
import { FaPlayCircle, FaPauseCircle } from "react-icons/fa";

const Waveform = ({ audio }: { audio: Blob }) => {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const waveSurferRef = useRef<WaveSurfer | null>(null);
  const [isPlaying, toggleIsPlaying] = useState(false);

  useEffect(() => {
    const waveSurfer = WaveSurfer.create({
      container: containerRef.current!,
      barWidth: 2,
      barHeight: 1,
      width: containerRef.current!.clientWidth,
    });
    waveSurfer.loadBlob(audio);
    // waveSurfer.load(audio);
    waveSurfer.on("ready", () => {
      waveSurferRef.current = waveSurfer;
    });

    return () => {
      waveSurfer.destroy();
    };
  }, [audio]);

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "40px 1fr",
        alignItems: "center",
        // backgroundColor: "white",
        width: "100%",
      }}
    >
      <button
        style={{
          padding: 2,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: "white",
          color: "black",
        }}
        onClick={() => {
          if (!waveSurferRef.current) {
            throw new Error("WaveSurfer is not ready");
          }
          waveSurferRef.current.playPause();
          toggleIsPlaying(waveSurferRef.current.isPlaying());
        }}
        type="button"
      >
        {isPlaying ? <FaPauseCircle size="3em" /> : <FaPlayCircle size="3em" />}
      </button>
      <div
        style={{
          width: "100%",
          height: "100%",
        }}
        ref={containerRef}
      />
    </div>
  );
};

export default Waveform;
