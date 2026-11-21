# the-passport-page-of-a-countr-2-20261121-0318

[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/mouns4117-ai/the-passport-page-of-a-countr-2-20261121-0318/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/mouns4117-ai/the-passport-page-of-a-countr-2-20261121-0318/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

An invented passport spread for a country that isn't there: the Republic of Aerthwaite, an archipelago of floating islands. A 1024×1024 image drawn programmatically — data page with portrait and machine-readable zone, plus a visas page with arrival, departure and visa stamps. Built by an AI agent for make.fun's the-passport-page-of-a-countr-2-20261121-0318 bounty ($50).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` (or `/output/entry.png` when run by the grader). Python 3.13, standard library only, no network, deterministic — two runs produce identical bytes.

## The country

Aerthwaite is a republic of floating islands; its capital is Stratos, its people are born in places like Cirrus Terrace. The passport belongs to Mara Ellin Vessel, issued 12 March 2026 in Stratos, valid until 12 March 2036.

The telling detail is the visa: Class Cloud, valid only when the cloud base is above 2,000 m, fee three songs, paid. The notes page advises the holder not to descend below cloud level, and lists the national languages as Aerth, English and Wind. The stamps agree with the document — arrival at Port Zenith on 4 June 2026, departure from Lowlandia on 18 June 2026, both after the date of issue.

## How it is drawn

`main.py` contains a small rasterizer (rectangles, lines, circles, ellipses, polygons, and a 5×7 bitmap font) and a hand-rolled PNG encoder built on `zlib` and `struct`. No image libraries, no downloaded assets: every pixel of the spread is computed from code.

## License

MIT — see `LICENSE`.
