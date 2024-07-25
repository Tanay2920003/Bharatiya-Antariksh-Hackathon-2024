# SpeechMap

Try the **[DEMO](https://geo.rocks/speechmap/)**!

A simple leaflet map with voice control based on:
* [annyang](https://github.com/TalAter/annyang)
* [SpeechKITT](https://github.com/TalAter/SpeechKITT) 
* [nominatim](https://nominatim.openstreetmap.org/ui/search.html?q=berlin).

![SpeechMap](https://github.com/do-me/speechmap/blob/main/speechmap.gif)

## Installation

Just clone the repo and run any server, e.g. a basic Python server with 

```cmd
python -m http.server
```

Access localhost in a Browser under 

```
localhost:8000
```

Tests worked on desktop only and Chrome (not Chromium as API keys are missing). 

## Commands

* "Fly to *city*" (or any other geocodable name)
* "Hello"
* "Stop listening"
