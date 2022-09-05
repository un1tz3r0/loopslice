# loopsex

A command-line tool for splitting musical audio files into loops on the downbeats. Uses madmom for music information retrieval, and pydub for audio file I/O.

Each file given is processed in two passes. The first analyzes the audio and locates the downbeat positions within it. The second splits the audio file at the downbeat onsets, writing numbered clips to the specified output directory, or alongside the input files if none is given.

```
Usage: loopsex.py [OPTIONS] [FILENAME]...

Options:
  --min-tempo FLOAT           The minimum BPM for the beat detection
                              algorithm.
  --max-tempo FLOAT           The maximum BPM for the beat detection
                              algorithm.
  --skip-in / --no-skip-in    Skip the section of audio before the first
                              detected downbeat.
  --skip-out / --no-skip-out  Skip the section of audio after the last
                              detected downbeat.
  -o, --outdir TEXT           The directory where to put output files. If not
                              specified, same as input file.
  --help                      Show this message and exit.
```


