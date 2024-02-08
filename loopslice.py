import pprint
from pydub import AudioSegment
from pathlib import Path
from madmom.features import RNNDownBeatProcessor, DBNDownBeatTrackingProcessor

def extractbars(filename, destdir=None, min_bpm=55., max_bpm=215., bar_beats=[3, 4], skip_in=True, skip_out=True):
  filepath = Path(filename)
  print(f"Analyzing {filename}...")
  
  proc = DBNDownBeatTrackingProcessor(beats_per_bar=bar_beats, fps=100, min_bpm=min_bpm, max_bpm=max_bpm)
  act = RNNDownBeatProcessor()(filename)
  beats = proc(act)

  numdownbeats = len([beatpos for beatpos, beatnum in beats if beatnum == 1.])
  print(f"  Found {numdownbeats} down-beats, {len(beats)} beats")

  print(f"Splitting {filename} at down-beats...")

  if destdir == None:
    destdir = filepath.parent
  else:
    destdir = Path(destdir)
  destdir.mkdir(parents=True, exist_ok=True)
  
  audio = AudioSegment.from_file(filename)
  if skip_in:
    startpos = None
  else:
    startpos = 0.
  chunknum = 0
  for i in range(0, len(beats)):
    beatpos, beatnum = beats[i]
    
    if beatnum == 1.:
      endpos = beatpos
      if startpos != None:
        chunk = audio[int(startpos*1000):int(endpos*1000)]
        chunkpath = destdir / f"{filepath.stem}_{chunknum:04}.wav"
        print(f"Writing chunk {chunknum} ({endpos-startpos}s) to file {chunkpath}")
        with open(str(chunkpath), "wb") as f:
          chunk.export(f, format="wav")
        chunknum = chunknum + 1
      startpos = beatpos
  if not skip_out:
    chunk = audio[int(startpos*1000):]
    chunkpath = destdir / f"{filepath.stem}_{chunknum:04}.wav"
    print(f"Writing chunk {chunknum} ({endpos-startpos}s) to file {chunkpath}")
    with open(str(chunkpath), "wb") as f:
      chunk.export(f, format="wav")

import click

@click.command()
@click.option("--min-tempo", default=55., help="The minimum BPM for the beat detection algorithm.")
@click.option("--max-tempo", default=215., help="The maximum BPM for the beat detection algorithm.")
@click.option("--skip-in/--no-skip-in", default=True, help="Skip the section of audio before the first detected downbeat.")
@click.option("--skip-out/--no-skip-out", default=True, help="Skip the section of audio after the last detected downbeat.")
@click.option("--outdir", "-o", default=None, help="The directory where to put output files. If not specified, same as input file.")
@click.argument("filename", nargs=-1)
def cli(filename, min_tempo=55., max_tempo=215., skip_in=True, skip_out=True, outdir=None):
  for f in filename:
    try:
      extractbars(f, destdir=outdir, min_bpm=min_tempo, max_bpm=max_tempo, skip_in=skip_in, skip_out=skip_out)
    except KeyboardInterrupt as kbint:
      print("Control-C pressed, exiting...")
      break
    except Exception as err:
      print(f"An error occurred: {err}")
      import traceback as tb
      tb.print_exc()
      print(f"while processing file: {f}")

if __name__ == "__main__":
  cli()
