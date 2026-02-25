
# Financial Document Analyzer

**CrewAI Debug Assignment – VWO**

## Overview

This project implements an AI-powered financial document analyzer using FastAPI and CrewAI. The system accepts a financial PDF along with a user query, processes it asynchronously using LLM agents, and returns structured financial insights in JSON format.

The primary objective of this assignment was to debug the provided system, resolve architectural and dependency issues, stabilize LLM output handling, and implement persistent storage for analysis results.

The final version is fully working, produces structured responses, and includes database integration for tracking and storing analysis results.



## System Architecture

The application follows an asynchronous job-based design:

1. A user uploads a financial PDF and submits a query via `/analyze`.
2. A unique `job_id` is generated.
3. A database record is created with status set to `processing`.
4. A background task executes the CrewAI pipeline.
5. The structured output is stored in SQLite.
6. The client polls `/result/{job_id}` to retrieve the final result.

This approach prevents long-running blocking HTTP requests and makes the system more scalable and production-oriented.



## Tech Stack

* **FastAPI** – API layer
* **CrewAI** – Multi-agent orchestration
* **OpenAI (LLM Provider)** – Language model processing
* **SQLite (sqlite3)** – Persistent storage
* **Python 3.11** – Runtime environment


## Project Structure

financial-document-analyzer/
│
├── main.py               # FastAPI entry point
├── agents.py             # CrewAI agent definitions
├── tasks.py              # Agent task configurations
├── process.py            # Document processing logic
├── database.py           # SQLite integration layer
├── requirements.txt
├── analysis.db           # SQLite database (generated at runtime)
└── README.md

The application is modularized to clearly separate:

API layer

Agent orchestration

Processing pipeline

Database layer

## Setup Instructions

### Prerequisites

* Python 3.11 (required due to chroma-hnswlib compatibility)

### Installation

```bash
pip install -r requirements.txt
```

### Run the Server

```bash
uvicorn main:app --reload
```

Open the API documentation:

```
http://127.0.0.1:8000/docs
```

---

## API Documentation

### 1. POST `/analyze`

Uploads a financial PDF and submits a query.

**Request (multipart/form-data):**

* `file`: Financial PDF
* `query`: Financial question

**Response:**

```json
{
  "status": "processing",
  "job_id": "generated-uuid",
  "message": "Document submitted successfully. Use /result/{job_id} to fetch result."
}
```

Processing happens in the background.

---

### 2. GET `/result/{job_id}`

Returns the status and final result.

If still processing:

```json
{
  "status": "processing"
}
```

If completed:

```json
{
  "job_id": "...",
  "file_name": "...",
  "query": "...",
  "status": "completed",
  "result": { structured financial analysis },
  "execution_time": 95.4,
  "created_at": "timestamp"
}
```

Polling is required because the analysis typically takes 60–120 seconds depending on LLM execution time.


## How to Test the System

### 1. Start the server:

uvicorn main:app --reload

### 2. Open Swagger:

http://127.0.0.1:8000/docs

### 3. Use POST /analyze:

* Upload a financial PDF

* Enter a financial query

### 4. Copy the returned job_id.

### 5. Use GET /result/{job_id}:

* If status = processing, wait and retry

* If status = completed, structured JSON result will be returned

Average processing time: 60–120 seconds.


## Database Integration (Bonus Implemented)

SQLite (`analysis.db`) is used to persist:

* Job ID
* File name
* Query
* Status
* Structured result
* Execution time
* Timestamp

Since raw `sqlite3` (no ORM) is used, JSON serialization is handled explicitly:

* `json.dumps()` before storing results
* `json.loads()` when retrieving results

This ensures clean API responses and prevents double JSON encoding issues.


## Bugs Identified and Fixed

During debugging, the following issues were identified and resolved:

### 1. Dependency Conflict (click version)

`click==8.1.7` was incompatible with `crewai-tools`.

**Fix:**
Aligned dependency versions to ensure compatibility.


### 2. chroma-hnswlib Build Failure (Python 3.12)

The package failed to build under Python 3.12.

**Fix:**
Downgraded environment to Python 3.11 to ensure stable installation.


### 3. CrewAI Import Path Changes

Agent and tool imports had changed in newer versions.

**Fix:**

```python
from crewai import Agent
from crewai_tools import SerperDevTool
```

### 4. NameError: LLM Not Defined

The LLM instance was referenced before being properly initialized and injected into agents.

**Fix:**
Explicitly instantiated the LLM and ensured it was correctly passed into agent configurations.

### 5. Incorrect BaseTool Implementation

The custom tool did not fully comply with CrewAI’s expected interface.

**Fix:**
Refactored the implementation to properly extend and align with CrewAI’s BaseTool structure.

### 6. Function Name Shadowing

A function name conflicted with a variable name, causing unexpected behavior.

**Fix:**
Renamed identifiers to prevent shadowing and improve clarity.

Then renumber th

### 7. OpenAI Rate Limit Errors

Frequent rate limits during testing caused failures.

**Fix:**
Improved error handling and structured the code to support easy switching to alternate providers if required.


### 8. Double JSON Encoding Issue

API responses were returning escaped JSON with `\n`, `\"`, and schema showing `"string"`.

**Root Cause:**
Results were being serialized twice before returning from FastAPI.

**Fix:**

* Serialize only when storing in SQLite
* Deserialize before returning from API
* Refactored database layer to return structured dictionaries


### 9. KeyError After Refactoring Database Layer

After modifying `get_job()` to return a dictionary instead of a tuple, the API layer still accessed tuple indices.

**Fix:**
Updated the API layer to return dictionary objects directly.


## Design Decisions

* Used asynchronous background tasks instead of blocking requests.
* Implemented structured JSON output instead of free-text responses.
* Used SQLite for portability and simplicity.
* Explicitly handled JSON serialization due to raw `sqlite3` usage.
* Separated API logic, processing logic, and database logic.

The system is minimal but designed in a way that it can be extended to a queue-based worker architecture (Redis/Celery) if needed.


## Bonus Points Implemented

✔ Database integration for storing analysis results and metadata
✔ Structured output handling
✔ Stable asynchronous processing model


## Future Improvements

* Redis + Celery worker model for concurrent request handling
* Retry mechanism for failed jobs
* Improved logging and monitoring
* Lightweight frontend dashboard for job tracking


## Key Engineering Improvements

Beyond fixing surface-level bugs, the following structural improvements were implemented:

* Clean separation of concerns (API, processing, database)
* Reliable JSON serialization pattern for SQLite
* Background task processing model
* Structured output enforcement for LLM responses
* Improved error handling for API failures


## Final Notes

This assignment focused on debugging and stabilizing the existing system rather than expanding feature scope. The final solution:

* Runs reliably
* Produces structured financial analysis
* Handles asynchronous execution properly
* Stores results persistently
* Resolves dependency and serialization issues

All identified bugs have been documented and fixed.
