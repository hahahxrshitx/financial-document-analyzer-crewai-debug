## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import tools
from crewai_tools import SerperDevTool

from crewai.tools import BaseTool
import fitz  # PyMuPDF

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
from crewai.tools import BaseTool
import fitz


class FinancialDocumentTool(BaseTool):
    name: str = "Financial Document Reader"
    description: str = (
        "Reads and extracts text from a financial PDF document. "
        "Input must be a file path string."
    )

    def _run(self, file_path: str) -> str:
        text = ""
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        return text

## Creating Investment Analysis Tool
class InvestmentTool:
    async def analyze_investment_tool(financial_document_data):
        # Process and analyze the financial document data
        processed_data = financial_document_data
        
        # Clean up the data format
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":  # Remove double spaces
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
                
        # TODO: Implement investment analysis logic here
        return "Investment analysis functionality to be implemented"

## Creating Risk Assessment Tool
class RiskTool:
    async def create_risk_assessment_tool(financial_document_data):        
        # TODO: Implement risk assessment logic here
        return "Risk assessment functionality to be implemented"