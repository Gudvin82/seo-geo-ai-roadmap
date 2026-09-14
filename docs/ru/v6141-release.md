# Сводка Релиза v6.14.1

`v6.14.1` завершает v6.14 integrity release после обнаружения CI-only import
issue в первом tagged commit.

Capability matrix намеренно dependency-light: документационные и release checks
генерируют ее без импорта optional HTTP client dependencies. Код live connector
загружается только при запросе реального provider sync.

Product scope не изменился относительно v6.14.0:

- generated evidence-bound capability matrix
- protocol calibration для explainable readiness scores
- каноническая EN/RU documentation map и parity check
- архивированные superseded evaluation и launch wrappers

Все release checks должны пройти на этом теге до того, как он будет считаться
текущим публичным релизом.
