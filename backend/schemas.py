from pydantic import BaseModel, ConfigDict, Field

class PostBase(BaseModel):
    pass

class PostRequest(PostBase):
    query: str = Field(min_length=1, max_length=50)
    hero: str | None = None

class SearchResult(BaseModel):
    hero: str
    ID: str
    line: str
    score: float
    audio_url: str | None

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    
    results: list[SearchResult] 

