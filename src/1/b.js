import { getInput, toNumbers } from "../common.ts";

const input = toNumbers(getInput({ day: 1 }));

let sums = [];
let sum = 0;
let i = 0;
while (i < input.length) {
  if (input[i] !== 0) {
    sum += input[i];
  } else {
    sums.push(sum);
    sum = 0;
  }
  i++;
}

sums = sums.sort((a, b) => b - a);

console.log(sums.slice(0, 3).reduce((a, b) => a + b, 0));
