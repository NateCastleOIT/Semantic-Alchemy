"""
FastAPI backend for the Alchemy Engine.
Provides REST API endpoints with hot-reload support.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from alchemy_engine.database import AlchemyDatabase
from alchemy_engine.generator import ElementGenerator
from alchemy_engine.engine import AlchemyEngine
from alchemy_engine.seed_data import initialize_base_elements
from alchemy_engine.config import DATABASE_PATH


# Initialize FastAPI app
app = FastAPI(
    title="Semantic Alchemy API",
    description="REST API for the semantic alchemy combination game",
    version="1.0.0"
)

# Configure CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize game components
database = AlchemyDatabase(DATABASE_PATH)
generator = ElementGenerator()
engine = AlchemyEngine(database, generator)
initialize_base_elements(database)


# Pydantic models for request/response
class CombineRequest(BaseModel):
    element1_id: str  # UUID string
    element2_id: str  # UUID string


class ElementResponse(BaseModel):
    id: str  # UUID string
    name: str
    emoji: str  # Maps to visual_hint
    definition: str  # Maps to description
    is_base: bool


class CombineResponse(BaseModel):
    success: bool
    result: Optional[ElementResponse] = None
    message: str
    was_discovered: bool = False


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "message": "Semantic Alchemy API is running",
        "docs": "/docs"
    }


@app.get("/elements", response_model=List[ElementResponse])
async def get_all_elements():
    """Get all discovered elements."""
    elements = database.get_all_elements()
    return [
        ElementResponse(
            id=elem.id,
            name=elem.name,
            emoji=elem.visual_hint,
            definition=elem.description,
            is_base=elem.is_base
        )
        for elem in elements
    ]


@app.get("/elements/{element_id}", response_model=ElementResponse)
async def get_element(element_id: str):
    """Get a specific element by ID."""
    element = database.get_element(element_id)
    if not element:
        raise HTTPException(status_code=404, detail="Element not found")

    return ElementResponse(
        id=element.id,
        name=element.name,
        emoji=element.visual_hint,
        definition=element.description,
        is_base=element.is_base
    )


@app.post("/combine", response_model=CombineResponse)
async def combine_elements(request: CombineRequest):
    """Combine two elements to create a new one."""
    # Get elements
    elem1 = database.get_element(request.element1_id)
    elem2 = database.get_element(request.element2_id)

    if not elem1 or not elem2:
        raise HTTPException(status_code=404, detail="One or both elements not found")

    # Try to combine - pass Element objects, not names
    result = engine.combine(elem1, elem2)

    if result:
        # Check if this was a new discovery
        was_discovered = not database.get_combination(f"{elem1.id}+{elem2.id}")

        return CombineResponse(
            success=True,
            result=ElementResponse(
                id=result.id,
                name=result.name,
                emoji=result.visual_hint,
                definition=result.description,
                is_base=result.is_base
            ),
            message=f"Created: {result.name}",
            was_discovered=was_discovered
        )
    else:
        return CombineResponse(
            success=False,
            message=f"Cannot combine {elem1.name} and {elem2.name}"
        )


@app.get("/stats")
async def get_stats():
    """Get game statistics."""
    all_elements = database.get_all_elements()
    base_elements = [e for e in all_elements if e.is_base]
    discovered_elements = [e for e in all_elements if not e.is_base]

    return {
        "total_elements": len(all_elements),
        "base_elements": len(base_elements),
        "discovered_elements": len(discovered_elements)
    }


if __name__ == "__main__":
    import uvicorn
    print("Starting Semantic Alchemy API...")
    print("API Documentation: http://localhost:8000/docs")
    print("Hot reload enabled - changes will auto-update")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
