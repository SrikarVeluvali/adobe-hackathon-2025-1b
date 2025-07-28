# Adobe Hackathon – Round 1B: Persona-Driven Document Intelligence

## Overview

This round challenges participants to go beyond traditional document analysis by **extracting relevant content from multiple PDFs** based on a given **persona** and their **job-to-be-done**. The task is to simulate intelligent reading tailored to the user’s intent—surfacing only the most useful document sections and insights.


## Objective

Given:

* A **set of documents**
* A defined **persona** (e.g., Travel Planner, HR Professional)
* A **job to be done**

You must return:

* A ranked list of **relevant document sections**
* A **subsection analysis** that highlights the refined, useful text snippets

## Approach

### 1. **Understanding Context**

Each `input.json` includes:

* Persona: their role, domain, and perspective
* Job-to-be-done: task they are trying to achieve
* PDF collection relevant to that task

### 2. **Content Parsing**

* PDFs are preprocessed and segmented into sections (titles, paragraphs, etc.)
* Metadata (document name, page number) is retained

### 3. **Relevance Scoring**

For each section:

* Calculated semantic similarity between the **job-to-be-done** and **document sections**
* Scored based on **persona-specific keywords**, **task relevance**, and **location (e.g., introductory summaries, lists, guides)**

### 4. **Subsection Extraction**

* Top-ranked sections are analyzed more deeply
* Short, useful passages are extracted for clarity and brevity
* Applied regex and chunking to refine and format text

### 5. **Output Formatting**

Output includes:

* Metadata: persona, job, input files, timestamp
* Extracted Sections: title, page, rank
* Subsection Analysis: meaningful passages tied to user intent

### Tools Used

* Python (PDF parsing, NLP)
* `PyMuPDF`, `pdfplumber` for PDF handling
* `spaCy`, `sentence-transformers` for NLP embedding/similarity
* Lightweight models (<1GB, CPU-friendly)

## Docker & Constraints

* CPU only (no GPU/internet)
* Model size ≤ 1GB
* Execution time ≤ 60 seconds for 3–5 PDFs

```bash
docker build --platform linux/amd64 -t persona-analyzer .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none persona-analyzer
```
