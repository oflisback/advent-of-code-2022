import {hideBin} from 'yargs/helpers'
import path from 'path'
import {readFileSync} from 'fs'
import yargs from 'yargs/yargs'

type CompletionStatus = Record<
  string,
  {
    get_star_ts: number
    start_index: number
  }
>

type Member = {
  completion_day_level: CompletionStatus[]
  name: string
  stars: number
}

type AoCData = {
  event: string
  owner_id: number
  members: Member[]
}

type StarRange = 1 | 2
const StarNames: StarRange[] = [1, 2]

const printDay = ({data, day}: {data: AoCData; day: number}) => {
  const dayData = Object.values(data.members).map((m) => ({
    name: m.name,
    stars: {
      1: m.completion_day_level[day]?.['1']?.get_star_ts,
      2: m.completion_day_level[day]?.['2']?.get_star_ts,
    },
  }))
  StarNames.forEach((starName: StarRange) => {
    const anyStars = dayData.some((m) => m.stars[starName])
    if (anyStars) {
      console.log(`*** Day ${day} star ${starName} ***`)
    }
    dayData
      .filter((m) => m.stars[starName] !== undefined)
      .sort((a, b) => a.stars![starName] - b.stars![starName])
      .forEach((m) => {
        console.log(
          `${new Date(m.stars![starName] * 1000).toLocaleString('sv-SE', {
            timeZone: 'Europe/Stockholm',
          })} - ${m.name}`
        )
      })
  })
}

const getData = ({listName, year}: {listName: string; year: number}) => {
  try {
    const data = JSON.parse(
      readFileSync(
        path.resolve(__dirname, `./highscore-lists/${listName}-${year}.json`),
        'utf8'
      )
    )
    return data
  } catch (e) {
    console.error('Error loading list, list not pre-downloaded?')
    console.log(e)
    process.exit(-1)
  }
}

const start = ({
  listName,
  day,
  year,
}: {
  listName: string
  day?: number
  year?: number
}) => {
  if (!year) {
    year = new Date().getFullYear()
  }

  // Load the list data
  const data = getData({listName, year})

  if (day) {
    printDay({data, day})
  } else {
    for (let i = 1; i <= 25; i++) {
      printDay({data, day: i})
    }
  }
}

yargs(hideBin(process.argv))
  .command(
    '* <listName> [-d day] [-y year]',
    'Display stats for participants in a private AoC highscore list',
    () => ({}),
    (argv) => {
      let day, year
      if (argv.day) {
        const parsed_day = Number.parseInt(argv.day as string)
        day = Number.isNaN(parsed_day) ? undefined : parsed_day
      }
      if (argv.year) {
        const parsed_year = Number.parseInt(argv.year as string)
        year = Number.isNaN(parsed_year) ? undefined : parsed_year
      }
      start({day, listName: argv.listName as string, year})
    }
  )
  .positional('listName', {
    describe: "The name of the list you'd like to display",
  })
  .option('day', {
    alias: 'd',
    demandOption: false,
    type: 'number',
    description: 'Show stats for specific day number',
  })
  .option('year', {
    alias: 'y',
    demandOption: false,
    type: 'number',
    description: 'Show stats for a year other than current year',
  })
  .parse()
