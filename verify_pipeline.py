import asyncio
import sys
from loguru import logger

sys.path.append("/home/arc/Dev/tailor")

from sidecar.pipeline import PipelineManager, DefaultPipeline, PipelineConfig, PipelineEvents, PipelineContext

async def test_pipeline():
    logger.info("Initializing Pipeline (LangGraph powered)...")
    manager = PipelineManager()
    config = PipelineConfig(model="gpt-3.5-turbo", api_key="test-key")
    pipeline = DefaultPipeline(manager, config)
    
    # Register a test hook
    async def log_input(ctx: PipelineContext):
        print(f"[Hook] Input received: {ctx.message}")
        ctx.add_metadata("test_hook_ran", True)
        # Verify Pydantic validation handles this assignment
        
    manager.subscribe(PipelineEvents.INPUT, log_input)
    
    logger.info("Running Pipeline...")
    # This will use placeholder since we don't have real OpenAI key configured/mocked here
    ctx = await pipeline.run("Hello world")
    
    print(f"Response: {ctx.response}")
    print(f"Events Emitted: {ctx.events_emitted}")
    print(f"Metadata: {ctx.metadata}")
    
    assert ctx.response is not None
    assert "test_hook_ran" in ctx.metadata, "Hook did not modify metadata"
    assert PipelineEvents.INPUT in ctx.events_emitted
    assert PipelineEvents.OUTPUT in ctx.events_emitted
    
    logger.success("Verification Successful!")

if __name__ == "__main__":
    asyncio.run(test_pipeline())
