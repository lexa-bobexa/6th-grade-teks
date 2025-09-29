from fastapi import FastAPI
from .routers import health, items, attempts, progress
from services.mastery import MasteryService
from services.curriculum import CurriculumService
from services.item_factory import ItemFactory

app = FastAPI(title="TEKS Grade 6 Tutor API", version="0.1.0")

# Initialize services
mastery_service = MasteryService()
curriculum_service = CurriculumService(mastery_service)
item_factory = ItemFactory()

# Make services available to routers
app.state.mastery_service = mastery_service
app.state.curriculum_service = curriculum_service
app.state.item_factory = item_factory

# Routers
app.include_router(health.router)
app.include_router(items.router)
app.include_router(attempts.router)
app.include_router(progress.router)


@app.get("/")
def root():
    return {"ok": True, "service": "teks-grade6-tutor"}
