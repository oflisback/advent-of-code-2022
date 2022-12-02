import { getInput } from "../common.ts";

const input = getInput({ day: 2 }).split("\n");

const rounds = input.map((i) => i.split(" ")).map((i) => [i[0], i[1]]);

const charToCommand = {
  'A': 'ROCK',
  'B': 'PAPER',
  'C': 'SCISSOR',
}

const charToStrat = {
  "X": "LOSE",
  "Y": "DRAW",
  "Z": "WIN",
}

const commandToScore = {
  'ROCK': 1,
  'PAPER': 2,
  'SCISSOR': 3
}

const getCommandFromStrat = (yours, instr) => {
  if (instr === "DRAW") {
    return yours;
  }
  switch (yours) {
    case "ROCK":
      return instr === "WIN" ? "PAPER" : "SCISSOR"
    case "PAPER":
      return instr === "WIN" ? "SCISSOR" : "ROCK"
    default:
      return instr === "WIN" ? "ROCK" : "PAPER"
  }
}

const getRoundCommands = (round) =>
 [charToCommand[round[0]],getCommandFromStrat(charToCommand[round[0]], charToStrat[round[1]])]

const getRoundPoints = (o) => {
  const [yours, mine] = o
  const commandScore = commandToScore[mine]

  if (yours === mine) {
    return 3 + commandScore
  }

  switch (yours) {
    case "ROCK":
      return commandScore + (mine === "PAPER" ? 6 : 0)
    case "PAPER":
      return commandScore + (mine === "SCISSOR" ? 6 : 0)
    case "SCISSOR":
      return commandScore + (mine === "ROCK" ? 6 : 0)
  }
};

const roundCommands = rounds.map(getRoundCommands);
const roundPoints = roundCommands.map(getRoundPoints);
const sum = roundPoints.reduce((a, b) => a + b, 0);

console.log(sum);
