import {readFileSync} from 'fs'

export const getInput = ({day}: {day: number}) =>
  readFileSync(`./src/${day}/input.txt`, 'utf8')

export const lines = (data: string) => data.split('\n')

export const toNumbers = (data: string) => lines(data).map((value) => +value)

export const verify = (
  func: (input: string) => number,
  input: string,
  expectation: number
) => {
  if (func(input) === expectation) {
    console.log('Pass!')
  } else {
    console.log('Fail!')
  }
}
