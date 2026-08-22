# AI Provider Abstraction — PL-04

This layer gives Personal AI one request/response contract across providers without making provider access implicit.

## Implemented providers

- `mock` — deterministic, offline, always available; authoritative PL-04 acceptance path.
- `openai` — stdlib adapter for the OpenAI Responses endpoint; requires `OPENAI_API_KEY`, an explicit/default model and CLI `--allow-network`.
- `anthropic` — stdlib adapter for the Claude Messages endpoint; requires `ANTHROPIC_API_KEY`, an explicit/default model and CLI `--allow-network`.
- `ollama` — stdlib adapter for local `/api/chat`; requires an explicit/default model and CLI `--allow-network`. A configured URL is not a health proof that Ollama is running.

`provider list` is metadata-only and never probes the network. Provider descriptors do not contain API keys.

## CLI

```bash
python personal-ai/run.py provider list
python personal-ai/run.py provider run mock "hello"
python personal-ai/run.py provider run openai "hello" --model <model> --allow-network
python personal-ai/run.py provider run anthropic "hello" --model <model> --allow-network
python personal-ai/run.py provider run ollama "hello" --model <local-model> --allow-network
```

## Acceptance boundary

PL-04 proves the common provider contract and mock execution without a paid API. Adapter request/response shapes are regression-tested using an injected fake transport; CI performs no live OpenAI, Anthropic or Ollama request. A configured key is not provider-live evidence, and this layer is not model training or self-modification.
