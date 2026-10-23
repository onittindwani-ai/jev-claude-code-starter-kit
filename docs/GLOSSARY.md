# Glossary in plain words

- **Jev**: TypeSafe AI's first System One model. It answers typed questions instead of writing text.
- **System One model**: a model for fast, automatic judgment (like a gut decision), not for slow thinking in words.
- **State**: the text or data you give Jev to judge (for example the reply).
- **Choice**: pick 1 option from a list you define. Returns the choice, a probability for every option and a confidence.
- **Score**: rate on levels you define (for example calm, frustrated, angry).
- **Noul**: TypeSafe's word for a yes or no question. Returns a number from 0 (no) to 1 (yes).
- **Probability**: how likely each answer is, according to the model.
- **Confidence**: how sure the model is about its answer. Not the same as being right; test it (calibration).
- **Calibration**: whether confidence matches reality (80 percent sure, right about 80 times in 100).
- **Threshold**: the confidence you require before code acts automatically.
- **Confidence gate**: a rule that sends low confidence items to a person.
- **Prompt injection**: text that tries to give instructions to an AI.
- **Baseline**: a simple rule the model must beat to be worth using.
- **Shadow mode**: running a new system beside the old one without acting on it, to compare.
- **Token**: a small piece of text; you pay per million input tokens.
- **API key**: a secret password for your code to use Jev. Keep it out of chat, screenshots and git.
- **Environment variable**: a setting your terminal holds in memory (`TYPESAFE_API_KEY`).
