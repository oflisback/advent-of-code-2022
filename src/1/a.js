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

console.log(Math.max(...sums));
