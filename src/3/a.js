import {getInput} from '../common.ts'

const input = getInput({day: 3}).split('\n')

const getPoints = (char) =>
  char.charCodeAt(0) + (char.charCodeAt(0) >= 97 ? -97 + 1 : -65 + 1 + 26)

let sum = 0
input.forEach((row) => {
  const left = {}
  const right = {}
  for (let i = 0; i < row.length / 2; i++) {
    const leftValue = row[i]
    const rightValue = row[i + row.length / 2]
    left[leftValue] = true
    right[rightValue] = true
    if (right[leftValue]) {
      sum += getPoints(leftValue)
      break
    }
    if (left[rightValue]) {
      sum += getPoints(rightValue)
      break
    }
  }
})
console.log(sum)
