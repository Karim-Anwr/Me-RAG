from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnum import DataBaseEnum 
from bson.objectid import ObjectId
from pymongo import InsertOne


class ChunkModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[
            DataBaseEnum.DATA_CHUNKS_COLLECTION.value
        ]

    async def create_chunk(self, chunk: DataChunk):

        chunk_dict = chunk.dict(by_alias=True, exclude_unset=True)

        result = await self.collection.insert_one(chunk_dict)

        chunk.id = str(result.inserted_id)
        return chunk

    async def get_chunks(self, chunk_id: str):

        cursor = self.collection.find({
            "_id": ObjectId(chunk_id)
        })

        chunks = [DataChunk(**doc) async for doc in cursor]
        return chunks

    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]

            batch_dicts = [
                chunk.dict(by_alias=True, exclude_unset=True)
                for chunk in batch
            ]

            await self.collection.insert_many(batch_dicts)

        return len(chunks)