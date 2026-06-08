# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain
This project covers Riverside State University (RSU) campus dining: student reviews, wait times, meal plan advice, vegetarian/vegan options, and late-night food. This knowledge is useful because official dining pages mostly provide menus and hours, but students need practical details such as actual lunch wait times, which plan saves money, and where to eat near specific buildings. The information exists, but it is scattered across threads and informal guides that are hard to search quickly.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | North Dining Hall reviews | Reddit thread export | `documents/north_hall_reviews.txt` |
| 2 | South Quad Cafe guide | Student wiki export | `documents/south_quad_cafe.txt` |
| 3 | West Market reviews | Student forum thread export | `documents/west_market_reviews.txt` |
| 4 | East Commons survey | Student government summary export | `documents/east_commons_dining.txt` |
| 5 | Meal plan comparison | Unofficial survival guide export | `documents/meal_plan_guide.txt` |
| 6 | Vegetarian/Vegan guide | Student club guide export | `documents/vegetarian_vegan_options.txt` |
| 7 | Late-night eating megathread | Reddit thread export | `documents/late_night_eating.txt` |
| 8 | Weekend brunch guide | Campus life blog export | `documents/brunch_weekend_dining.txt` |
| 9 | Food truck schedule | Student activities export | `documents/food_trucks_campus.txt` |
| 10 | Dining wait-time log | Crowdsourced spreadsheet summary export | `documents/dining_wait_times.txt` |
| 11 | Budget eating tips | Reddit pinned post export | `documents/budget_eating_tips.txt` |
| 12 | Coffee + study spots | Student Notion guide export | `documents/coffee_study_spots.txt` |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 400 characters

**Overlap:** 80 characters

**Why these choices fit your documents:**  
The corpus mixes short reviews with longer guide sections. A 400-character chunk keeps each chunk focused on one idea (for example, one wait-time pattern or one opinion block), while the 80-character overlap reduces information loss when a key fact sits near a boundary. I also clean text by unescaping entities, removing HTML tags, normalizing whitespace, and removing URL noise before chunking.

**Final chunk count:** 77 chunks across 12 documents

### Sample chunks

**Chunk 1** — Source: `brunch_weekend_dining.txt` (chunk index 0)

> Source document: brunch_weekend_dining.txt  
> Weekend dining at Riverside State University is different from weekdays. Only two locations serve brunch, and hours are shorter. East Commons (Saturday-Sunday 9:00 AM - 2:00 PM): The premier weekend brunch destination. Made-to-order omelet station, waffle bar with toppings (berries, whipped cream, chocolate chips)...

**Chunk 2** — Source: `coffee_study_spots.txt` (chunk index 5)

> Source document: coffee_study_spots.txt  
> No real coffee shop on the 3rd floor, but vending machines sell canned cold brew ($3). Silent study policy makes it the best focus environment (5/5 study rating). Many students buy at South Quad and walk to the library. Study spot rankings from student poll: 1. South Quad Cafe (coffee + study combo) 2. Library 3rd floor...

**Chunk 3** — Source: `food_trucks_campus.txt` (chunk index 5)

> Source document: food_trucks_campus.txt  
> Dessert Truck "Sweet Wheels" (2 PM - 6 PM): Cookies, brownies, ice cream sandwiches. Student tips: Food truck lines are shortest 11:00-11:30 AM and after 2:00 PM. Download the "RSU Eats" app for real-time truck locations. Dining dollars work at all trucks but cannot be used for meal plan swipes.

**Chunk 4** — Source: `north_hall_reviews.txt` (chunk index 4)

> Source document: north_hall_reviews.txt  
> Made-to-order omelets open at 7 AM and there's almost no wait before 8:30. The waffle maker is self-serve. Lunch is chaos — eat at 11:15 or after 1:30." Review by u/transfer_student_22: "Compared to my old school, North Hall portions are huge. One swipe gets you unlimited trips...

**Chunk 5** — Source: `west_market_reviews.txt` (chunk index 5)

> Source document: west_market_reviews.txt  
> Sunday 10:00 AM - 9:00 PM. Student consensus: Best for engineering/science students who need proximity. Food quality 3/5. Convenience 5/5. Wait times 2.5/5 at lunch peak.

Each chunk is self-contained enough to answer a focused question (brunch hours, study spots, food truck tips, North Hall timing advice, West Market proximity).

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**  
Primary intended model: `all-MiniLM-L6-v2` via sentence-transformers.  
Actual run in this environment: fallback TF-IDF embeddings (`tfidf-fallback`) because `huggingface.co` DNS resolution failed and the model could not be downloaded.

**Production tradeoff reflection:**  
If deploying this for real users, I would prefer a stronger semantic embedding model once network access is stable, because it handles paraphrased queries better than TF-IDF keyword overlap. I would trade some latency and cost for improved semantic matching, especially on informal student language. I would also compare top-k quality and retrieval distances between local and API-hosted embeddings before selecting a final production setup.

---

## Retrieval Test Results

Tested with `python retrieve.py` (top-k = 5). Lower distance = stronger match.

### Query 1: What are the wait times at North Dining Hall during lunch peak?

| Rank | Distance | Source | Top chunk (excerpt) |
|------|----------|--------|---------------------|
| 1 | 0.7561 | west_market_reviews.txt | "...Wait times 2.5/5 at lunch peak." |
| 2 | 0.8094 | dining_wait_times.txt | "This document summarizes average wait times collected by student volunteers..." |
| 3 | 0.8293 | north_hall_reviews.txt | Rating summary: "Wait times 2/5 at peak lunch..." |
| 4 | 0.8641 | north_hall_reviews.txt | "North Dining Hall is the largest dining hall on the Riverside State University campus..." |
| 5 | 0.9110 | dining_wait_times.txt | "...Food trucks: Average 10-15 minutes at lunch peak..." |

**Why these chunks are relevant:** Results #2–#4 come from the wait-time log and North Hall review documents, which directly discuss North Dining Hall lunch congestion and wait times. Result #1 is partially off-target (West Market wait times), which shows a retrieval weakness when multiple documents mention "wait times" with similar keywords.

### Query 2: Which dining hall is best for vegan students?

| Rank | Distance | Source | Top chunk (excerpt) |
|------|----------|--------|---------------------|
| 1 | 0.8623 | north_hall_reviews.txt | North Dining Hall overview and reviews |
| 2 | 0.8992 | vegetarian_vegan_options.txt | "...look for the green VEGAN sticker... Burrito bowls: choose tofu or beans..." |
| 3 | 0.9069 | west_market_reviews.txt | West Market proximity/consensus |
| 4 | 0.9123 | north_hall_reviews.txt | "...vegan chili on Wednesdays is the best plant-based hot meal on campus..." |
| 5 | 0.9132 | vegetarian_vegan_options.txt | "...Rated best dining hall for vegans... East Commons..." |

**Why these chunks are relevant:** Results #2 and #5 are from the dedicated vegetarian/vegan guide and mention vegan options and dining-hall recommendations. Results #1 and #4 mention vegan food at North Hall, which is related but can mislead generation if ranked too high — this contributed to the failure case in the evaluation report.

### Query 3: What late-night food options are available on campus after 9 PM?

| Rank | Distance | Source | Top chunk (excerpt) |
|------|----------|--------|---------------------|
| 1 | 0.6783 | late_night_eating.txt | "Where to eat after 9 PM on campus" — limited late-night options |
| 2 | 0.8925 | late_night_eating.txt | Pro tip about keeping dining dollars for late-night West Market runs |
| 3 | 0.8965 | late_night_eating.txt | West Market late-night option: chicken tenders, pizza, ramen bar, convenience store |
| 4 | 0.9173 | dining_wait_times.txt | Late night wait times (5-8 minutes) |
| 5 | 0.9372 | dining_wait_times.txt | South Quad Cafe lunch line times |

**Why these chunks are relevant:** The top three results all come from `late_night_eating.txt`, which is exactly the document that lists West Market, the Night Owl truck, and convenience-store options after 9 PM. This is the strongest retrieval result of the three test queries.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**  
The system prompt explicitly says: answer using only provided excerpts, do not use outside knowledge, and if context is insufficient, return exactly `"I don't have enough information on that."` It also forbids inventing hours, prices, ratings, or wait times.

**How source attribution is surfaced in the response:**  
Each retrieved chunk includes `source` metadata and chunk index. The generation context is formatted with source labels per excerpt, and the final response returns a `sources` list programmatically, so attribution is always available even if the LLM omits it in prose.

---

## Example Responses

### Example 1 — Grounded answer with source attribution

**Query:** What are the wait times at North Dining Hall during lunch peak?

**Answer:** The wait times at North Dining Hall during lunch peak (11:45 AM - 1:15 PM) are 18-25 minutes at stir-fry and grill. (dining_wait_times.txt)

**Retrieved from:**
- dining_wait_times.txt
- north_hall_reviews.txt
- west_market_reviews.txt

---

### Example 2 — Grounded answer with source attribution

**Query:** What late-night food options are available on campus after 9 PM?

**Answer:** According to late_night_eating.txt, the late-night food options available on campus after 9 PM are:
1. West Market (open until 11 PM weekdays) which offers chicken tenders, pizza by the slice, and a ramen bar.
2. The convenience store for instant noodles and snacks, and salad cups (usually sold out by 10 PM).
3. The Night Owl truck, but it has zero healthy options.

Note that South Quad Cafe is only an option during final exam reading days, extending its hours to midnight, but not during normal weeks.

**Retrieved from:**
- dining_wait_times.txt
- late_night_eating.txt

---

### Example 3 — Out-of-scope refusal

**Query:** What is the acceptance rate for RSU medical school?

**Answer:** I don't have enough information on that.

**Retrieved from:**
- east_commons_dining.txt
- late_night_eating.txt
- meal_plan_guide.txt
- north_hall_reviews.txt
- west_market_reviews.txt

The system retrieved dining-related chunks (none contain medical school information) and correctly refused to answer rather than inventing an acceptance rate from general knowledge.

---

## Query Interface

The system uses a **Gradio** web UI (`app.py`). To launch it:

```powershell
.\.venv\Scripts\Activate.ps1
python app.py
```

Then open the local URL printed in the terminal (typically `http://127.0.0.1:7860`).

### Input and output fields

| Field | Type | Description |
|-------|------|-------------|
| **Your question** | Text input (2 lines) | Where the user types a natural-language question about RSU campus dining. Placeholder example: *"What are lunch wait times at North Dining Hall?"* |
| **Ask** | Button | Submits the question to the RAG pipeline (retrieve → generate). The user can also press Enter in the question box. |
| **Answer** | Text output (8 lines) | The grounded response generated by Groq using only retrieved document excerpts. |
| **Retrieved from** | Text output (4 lines) | Bulleted list of source filenames (`documents/*.txt`) for the chunks passed into generation. |

### Sample interaction transcript

```
[Your question]
What are the wait times at North Dining Hall during lunch peak?

[User clicks "Ask"]

[Answer]
The wait times at North Dining Hall during lunch peak (11:45 AM - 1:15 PM) are
18-25 minutes at stir-fry and grill. (dining_wait_times.txt)

[Retrieved from]
• dining_wait_times.txt
• north_hall_reviews.txt
• west_market_reviews.txt
```

This interaction shows the full loop: the user asks a specific question, the system returns a grounded answer with an inline source citation, and the **Retrieved from** panel lists which document files supplied the context.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What are the wait times at North Dining Hall during lunch peak? | 18–25 minutes at key stations during peak lunch. | Returned 18–25 minutes at stir-fry and grill during lunch peak. | Partially relevant (one top chunk off-target, others relevant) | Accurate |
| 2 | Which dining hall is best for vegan students? | East Commons, based on club ratings and dedicated station. | Returned North Hall as best for vegans. | Partially relevant | Inaccurate |
| 3 | What late-night food options are available on campus after 9 PM? | West Market, Night Owl truck, and Student Union convenience store. | Returned West Market, Night Owl truck, and convenience options with schedule details. | Relevant | Accurate |
| 4 | Is the unlimited meal plan worth it? | Worth it mainly if eating on campus >14 meals/week. | Returned that unlimited is worth it if eating on campus more than ~14 meals/week. | Relevant | Accurate |
| 5 | Where can I get the best coffee on campus for studying? | South Quad Cafe. | Returned South Quad Cafe as best coffee + study option. | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**  
Which dining hall is best for vegan students?

**What the system returned:**  
It answered that North Hall is best for vegans, which conflicts with the expected answer (East Commons).

**Root cause (tied to a specific pipeline stage):**  
This is primarily a retrieval-stage issue caused by fallback TF-IDF embeddings. Because TF-IDF emphasizes literal token overlap rather than semantics, chunks mentioning “vegan” from North Hall reviews scored similarly to the East Commons recommendation chunk. The generation stage then synthesized the wrong top signal.

**What you would change to fix it:**  
Restore semantic embeddings (`all-MiniLM-L6-v2`) once DNS/network access to Hugging Face is available, then retune top-k and optionally add a reranker. I would also add metadata-aware filtering (boost chunks from the vegetarian guide when query contains “vegan/vegetarian”).

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**  
The spec made implementation much faster by locking in concrete numbers early (400/80 chunking, top-k=5, ChromaDB, Groq model). That prevented scope drift and let me validate each stage against a checklist instead of guessing defaults.

**One way your implementation diverged from the spec, and why:**  
The implementation diverged at the embedding step: I could not download `all-MiniLM-L6-v2` due repeated DNS failures for `huggingface.co`, so I added an offline TF-IDF fallback to keep the end-to-end system functional. This made retrieval less semantic than planned, which is visible in the vegan failure case.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* My planning.md Documents section, chunk size/overlap requirements, and architecture stage definitions.
- *What it produced:* Initial ingestion and chunking scripts (`ingest.py`, `chunk.py`) with metadata attachment.
- *What I changed or overrode:* I added stricter cleaning and ensured every chunk carries source metadata and chunk index, then manually inspected sample chunks and adjusted formatting.

**Instance 2**

- *What I gave the AI:* Retrieval and grounding requirements (top-k retrieval, context-only answering, explicit fallback string when context is missing, source attribution in output).
- *What it produced:* `embed.py`, `retrieve.py`, `query.py`, and Gradio interface (`app.py`).
- *What I changed or overrode:* I implemented a TF-IDF fallback path and vectorizer persistence after embedding model download failures, and verified end-to-end behavior with five evaluation questions plus an out-of-scope query.
