# Developer Tools

The `bandwidth.tools` package contains helpers for building and testing
Bandwidth voice and messaging applications locally.

## CallbackStore

Record callbacks your webhook receives and query them later.

```python
from bandwidth.tools import CallbackStore

store = CallbackStore("callbacks.db")
store.add(request.json)
store.find_by_call_id("c-86d5e1f2-...")
store.latest("answer")
```

## parse_bxml

Turn a BXML document into nested dictionaries, handy for asserting on
the BXML your app returns.

```python
from bandwidth.tools import parse_bxml

parse_bxml('<Response><Pause duration="2" /></Response>')
# {"root": "Response", "verbs": [{"verb": "Pause", "attributes": {"duration": "2"}}]}
```

## MediaCache

Cache media downloaded from the Media API on disk.

```python
from bandwidth.tools import MediaCache

cache = MediaCache(".media-cache", ttl_seconds=600)
cache.set(url, content, {"Content-Type": "image/jpeg"})
cache.get(url)
```

## Audio conversion

Convert audio to mono 16-bit PCM WAV for `<PlayAudio>`. Requires `ffmpeg` on
your `PATH`.

```python
from bandwidth.tools import convert_to_wav

convert_to_wav("greeting.mp3")  # "greeting.wav"
```

## Routing rules

Evaluate simple boolean rules against callback payloads. Payload keys are
converted to snake_case; `from` and `to` become `from_` and `to_`.

```python
from bandwidth.tools import evaluate_rule

evaluate_rule('event_type == "gather" and digits == "1"', payload)
```

## send_test_callback

POST a sample callback to your webhook server.

```python
from bandwidth.tools import send_test_callback

send_test_callback("https://localhost:8443/callbacks/answer", {"eventType": "answer"})
```
