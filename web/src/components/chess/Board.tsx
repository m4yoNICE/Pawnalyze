"use client";

import { Chessboard } from "react-chessboard";
import { BoardProps } from "@/lib/Types";
import { createCustomPieces } from "@/lib/utils/piece";

const customPieces = createCustomPieces("/pieces/yun.png");

export default function Board({ fen }: BoardProps) {
  return (
    <div className="w-full max-w-[560px] mx-auto">
      <Chessboard
        options={{
          id: "BasicBoard",
          position: fen,
          allowDragging: true,
          lightSquareStyle: { backgroundColor: "#F3EFFE" },
          darkSquareStyle: { backgroundColor: "#7B6FA0" },
          // pieces: customPieces,
        }}
      />
    </div>
  );
}
