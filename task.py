from crewai import Task
from agents import financial_analyst
from tools import FinancialDocumentTool

financial_analysis_task = Task(
    description=(
        "Use the Financial Document Reader tool to read the document at {file_path}. "
        "Extract relevant financial metrics from the document.\n\n"
        "Then answer the following query strictly based on extracted data:\n"
        "{query}"
        "Return output in structured JSON format with:\n"
        "- summary\n"
        "- key_metrics\n"
        "- risks\n"
        "- investment_outlook\n"
        "- confidence_score"
    ),
    expected_output=(
        "Structured financial analysis including:\n"
        "- Revenue\n"
        "- Net income\n"
        "- Cash flow\n"
        "- Investment outlook\n"
        "Do not fabricate information."
    ),
    agent=financial_analyst,
    tools=[FinancialDocumentTool()],
    async_execution=False,
)