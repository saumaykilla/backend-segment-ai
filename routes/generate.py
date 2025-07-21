from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List
import asyncio
import logging
import time

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

router = APIRouter()

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Prompt dictionary
CATEGORY_PROMPTS = {
    "Marketing OKRs": (
        "What are 3 measurable marketing OKRs to grow usage in the {segment} segment for the {product} to help {business_objective}?"),
    "Strengths": ("What product strengths matter most to a {segment} for the {product} to help {business_objective}?"),
    "Weaknesses": ("What would the {segment} be concerned about or dislike about the {product}  to help {business_objective}?"),
    "Opportunities":( "What product or brand opportunities can we unlock by targeting the {segment} with the {product} to help {business_objective}?"),
    "Threats": ("What risks might prevent the {segment} from adopting or staying loyal to the {product} to help {business_objective}?"),
    "Market Positioning": ("How should we position the {product} to resonate with the {segment} to help {business_objective}?"),
    "Buyer Persona":( "Write a sample persona for a typical {segment} customer of the {product} to help {business_objective}."),
    "Investment Opportunities": ("Why is the {segment} segment strategically valuable for growth/investment in the {product} to help {business_objective}?"),
    "Channels & Distribution": ("How should we reach and activate the {segment} for the {product} to help {business_objective}?")
}

# SWOT expansion mapping
SWOT_MAPPING = ["Strengths", "Weaknesses", "Threats", "Opportunities"]

# Pydantic schemas
class InsightResponse(BaseModel):
    insights: List[str]

class PromptInput(BaseModel):
    product: str
    business_objective: str
    segment: str
    focus_areas: List[str]

# Async function for one category
async def run_prompt(product, business_objective, segment, category):
    start = time.time()
    logger.info(f"⏳ Starting prompt for: {category}")
    try:
        prompt_template = CATEGORY_PROMPTS[category]

        prompt_str = f"""
{prompt_template}
  
  Please respond ONLY with a JSON object matching this schema:
{{{{ 
  "insights": [
    "string",
    "string",
    "string"
  ]
}}}}


    Do NOT use key-value pairs inside the "insights" array.
    Do NOT add markdown or formatting.
""".strip()
        
        prompt = PromptTemplate(
            input_variables=["product", "business_objective", "segment"],
            template=prompt_str
        )
        parser = PydanticOutputParser(pydantic_object=InsightResponse)
        chain = prompt | llm | parser

        result = await chain.ainvoke({
            "product": product,
            "business_objective": business_objective,
            "segment": segment,
        })

        logger.info(f"✅ Completed category: {category} in {round(time.time() - start, 2)}s")
        return {category: result.insights}

    except Exception as e:
        logger.error(f"❌ Error in category {category}: {str(e)}")
        return None

# POST endpoint for prompt generation with SWOT expansion
@router.post("/generate")
async def generate_insights(request: Request, body: PromptInput):
    try:
        user = getattr(request.state, "user", None)
        if not user:
            return {"error": "Not authorized"}

        logger.info(f"Authenticated user: {user}")
        logger.info(f"📥 Request received with focus areas: {body.focus_areas}")

        # Expand SWOT Analysis into its components
        expanded_focus_areas = []
        for area in body.focus_areas:
            if area == "SWOT Analysis":
                expanded_focus_areas.extend(SWOT_MAPPING)
            else:
                expanded_focus_areas.append(area)

        tasks = [
            run_prompt(body.product, body.business_objective, body.segment, category)
            for category in expanded_focus_areas
        ]

        results = await asyncio.gather(*tasks)

        final_output = {}
        for res in results:
            if res:
                final_output.update(res)
        return final_output

    except Exception as e:
        logger.exception("Internal Server Error")
        return {"error": "Internal Server Error"}
