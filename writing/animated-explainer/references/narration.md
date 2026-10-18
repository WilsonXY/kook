# Narration: script, voice and audio

## Writing the script
- **One beat per `say()`.** A beat is one or two sentences and one visual change. The narration describes what is on screen at that moment, and the animation shows what the sentence says.
- **Bottom-up.** Start from the running example, then name the idea, then give the source's definition. Never open a section with the definition.
- **Full sentences.** Avoid dramatic fragments ("Planned. Decided in advance."), slogans ("Quality doesn't happen by accident") and "not X, but Y" contrasts. Each `say()` is synthesised on its own, so its intonation restarts every time. Fragments therefore come out choppy. Then run the `wilson-humanizer` skill over the whole script.
- **Natural signposts.** Write "So, first up. What is quality?", not "Section one. What is quality?".
- **Keep the source exact.** Definitions, quotes and list counts the audience must learn stay word for word. Introduce them ("The IEEE defines it as …"). Never paraphrase them into something the exam would mark wrong.
- **Label your examples.** Say "For example …" or "Say …" for running-example content, and show "(example, not from the source)" on screen.
- **Length.** Expect natural sentences to run about 20% longer than terse ones. Tighten the wording, not the content.
- **Bulk edits.** `narration.py dump chNN.py` lists every narration string with an id. Write a JSON map of `{"id": "new text"}`, then run `narration.py apply chNN.py map.json`. The dump also lists sentence-like on-screen captions, so map only the ids that are narration.

## Words the voice must say right
- **Acronyms.** Write them joined ("SQAP", "QA", "IEEE"). The kit joins spaced capitals ("Q A" becomes "QA") because Kokoro reads a lone "A" as the article: "Q A" comes out as "queue, uh". Subtitles show the joined form as well.
- **Check before rendering.** `KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M", model=False)(text)` returns phonemes without audio. Look for names, local words and currency.
- **Fix a word** by adding it to `KOKORO_FIXES` in the kit, in misaki syntax: `"Aina": "[Aina](/ˈInə/)"`.
- **Write numbers and symbols the way they're spoken.** For example "five ringgit", "two times five", "ten percent".

## Choosing the voice
- **Pick by ear.** `voice_samples.py` writes the same passage in each voice to `voice_samples/`. You can't hear audio, so the user picks. Recommend Kokoro's best-rated voices: `af_heart` (US female, the top rating), `am_puck` and `am_michael` (US male), `bf_emma` (UK female). Set the choice with `EXPLAINER_VOICE`.
- **Render a preview.** Do a short draft of one section with the chosen voice before rendering everything, so pace and tone are judged in context.
- **Free options only:** Kokoro (local, CPU is fine, about 2–3 s per sentence) or `EXPLAINER_TTS=edge` (Microsoft's online voices, flatter). Paid voices (ElevenLabs, OpenAI) only if the user asks. The engine sits behind the kit's `_tts()`, so swapping it is a small change, and timing re-syncs on its own because every beat waits for its audio.

## Audio level
- **Mastering.** The kit masters every clip: it trims silence, levels to -15 LUFS, applies a peak limiter, and saves 48 kHz stereo. Full videos land around -13 to -14 LUFS, YouTube's level.
- **Measure the final video, not the clips:**
  ```python
  import av, numpy as np, pyloudnorm as pyln
  c = av.open("video.mp4"); r = c.streams.audio[0].rate
  x = np.concatenate([f.to_ndarray() for f in c.decode(audio=0)], axis=1).T
  print(pyln.Meter(r).integrated_loudness(x))
  ```
- **Two traps made earlier videos about 7 dB too quiet:**
  - Capping peaks without a limiter stops the voice from getting loud.
  - Mono clips lose 3 dB when they're mixed into a stereo video.
