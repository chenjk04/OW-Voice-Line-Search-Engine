from pydantic import BaseModel, ConfigDict, Field

class PostBase(BaseModel):
    pass

class PostRequest(PostBase):
    query: str = Field(min_length=1, max_length=50)

class SearchResult(BaseModel):
    hero: str
    id: str
    line: str
    score: float
    audio_url: str

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    
    results: list[SearchResult] 

