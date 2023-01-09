#!/usr/bin/env bash

pyinstaller --noconsole --onefile --add-data pause.png:. --add-data start.png:. --add-data stop.png:. --add-data arrow.png:. mazes.pyw