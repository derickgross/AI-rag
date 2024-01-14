AI app iterations and upcoming features
================

Wishlist:
- integration with derickgross.com
- ability to interact with AI (ask software engineering questions)
- Rejects non-software engineering related questions: “Sorry, this question does not seem to be related to software engineering.” (discourages misuse of AI)
- ability to modify several parameters, such as:
    - chunking strategy
    - embedding methods
    - retrieval approaches:
        - sentence-window
        - auto-merging
- app should show updated (TruLens) RAG triad ratings each time a parameter is updated
    - if new parameters match old, should ignore and not regenerate (not necessary for MVP)

*Keep notes for maintaining some version of a case study, so I can discuss challenges faced etc.


Implementation details:
- how should parameter updates be handled?  Regenerate new embeddings, index, etc.?  Preemptively generate several combinations an store them? (probably not- to offer a robust set of parameter options would mean an exponential number of pre-built combos)
- which LLM should we use?  Continue with OpenAI via API, or use a reasonably sized model that can be hosted?
    - consider baseline for answering SWE questions.  Better if there is a bigger difference in TruLens ratings between base and RAG implementations.
- hosting: AWS, or something like Heroku?  Probably AWS, as I've used it more recently