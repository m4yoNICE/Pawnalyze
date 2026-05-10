export interface AnalyzeRequest {
  pgn: string;
  depth?: number;
}

export interface Evaluation {
  type: "cp" | "mate";
  value: number;
}

export interface TopMove {
  Move: string;
  Centipawn: number | null;
  Mate: number | null;
}

export interface MoveAnalysis {
  fen: string;
  best_move: string;
  evaluation: Evaluation;
  top_moves: TopMove[];
  classification: string;
  symbol: string;
  commentary: string;
}

export interface AnalyzeResponse {
  status: string;
  analysis: MoveAnalysis[];
  summary: string;
}

export interface BoardProps {
  fen?: string;
}
