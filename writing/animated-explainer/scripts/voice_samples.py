"""Render the same passage in several voices so the user can pick one by ear (you cannot hear audio).

    python voice_samples.py                    # default passage
    python voice_samples.py passage.txt        # one narration line per line of the file

Writes ../voice_samples/kokoro_<voice>.wav (plus edge_<voice>.wav if edge-tts is installed).
Every sample goes through the same mastering as the videos, so loudness matches.
"""
import os
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

os.environ.setdefault("EXPLAINER_TTS", "kokoro")
sys.path.insert(0, str(Path(__file__).parent))
import explainer_kit as kit  # noqa: E402

LINES = [
    "Say you order a pizza. You need a large one, it has to be hot, and it should arrive within thirty minutes.",
    "What actually shows up is a small pizza, cold, an hour and a half late.",
    "That's basically the whole idea. Quality is how closely what you get matches what you need.",
]
if len(sys.argv) > 1:
    LINES = [l.strip() for l in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines() if l.strip()]

# Kokoro's best-rated voices first; a = American, b = British, f = female, m = male.
VOICES = ["af_heart", "af_bella", "am_puck", "am_michael", "am_fenrir", "bf_emma", "bm_george", "bm_fable"]
EDGE = ["en-US-AndrewNeural", "en-GB-RyanNeural"]

out = kit.BUILD.parent / "voice_samples"
out.mkdir(exist_ok=True)
gap = np.zeros((int(kit.OUT_SR * 0.45), 2), dtype=np.float32)


def stitch(paths, dest):
    parts = []
    for p in paths:
        a, sr = sf.read(str(p), dtype="float32")
        assert sr == kit.OUT_SR
        parts += [a, gap]
    sf.write(str(dest), np.concatenate(parts), kit.OUT_SR)
    print("wrote", dest.name)


for v in VOICES:
    kit.KOKORO_VOICE = v
    stitch([kit._tts(l) for l in LINES], out / f"kokoro_{v}.wav")

try:
    import edge_tts  # noqa: F401
except ImportError:
    sys.exit(0)
kit.ENGINE = "edge"
for v in EDGE:
    kit.VOICE = v
    wavs = []
    for l in LINES:
        mp3 = kit._tts(l)
        wav = mp3.with_suffix(".cmp.wav")
        kit._decode_to_wav(mp3, wav)
        wavs.append(wav)
    stitch(wavs, out / f"edge_{v}.wav")
