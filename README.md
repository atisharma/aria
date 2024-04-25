# This is an experimental fork of Aria

[Original Aria project](https://github.com/lef-fan/aria/)

[x] use of OpenAI-compatible API instead of llama.cpp (I use with tabbyAPI)
[x] separation of server and client into separate branches
[x] commit to the client-server architecture
[ ] handle disconnections and reconnections without failure
[ ] multiple simultaneous clients
[ ] conversational memory (server-side)
[ ] UI changes and simplifications
[x] Alternative UI for raspberry pi with hardware controls (rosa branch)
[ ] RAG from vector db (server-side)
[ ] RAG from tools, e.g. web search, transcripts (server-side)

## Acknowledgments

- [The original Aria project](https://github.com/lef-fan/aria/)
- [silero-vad](https://github.com/snakers4/silero-vad)
- [transformers](https://github.com/huggingface/transformers)
- [whisper](https://github.com/openai/whisper)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [TTS](https://github.com/coqui-ai/TTS)
- [tabbyAPI](https://github.com/theroyallab/tabbyAPI/)
- [exllamav2](https://github.com/turboderp/exllamav2)

## License

I inherit and retain the licence of Aria, which is licensed under GNU AGPLv3.

### Important Note:
While this project is licensed under GNU AGPLv3, the usage of some of the components it depends on might not and they will be listed below:

#### TTS MODEL
- **License**: Open-source only for non-commercial projects.
- **Commercial Use**: Requires a paid plan.
- **Details**: [Coqui Public Model License 1.0.0](https://coqui.ai/cpml)
