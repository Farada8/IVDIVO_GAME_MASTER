# AI Provider Abstraction — PL-04

Business, book and agent logic must depend on `AIProvider`, not on a provider SDK or hard-coded model name.

Canonical provider classes:

- `OpenAIProvider`
- `AnthropicProvider`
- `OllamaProvider`
- `MockProvider`

Required provider-neutral operations:

- `generate(request)`
- `analyze(request, instruction=...)`
- `classify(request, labels=...)`
- `extract(request, schema=...)`

`analyze`, `classify` and `extract` are normalized at the `AIProvider` boundary and use the provider-specific `generate` implementation. All return `ProviderResponse` with common provider/model/text/usage/metadata fields.

`ProviderConfig` supports provider, model, temperature, max_tokens, endpoint and the **name** of a secret environment variable. It never embeds the secret value. `provider_from_config()` is the factory boundary used instead of provider-specific construction in business logic.

`MockProvider` is deterministic and network-free, so all core tests can execute with zero API spend.

OpenAI/Anthropic/Ollama adapters use a `JsonTransport` abstraction. Tests inject a fake transport; no live endpoint is contacted. Missing paid-provider credentials fail closed. Unknown provider names fail closed. There is no automatic fallback from a requested live provider to `MockProvider`.

PL-04 establishes the abstraction and adapters only. Cost accounting belongs to PL-18, model routing to PL-19, bounded agent execution to PL-05, and claim/evidence semantics to PL-03.
