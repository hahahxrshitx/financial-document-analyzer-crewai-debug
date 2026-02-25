from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import json

from crewai import Crew, Process
from agents import financial_analyst
from task import financial_analysis_task
import time
from fastapi import BackgroundTasks
from database import init_db, create_job, update_job, get_job
from agents import verifier, risk_assessor, investment_advisor


app = FastAPI(title="Financial Document Analyzer")
init_db()

def run_crew(query: str, file_path: str="data/sample.pdf"):
    """To run the whole crew"""
    financial_crew = Crew(
        agents=[
            verifier,
            financial_analyst,
            risk_assessor,
            investment_advisor
        ],
        tasks=[financial_analysis_task],
        process=Process.sequential,
    )
    
    result = financial_crew.kickoff({
        "query": query,
        "file_path": file_path})
    return result
def process_document(job_id: str, query: str, file_path: str):
    try:
        start_time = time.time()

        response = run_crew(query=query, file_path=file_path)

        execution_time = round(time.time() - start_time, 2)

        # Clean markdown formatting if LLM returned ```json ... ```
        cleaned_response = str(response).strip()

        if cleaned_response.startswith("```"):
            cleaned_response = cleaned_response.split("```")[1].strip()

        # Try parsing into proper JSON
        try:
            parsed_response = json.loads(cleaned_response)
        except Exception:
            parsed_response = cleaned_response

        update_job(
            job_id=job_id,
            status="completed",
            result=json.dumps(parsed_response),
            execution_time=execution_time
        )

    except Exception as e:
        update_job(
            job_id=job_id,
            status="failed",
            result=str(e),
            execution_time=0
        )

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_document_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):

    job_id = str(uuid.uuid4())
    file_path = f"data/{job_id}.pdf"

    os.makedirs("data", exist_ok=True)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    if not query or query.strip() == "":
        query = "Analyze this financial document for investment insights"

    # Save job in DB
    create_job(job_id, file.filename, query)

    # Run crew in background
    background_tasks.add_task(
        process_document,
        job_id,
        query.strip(),
        file_path
    )

    return {
        "status": "processing",
        "job_id": job_id,
        "message": "Document submitted successfully. Use /result/{job_id} to fetch result."
    }

@app.get("/result/{job_id}")
async def get_result(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)