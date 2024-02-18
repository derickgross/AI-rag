AI app iterations and upcoming features
================

Next: Design AWS CDK architecture
- Github Actions are running on push to main branch (errors because app.py missing app.synth()).  Need to finish app.py.  

Architecture:
- EC2, or serverless?  I can likely use serverless, and have lambdas for processing embeddings when they change (and storing them in S3), fulfilling requests, etc.

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
- which data set?  Return to MDN docs- custom sports data set was fun to build, but distracts from building foundational skills
- how should parameter updates be handled?  Regenerate new embeddings, index, etc.?  Preemptively generate several combinations an store them? (probably not- to offer a robust set of parameter options would mean an exponential number of pre-built combos)
- which LLM should we use?  Continue with OpenAI via API, or use a reasonably sized model that can be hosted?
    - consider baseline for answering SWE questions.  Better if there is a bigger difference in TruLens ratings between base and RAG implementations.
- hosting: AWS, or something like Heroku?  Probably AWS, as I've used it more recently
- when to integrate with website?  Sooner allows users to experience my work sooner, but later allows focus to remain on building foundational skills.  Probably sooner, as part of the goal is to learn in public
- use Github Actions to update architecture
- key actions/events:
    - create embeddings: lambda runs embed.py, then stores result in S3.  Should only run when certain files that impact the embedding are changed (which files?).  This means it's likely ideal to call this within the Github Actions build-app workflow.

Resources:
- https://dev.to/aws-builders/deploy-to-aws-with-github-actions-and-aws-cdk-4m1e
- https://github.com/stagehand-framework/stagehand/blob/main/templates/create_review_app.yml
- Jackson Yuan's Github Actions and AWS Serverless video: https://www.youtube.com/watch?v=KorJPUKvHKc
- Latent Space University: https://www.latent.space/p/aie-2023-workshops