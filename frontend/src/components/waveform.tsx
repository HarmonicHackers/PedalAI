import React, { useState, useEffect, useRef } from "react";
// import PropTypes from "prop-types";
import WaveSurfer from "wavesurfer.js";

import RangeSlider from "react-range-slider-input";
import { FaPlayCircle, FaPauseCircle } from "react-icons/fa";

import "react-range-slider-input/dist/style.css";

const Waveform = ({
  audio,
  value,
  setValue,
}: {
  audio: Blob;
  value: [number, number];
  setValue: (value: [number, number]) => void;
}) => {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const waveSurferRef = useRef<WaveSurfer | null>(null);
  const [isPlaying, toggleIsPlaying] = useState(false);

  useEffect(() => {
    if (isPlaying) toggleIsPlaying(false);
  }, [audio]);

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
      // waveSurferRef.enableDragSelection({});
    });

    return () => {
      waveSurfer.destroy();
    };
  }, [audio]);

  // get url from blob

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

      <div className="w-full h-full relative">
        <div className="h-full w-full" ref={containerRef} />
        <div
          style={{
            left: value[0] + "%",
            width: value[1] - value[0] + "%",
            height: "100px",
          }}
          className="bg-red-500 opacity-50 absolute top-0 bottom-0 bg-blend-lighten"
        ></div>
        <div className="absolute opacity-50 top-1/2 left-0 right-0 z-50 w-full bottom-0">
          <pre>{JSON.stringify(value, null, 2)}</pre>
          <RangeSlider value={value} onInput={setValue} />
        </div>
      </div>
    </div>
  );
};

export default Waveform;
