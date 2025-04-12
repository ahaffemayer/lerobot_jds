# src/features/guess_who/router.py
import logging
from fastapi import APIRouter, HTTPException, Body

# Import schemas and services for this feature
from .schema import AnimalListResponse, AskRequest, AskResponse, FilterRequest, FilterResponse, SelectAnimalResponse
from .services import ALL_CHARACTERS, filter_list, select_random_animal, answer_question

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/select_animal",
    response_model=SelectAnimalResponse,
    summary="Select AI's Secret Animal",
    description="Randomly selects an animal for the AI to 'think' of."
)
async def http_select_animal():
    """Endpoint for the AI to choose its secret animal."""
    try:
        animal = await select_random_animal()
        return SelectAnimalResponse(selected_animal=animal)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception("Unexpected error during animal selection.")
        return SelectAnimalResponse(
            selected_animal="",
            error=f"An unexpected server error occurred: {type(e).__name__}"
        )


@router.post(
    "/ask",
    response_model=AskResponse,
    summary="Ask the AI a Question",
    description="Sends a yes/no question to the AI about its secret animal."
)
async def http_ask_question(request_data: AskRequest = Body(...)):
    """
    Endpoint for the user to ask a question.
    Requires the question and the AI's current secret animal in the request body.
    """
    logger.info(f"Received question for animal '{request_data.secret_animal}': '{request_data.question}'")
    try:
        ai_answer = await answer_question(
            question=request_data.question,
            secret_animal=request_data.secret_animal
        )
        return AskResponse(answer=ai_answer)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(f"Unexpected error processing question for animal '{request_data.secret_animal}'.")
        return AskResponse(
            answer="",
            error=f"An unexpected server error occurred while processing the question: {type(e).__name__}"
        )


@router.get(
    "/animals",
    response_model=AnimalListResponse,
    summary="Get All Animal Names",
    description="Retrieves the complete list of animal names available in the game."
)
async def http_get_all_animals():
    """Endpoint to get the list of all possible animals."""
    logger.info("Request received for the list of all animals.")
    try:
        return AnimalListResponse(animals=ALL_CHARACTERS)
    except Exception as e:
        logger.exception("Unexpected error retrieving animal list.")
        return AnimalListResponse(
            animals=[],
            error=f"An unexpected server error occurred: {type(e).__name__}"
        )


@router.post(
    "/filter",
    response_model=FilterResponse,
    summary="Filter Animal List",
    description="Uses the LLM to filter the animal list based on a question and answer."
)
async def http_filter_list(request_data: FilterRequest = Body(...)):
    logger.info(f"Filtering list based on Q:'{request_data.question}', A:'{request_data.answer}'")
    try:
        kept_animals, removed_animals, reasoning = await filter_list(
            question=request_data.question,
            answer=request_data.answer,
            current_list=request_data.current_list
        )
        return FilterResponse(
            kept_animals=kept_animals,
            reasoning=reasoning,
            error=None
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception("Unexpected error during list filtering.")
        return FilterResponse(
            kept_animals=[],
            reasoning="",
            error=f"An unexpected server error occurred during filtering: {type(e).__name__}"
        )
