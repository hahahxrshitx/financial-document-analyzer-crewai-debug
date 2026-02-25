## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()


from crewai import Agent

from tools import FinancialDocumentTool

### Loading LLM
from crewai import LLM
import os

llm = LLM(
    model="openrouter/mistralai/mistral-7b-instruct",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
# Creating an Experienced Financial Analyst agent
financial_analyst=Agent(
    role="Senior Financial Analyst Who Knows Everything About Markets",
    goal="Analyze the provided financial document carefully and provide data-backed financial insights based strictly on the document contents: {query}",
    memory=True,
    backstory=(
    "You are a senior financial analyst with deep expertise in interpreting financial reports, earnings statements, and market indicators. "
    "You rely strictly on documented financial data and avoid speculation. "
    "You ensure all conclusions are derived directly from the financial document provided."
    ),
    tools=[FinancialDocumentTool()],
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True  # Allow delegation to other specialists
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify whether the uploaded document is a legitimate financial document by checking for financial terminology, structured financial data, and relevant financial indicators.",
    verbose=True,
    memory=True,
   backstory=(
    "You are a compliance-focused financial document reviewer. "
    "You carefully validate whether the document contains legitimate financial data "
    "such as income statements, balance sheets, cash flow statements, or earnings reports."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=True
)


investment_advisor = Agent(
    role="Investment Guru and Fund Salesperson",
    goal="Provide balanced, risk-aware investment recommendations based strictly on insights derived from the financial document.",
    verbose=True,
    backstory=(
    "You are a certified financial advisor with experience in portfolio management and regulatory compliance. "
    "You provide responsible, diversified, and risk-aware investment suggestions based only on validated financial data."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)


risk_assessor = Agent(
    role="Extreme Risk Assessment Expert",
    goal="Assess financial risks objectively using financial metrics and document evidence, avoiding exaggeration or speculation.",
    verbose=True,
    backstory=(
    "You are a professional risk analyst who evaluates financial volatility, debt ratios, liquidity risk, and macroeconomic exposure "
    "based strictly on documented financial data."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)
