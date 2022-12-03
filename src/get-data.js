import {AocClient} from 'advent-of-code-client'
import * as dotenv from 'dotenv'
import {existsSync, mkdirSync, writeFileSync} from 'fs'

const args = process.argv.slice(2)
if (args.length !== 1) {
  console.log('Expecting one argument, the day number')
  process.exit(-1)
}

const day = parseInt(args[0])

dotenv.config()

const path = `./input/${day}`
const filePath = `${path}/input.txt`

if (existsSync(filePath)) {
  console.log('input file: ', filePath, ' already exists')
  process.exit(0)
}

mkdirSync(path)

const client = new AocClient({
  year: 2022,
  day,
  token: process.env.AOC_SESSION_COOKIE,
})

const input = await client.getInput()

writeFileSync(filePath, input)
console.log('input written to: ', filePath)

process.exit(0)
