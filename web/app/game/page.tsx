"use client";

import { useState } from "react";
import Board from "@/components/chess/Board";
import { getLastFen, parsePgn } from "@/lib/utils/pgn";

const DEFAULT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";

export default function GamePage() {
  const [pgn, setPgn] = useState("");
  const [fen, setFen] = useState(DEFAULT_FEN);
  const [cleanPgn, setCleanPgn] = useState("");

  function handleAnalyze() {
    try {
      const formatted = parsePgn(pgn);
      setCleanPgn(formatted);
      setFen(getLastFen(pgn));
    } catch (e) {
      console.error("Invalid PGN", e);
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6">
      <Board fen={fen} />
      <textarea
        value={pgn}
        onChange={(e) => setPgn(e.target.value)}
        placeholder="Paste PGN here..."
        className="w-full max-w-[560px] h-40 p-3 border rounded font-mono text-sm"
      />
      <button
        onClick={handleAnalyze}
        className="px-6 py-2 bg-black text-white rounded"
      >
        Analyze
      </button>
    </main>
  );
}
