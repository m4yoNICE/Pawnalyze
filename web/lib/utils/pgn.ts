import { Chess } from "chess.js";

export function parsePgn(pgn: string): string {
  const chess = new Chess();
  chess.loadPgn(pgn);
  return chess.pgn();
}

export function getLastFen(pgn: string): string {
  const chess = new Chess();
  chess.loadPgn(pgn);
  return chess.fen();
}