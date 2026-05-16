"use client";

import { MoveListProps } from "@/lib/Types";
import {
  getClassificationColor,
  getClassificationSymbol,
} from "@/lib/utils/classifications";

export default function MoveList({
  moves,
  currentMoveIndex,
  onMoveClick,
  analysis,
}: MoveListProps) {
  const movePairs = [];
  for (let i = 0; i < moves.length; i += 2) {
    movePairs.push(moves.slice(i, i + 2));
  }

  return (
    <div className="w-full overflow-y-auto max-h-[560px]">
      {movePairs.length === 0 && (
        <p className="text-sm text-[#6B6B6B] p-4 text-center">
          Paste a PGN and click Analyze to see moves.
        </p>
      )}
      {movePairs.map((pair, pairIndex) => (
        <div
          key={pairIndex}
          className={`flex items-center text-sm ${
            pairIndex % 2 === 0 ? "bg-white" : "bg-[#F8F7F4]"
          }`}
        >
          {/* Move Number */}
          <div className="w-10 py-2 px-2 text-[#6B6B6B] text-right text-xs select-none">
            {pairIndex + 1}.
          </div>

          {/* White Move */}
          <button
            onClick={() => onMoveClick(pairIndex * 2)}
            className={`flex-1 py-2 px-3 text-left font-semibold transition-colors ${
              currentMoveIndex === pairIndex * 2
                ? "bg-[#575068] text-white"
                : "text-[#1A1A1A] hover:bg-[#E1D8EF]"
            }`}
          >
            {pair[0]}
            {analysis?.[pairIndex * 2]?.symbol && (
              <span
                className="ml-1 text-xs font-bold"
                style={{
                  color: getClassificationColor(
                    analysis[pairIndex * 2].classification,
                  ),
                }}
              >
                {analysis[pairIndex * 2].symbol}
              </span>
            )}
          </button>

          {/* Black Move */}
          {pair[1] ? (
            <button
              onClick={() => onMoveClick(pairIndex * 2 + 1)}
              className={`flex-1 py-2 px-3 text-left font-semibold transition-colors ${
                currentMoveIndex === pairIndex * 2 + 1
                  ? "bg-[#575068] text-white"
                  : "text-[#1A1A1A] hover:bg-[#E1D8EF]"
              }`}
            >
              {pair[1]}
              {analysis?.[pairIndex * 2 + 1]?.symbol && (
                <span
                  className="ml-1 text-xs font-bold"
                  style={{
                    color: getClassificationColor(
                      analysis[pairIndex * 2 + 1].classification,
                    ),
                  }}
                >
                  {analysis[pairIndex * 2 + 1].symbol}
                </span>
              )}
            </button>
          ) : (
            <div className="flex-1" />
          )}
        </div>
      ))}
    </div>
  );
}
