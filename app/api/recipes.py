from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from models import db_helper, Recipe
from pydantic import BaseModel
from config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter(
    tags=["Recipes"],
    prefix=settings.url.recipes,
)


class RecipeRead(BaseModel):
    id: int
    title: str
    description: str
    cooking_time: int
    difficulty: int

class RecipeCreate(BaseModel):
    title: str
    description: str
    cooking_time: int
    difficulty: int


@router.get("", response_model=list[RecipeRead])
async def index(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    stmt = select(Recipe).order_by(Recipe.id)
    recipes = await session.scalars(stmt)
    print(recipes)
    print(recipes.all())
    return recipes.all()


@router.post("", response_model=RecipeRead, status_code=status.HTTP_201_CREATED)
async def store(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    recipe_create: RecipeCreate
):
    recipe = Recipe(
        title=recipe_create.title,
        description=recipe_create.description,
        cooking_time=recipe_create.cooking_time,
        difficulty=recipe_create.difficulty
    )
    session.add(recipe)
    await session.commit()
    return recipe

@router.get("/{id}", response_model=RecipeRead)
async def show(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    id: int,
):
    recipe = await session.get(Recipe, id)
    return recipe


@router.put("/{id}", response_model=RecipeRead)
async def update(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    id: int,
    recipe_update: RecipeCreate
):
    recipe = await session.get(Recipe, id)
    recipe.title = recipe_update.title
    recipe.description = recipe_update.description
    recipe.cooking_time = recipe_update.cooking_time
    recipe.difficulty = recipe_update.difficulty
    await session.commit()
    return recipe


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    id: int,
):
    recipe = await session.get(Recipe, id)
    await session.delete(recipe)
    await session.commit()