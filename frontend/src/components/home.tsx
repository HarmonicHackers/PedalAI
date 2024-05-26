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
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 h-screen max-w-3xl mx-auto ">
        <div className="flex flex-col justify-center gap-2">
          <h1 className="text-4xl font-bold">PedalAI</h1>
          <p className="text-lg">Your music effect assistant</p>
          <div className="pt-2">
            <button
              onClick={startSession}
              className=" px-4 py-3 rounded-lg text-xl border-none bg-white text-black shadow-sm"
            >
              Try pedal!
            </button>
          </div>
        </div>
        <div className="flex flex-col items-center justify-center">
          Insert logo here
          <div className="bg-gradient-to-tr from-white to-green-500 w-full h-[300px] rounded-full blur-[90px]"></div>
        </div>
      </div>
    </div>
  );
}
export default Home;
