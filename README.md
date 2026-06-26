# The Digital Saathi Prompt OS Backend

A production-ready, dynamic AI Prompt Operating System (Prompt OS) built with FastAPI. It converts structured user inputs into optimized, professional prompt directives, routing them to local models (Ollama by default) or paid LLMs (OpenAI, Gemini, Anthropic, DeepSeek, Grok) to generate marketing, sales, local maps POIs, and technical SEO crawls audits.

---

## Technical Architecture

### 1. Dynamic Form Configuration System
Forms are completely data-driven. Instead of coding new generators, you define a schema in a `config.json` file inside a module folder under `app/modules/{slug}/`:
```json
{
  "id": "instagram_reel",
  "label": "Instagram Reel Generator",
  "fields": [
    { "name": "business_name", "type": "string", "required": true },
    { "name": "industry", "type": "string", "required": true },
    { "name": "platform", "type": "enum", "options": ["Instagram", "YouTube", "Facebook"], "default": "Instagram" },
    { "name": "language", "type": "enum", "options": ["English", "Hindi", "Hinglish"], "default": "English" },
    { "name": "tone", "type": "enum", "options": ["Professional", "Casual", "Funny", "Emotional"], "default": "Professional" }
  ],
  "output_sections": ["hook", "intro", "body", "cta", "caption"],
  "template_key": "instagram_reel_v1"
}
```
Upon startup, the seeder automatically reads these JSON files, registers the generators, and links their output targets.

### 2. Prompt Construction Engine
1.  **Validate Fields**: Checks input payloads against the config's fields, casting integers and verifying enums.
2.  **Fill Defaults**: Merges missing values using default form configs and universal settings (business, industry, tone, etc.).
3.  **Improve Grammar**: Cleans trailing spaces and punctuation.
4.  **Add Hidden Instructions**: Appends critical system prompts (such as WhatsApp Hinglish locales, or short-attention span visual cues for Instagram).
5.  **Render final prompt**: interpolates variables into Jinja2 prompt bodies.

### 3. Multi-Model Router
-   **Local Model Default**: Uses Ollama (`http://localhost:11434/api/generate`) by default, utilizing local open-source models like `llama3` or `mistral`.
-   **Paid Adapters**: Plug in OpenAI, Gemini, Anthropic, DeepSeek, or Grok. The router automatically falls back to Ollama if API key variables are not set in the `.env` configuration.
-   **Fan-out Parallelism**: Supports fanning out prompts to multiple models concurrently, returning comparison text results.

---

## Installation & Setup

### 1. Configure Environment
Copy the example variables file to `.env`:
```bash
cp .env.example .env
```
Fill in the database connections or AI provider API keys.
*Note: If no paid API keys are provided, the backend falls back to local Ollama (and uses connection fallbacks) to ensure the system is testable immediately.*

### 2. Local Run
Install dependencies:
```bash
pip install -r requirements.txt
```
Run database tables creations and seeder:
```bash
python -m app.seed
```
Launch the uvicorn development server:
```bash
uvicorn app.main:app --reload
```
View the Swagger UI endpoints documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 3. Running via Docker Compose
To run FastAPI, Postgres database, Redis cache, and Celery workers:
```bash
docker-compose up --build
```

---

## Seed Credentials
*   **Super Admin User**:
    *   **Email**: `admin@digitalsaathi.com`
    *   **Password**: `admin123`
*   **Seeded Modules**: Instagram Reel, Video Script, Viral Hook, Image Prompt, SEO Content, and Email Campaign writers.

---

## How to Add a New Generator Form (No Code Changes)
1.  Create a new directory under `app/modules/{new_slug}/`.
2.  Place a `config.json` inside it defining the input fields and expected output sections.
3.  Add `new_slug` to the `MODULE_SLUGS` list in `app/seed.py` and register the corresponding prompt templates in `TEMPLATE_BODIES`.
4.  Run `python -m app.seed` or restart the app. The generator endpoint `POST /api/v1/generators/{new_slug}/generate` is instantly active.
