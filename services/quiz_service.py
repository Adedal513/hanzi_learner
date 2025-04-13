from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from sqlalchemy import select, func
from models.hanzi import Hanzi
import random

class QuizService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def get_random_hanzi(self) -> Hanzi:
        async with self.db as session:
            result = await session.execute(
                select(Hanzi).order_by(func.random()).limit(1)
            )
        return result.scalars().first()
    
    async def get_random_meanings(self, count: int, exclude: str) -> List[str]:
        # TODO: Rewrite this bit to make options less DB costly.
        result = await self.db.execute(
            text("SELECT meaning FROM hanzi WHERE meaning != :exclude ORDER BY RANDOM() LIMIT :count"),
            {"exclude": exclude, "count": count}
        )
        return [row[0] for row in result.all()]

    async def generate_quiz(self, options_count: int = 4) -> Dict:
        hanzi = await self.get_random_hanzi()
        wrong = await self.get_random_meanings(
            count=options_count - 1,
            exclude=hanzi.meaning
        )

        # n - 1 wrong options + 1 correct option 
        options = wrong + [hanzi.meaning]
        random.shuffle(options)
        
        return {
            'character': hanzi.character,
            'image_key': hanzi.s3_image_key,
            'options': options,
            'correct_answer': hanzi.meaning,
        }
