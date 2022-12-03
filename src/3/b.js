import {getInput} from '../common.ts'

const input = getInput({day: 3}).split('\n')

const getPoints = (char) =>
  char.charCodeAt(0) + (char.charCodeAt(0) >= 97 ? -97 + 1 : -65 + 1 + 26)

let sum = 0
while (input.length > 0) {
  const batch = input.splice(0, 3)
  const carried = [{}, {}, {}]

  batch.forEach((row, elfIndex) => {
    for (let i = 0; i < row.length; i++) {
      const c = row[i]
      carried[elfIndex][c] = true
      if (carried[0][c] && carried[1][c] && carried[2][c]) {
        sum += getPoints(c)
        break
      }
    }
  })
}
console.log(sum)
