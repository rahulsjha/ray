from ray import serve

@serve.deployment
class Translator:
    def __call__(self, req): return "t"

@serve.deployment
class Summarizer:
    def __init__(self, translator): self.t = translator
    async def __call__(self, req): return "s"

app = Summarizer.bind(Translator.bind())

@serve.deployment
class Other:
    def __call__(self, req): return "o"
other = Other.bind()
