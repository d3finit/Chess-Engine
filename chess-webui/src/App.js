import { useState } from "react";
import { Chess } from "chess.js";
import { Chessboard } from "react-chessboard";

export default function Board() {
  const [game, setGame] = useState(new Chess());

  const makeMove = (move) => {
    game.move(move);
    setGame(new Chess(game.fen()));
  };

  console.log(game.fen());
  var game_fen = game.fen();

  function makeRandomMove() {
    const possibleMoves = game.moves();
    if (game.isGameOver() || game.isDraw() || possibleMoves.length === 0)
      return; // exit if the game is over
    const randomIndex = Math.floor(Math.random() * possibleMoves.length);
    console.log(possibleMoves[randomIndex]);
    makeMove(possibleMoves[randomIndex]);
  }

  function onDrop(sourceSquare, targetSquare) {
    try {
      const move = makeMove({
        from: sourceSquare,
        to: targetSquare,
        promotion: "q", // always promote to a queen for example simplicity
      });

      // illegal move
      if (move === null) return false;
      setTimeout(makeRandomMove, 200);
      return true;

      game_fen = game.fen()
    } catch {
      console.log("err");
    }
  }

  // fen = game.fen()

  const styles = {

    position: 'absolute', left: '50%', top: '50%',
    transform: 'translate(-50%, -50%)
  };

  return (
    <div className="board" style={styles}>
      <Chessboard
        position={game_fen}
        onPieceDrop={onDrop}
        boardWidth={500}
        style={styles}
      />
    </div>
  );
}
