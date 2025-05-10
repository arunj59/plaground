import { useState, useEffect } from "react";

export default function TicTacToe() {
  const [board, setBoard] = useState(Array(9).fill(null));
  const [isXNext, setIsXNext] = useState(true);
  const [gameStatus, setGameStatus] = useState("Game in progress");
  const [winningLine, setWinningLine] = useState(null);
  const [animatingCell, setAnimatingCell] = useState(null);

  // Custom emoji markers as requested by user
  const playerMarkers = {
    X: "🏃‍♂️", // Running person emoji for player 1 (X)
    O: "🧑‍💻"  // Person at computer emoji for player 2 (O)
  };

  const lines = [
    [0, 1, 2], // top row
    [3, 4, 5], // middle row
    [6, 7, 8], // bottom row
    [0, 3, 6], // left column
    [1, 4, 7], // middle column
    [2, 5, 8], // right column
    [0, 4, 8], // diagonal
    [2, 4, 6], // diagonal
  ];

  const calculateWinner = (squares) => {
    for (let i = 0; i < lines.length; i++) {
      const [a, b, c] = lines[i];
      if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
        return { winner: squares[a], line: lines[i] };
      }
    }
    return null;
  };

  const handleClick = (i) => {
    if (board[i] || winningLine) {
      return;
    }

    const newBoard = board.slice();
    newBoard[i] = isXNext ? "X" : "O";

    setAnimatingCell(i);
    setTimeout(() => setAnimatingCell(null), 500);

    setBoard(newBoard);

    const winResult = calculateWinner(newBoard);
    if (winResult) {
      setWinningLine(winResult.line);
      setGameStatus(`Winner: ${winResult.winner}`);
    } else if (newBoard.every(square => square !== null)) {
      setGameStatus("Game ended in a draw");
    } else {
      setIsXNext(!isXNext);
    }
  };

  const resetGame = () => {
    setBoard(Array(9).fill(null));
    setIsXNext(true);
    setGameStatus("Game in progress");
    setWinningLine(null);
    setAnimatingCell(null);
  };

  const renderSquare = (i) => {
    const isWinningSquare = winningLine && winningLine.includes(i);
    const isAnimating = animatingCell === i;

    let bgColor = "bg-white hover:bg-gray-100";

    if (board[i] === "X") {
      bgColor = "bg-blue-100 hover:bg-blue-200";
    } else if (board[i] === "O") {
      bgColor = "bg-rose-100 hover:bg-rose-200";
    }

    if (isWinningSquare) {
      bgColor = board[i] === "X" ? "bg-blue-400" : "bg-rose-400";
    }

    return (
      <button
        className={`w-16 h-16 border border-gray-400 text-3xl font-bold flex items-center justify-center
        ${bgColor} transition-all duration-300 ${isAnimating ? "scale-110" : "scale-100"}
        ${isWinningSquare ? "animate-pulse shadow-lg" : ""}`}
        onClick={() => handleClick(i)}
      >
        <span className={`${isAnimating ? "animate-bounce" : ""}
        ${board[i] === "X" ? "text-blue-600" : "text-rose-600"} text-4xl`}>
          {board[i] ? playerMarkers[board[i]] : null}
        </span>
      </button>
    );
  };

  const xColor = "text-blue-600";
  const oColor = "text-rose-600";

  const status = winningLine
    ? <span>Winner: <span className={board[winningLine[0]] === "X" ? xColor : oColor} style={{fontWeight: "bold"}}>{playerMarkers[board[winningLine[0]]]}</span></span>
    : board.every(square => square !== null)
      ? "Game ended in a draw"
      : <span>Next player: <span className={isXNext ? xColor : oColor} style={{fontWeight: "bold"}}>{isXNext ? playerMarkers.X : playerMarkers.O}</span></span>;

  useEffect(() => {
    if (winningLine) {
      const confetti = document.createElement('div');
      confetti.className = 'absolute inset-0 z-10 pointer-events-none';
      confetti.innerHTML = Array(50).fill().map(() => {
        const size = Math.random() * 10 + 5;
        const color = board[winningLine[0]] === 'X' ? 'bg-blue-500' : 'bg-rose-500';
        return `<div class="absolute animate-confetti ${color}" style="
          top: ${Math.random() * 100}%;
          left: ${Math.random() * 100}%;
          width: ${size}px;
          height: ${size}px;
          "></div>`;
      }).join('');

      document.getElementById('game-container').appendChild(confetti);

      return () => {
        if (confetti.parentNode) {
          confetti.parentNode.removeChild(confetti);
        }
      };
    }
  }, [winningLine]);

  return (
    <div className="flex flex-col items-center justify-center p-4 relative" id="game-container">
      <style jsx>{`
        @keyframes confetti {
          0% { transform: translateY(0) rotate(0deg); opacity: 1; }
          100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
        }
        .animate-confetti {
          animation: confetti 4s ease-in-out forwards;
        }
      `}</style>

      <h1 className="text-3xl font-bold mb-4 bg-gradient-to-r from-blue-500 to-rose-500 text-transparent bg-clip-text">Emoji Tic-Tac-Toe</h1>

      <div className="mb-4 text-lg font-semibold">
        {status}
      </div>

      <div className="grid grid-cols-3 gap-2 mb-6 p-3 bg-gradient-to-r from-blue-100 to-rose-100 rounded-lg shadow-md">
        {renderSquare(0)}
        {renderSquare(1)}
        {renderSquare(2)}
        {renderSquare(3)}
        {renderSquare(4)}
        {renderSquare(5)}
        {renderSquare(6)}
        {renderSquare(7)}
        {renderSquare(8)}
      </div>

      <button
        className="bg-gradient-to-r from-blue-500 to-rose-500 hover:from-blue-600 hover:to-rose-600 text-white font-bold py-2 px-6 rounded-full shadow-md transform transition-transform hover:scale-105"
        onClick={resetGame}>
        New Game
      </button>
    </div>
  );
}