# The World in One Page — 17 November 2026

[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261117-blue)](https://make.fun/c/news-image-20261117)

A one-page newspaper front page summing up world news on
**Tuesday 17 November 2026**, drawn entirely in code — no photographs,
no network access at runtime.

## The day, in one image

- **Top story — Kerch Bridge hit.** Ukraine strikes the bridge to Crimea;
  the road span collapses into the strait. Zelenskyy calls it an
  "unprecedented operation"; Russia answers with missiles on Kyiv's
  bridges, cutting power, water and heat.
- **Trump lands in Manila** for the ASEAN summit, signing a joint trade
  statement with Thailand ahead of three-way talks with Xi Jinping and
  Putin in Shenzhen on 19 November.
- **Mines in the Strait of Hormuz** — two tankers hit; the USS Theodore
  Roosevelt, the third US carrier in the region, arrives; an Iranian drone
  fired at the US radar base in Bahrain is intercepted.
- **JPMorgan goes dark** — a Monday banking outage blamed on a software
  bug, not a cyberattack.
- **Nvidia after Huang** — earnings after the close, the first since
  Jensen Huang stepped down.
- **Vulcan rocket fails** — a ULA launch failure destroys 40 Amazon Leo
  internet satellites.
- **UK sanctions settlers** — London sanctions eight West Bank settlement
  builders; allies press Israel to open Gaza crossings for aid.
- Also today: the Pentagon fails its ninth straight audit ($4.8 trillion
  unverified), Japan scrambles jets, Houthi advance in Yemen, Depardieu
  pleads guilty, Brent crude $92.76.

## How it works

`main.py` (Python standard library only) copies the bundled
`artwork.png` to `/output/entry.png` byte-for-byte, then verifies the
output: SHA-256 match against the embedded expected hash, PNG header
dimensions of 1024×1024, and size under 1 MiB. Running it twice writes
identical bytes.

## License

MIT — see [LICENSE](LICENSE).
