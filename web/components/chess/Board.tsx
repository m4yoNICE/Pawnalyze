"use client";

import { Chessboard } from "react-chessboard";
import { BoardProps } from "@/lib/Types";

export default function Board({ fen }: BoardProps) {
  return (
    <div className="w-full max-w-[560px] mx-auto">
      <Chessboard
        options={{
          id: "BasicBoard",
          position: fen ?? "start",
          allowDragging: true,
        }}
      />
    </div>
  );
}
