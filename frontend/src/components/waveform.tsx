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
      height: containerRef.current!.clientHeight,
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
    <div className="grid grid-cols-[40px_1fr] items-center w-full h-full">
      <button
        className="p-0.5 flex items-center justify-center bg-white text-black"
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
      <div className="h-full w-full" ref={containerRef} />
    </div>
  );
};

export default Waveform;
