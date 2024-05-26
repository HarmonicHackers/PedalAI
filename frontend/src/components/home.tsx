function Home({
  startSession,
  restoreSession,
}: {
  startSession: () => void;
  restoreSession?: () => void;
}) {
  // two side hero
  return (
    <div className="bg-black text-white">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 h-screen max-w-5xl mx-auto ">
        <div className="flex flex-col justify-center gap-2">
          <h1 className="text-5xl font-bold text tracking-tighter  ">
            PedalAI
          </h1>
          <p className="text-lg">
            Hello hackers 🤟 ! I am Pedal, your music effect assistant! 🎶
            <br />
            Import a track and let's build together! 🚀
          </p>
          <div className="pt-2">
            <button
              onClick={startSession}
              className=" px-4 py-3 rounded-lg text-xl border-none bg-white text-black shadow-sm"
            >
              Try pedal!
            </button>
          </div>
        </div>
        <div className="flex flex-col items-center justify-center relative">
          <img
            src="/hack-logo.png"
            alt="hack logo"
            className="w-[500px] scale-120 z-10  rounded-full relative inset-0"
          />
          <div className="absolute inset-0 flex items-center justify-center h-full w-full">
            <div className="bg-gradient-to-tr from-green-500 to-green-800 w-full h-[300px] rounded-full blur-[90px]"></div>
          </div>
        </div>
      </div>
    </div>
  );
}
export default Home;
