# Legal Triage OpenEnv

## Environment Description
The Legal Triage OpenEnv is an autonomous legal assistance environment designed to simulate real-world legal triage and resolution. Agents act as legal assistants who must interpret user queries, classify the legal domain, retrieve relevant statutes and precedents from a knowledge base, and draft comprehensive, structured legal advice or resolutions. The environment spans multiple jurisdictions and domains (e.g., civil disputes, criminal law, IP, corporate, family law).

## Why This Matters for RL Research
Legal triage is an excellent domain for RL research because it requires multi-step reasoning, careful balancing of partial observability, and adherence to structured, real-world constraints. Agents must navigate an action space that demands both categorical decision-making and nuanced, long-form generation. The environment trains behaviors related to meticulous document retrieval, logical chaining of arguments, and adherence to formal procedures, making it a robust testbed for real-world reward shaping and complex NLP tasks.

## Action Space
The environment expects actions in the following structured format (Pydantic Action model):
- `action_type`: Literal string, must be one of `["classify", "retrieve_doc", "draft_response", "escalate", "final_answer"]`.
- `content`: String, the actual payload or text for the action (maximum 5000 characters).

## Observation Space
The agent receives observations structured as follows (Pydantic Observation model):
- `user_query`: String, the legal facts and relief sought.
- `context_documents`: List of strings, populated if the agent uses `retrieve_doc`.
- `current_step`: Integer, tracking the number of actions taken.
- `history`: List of strings, a log of previous actions and their contents.
- `available_actions`: List of strings, the valid action types allowed.

## Tasks

| Task | Difficulty | Description | Expected Score Range |
|------|-----------|-------------|----------------------|
| legal_classification | Easy | Classify case type and urgency | 0.6–1.0 |
| legal_retrieval | Medium | Retrieve relevant statutes/precedents | 0.4–0.8 |
| legal_resolution | Hard | Full structured resolution recommendation | 0.2–0.6 |

## Reward Function
The environment employs dense reward shaping. At each step, the agent's action is evaluated by a multi-criteria weighted rubric grader, and the improvement in score is awarded as the dense reward. A step penalty of -0.02 is applied to encourage efficiency. A final step bonus of +0.1 is awarded if the agent concludes the episode with a `final_answer` and a high score (>= 0.8). Step rewards are clamped to `[0.0, 1.0]`.

## Baseline Scores
(Baseline scores will be populated after running baseline inference)

## Setup & Usage
### Local
```bash
pip install -r requirements.txt
uvicorn api.main:app --host 0.0.0.0 --port 7860
```

### Docker
```bash
docker build -t legal-triage-openenv .
docker run -p 7860:7860 \
  -e HF_TOKEN=your_token \
  -e MODEL_NAME=Qwen/Qwen2.5-72B-Instruct \
  legal-triage-openenv
```

### Run Baseline Inference
```bash
export HF_TOKEN=your_token
python inference.py
```

## OpenEnv Validation
```bash
openenv validate
```

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| HF_TOKEN | Yes | — | HuggingFace API token |
| API_BASE_URL | No | https://router.huggingface.co/v1 | LLM endpoint |
| MODEL_NAME | No | Qwen/Qwen2.5-72B-Instruct | Model identifier |
