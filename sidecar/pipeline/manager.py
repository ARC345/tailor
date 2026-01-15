from typing import Dict, Any, List, Optional, Callable, Awaitable
import asyncio
from loguru import logger

from .types import PipelineContext
from .events import PipelineEvents

EventHandler = Callable[[PipelineContext], Awaitable[None]]

class PipelineManager:
    """
    Central Orchestrator for Pipeline Events.
    Delegates actual event handling to VaultBrain (Sequential Mode).
    """
    
    def __init__(self):
        self._logger = logger.bind(component="PipelineManager")

    @property
    def brain(self):
        from ..vault_brain import VaultBrain
        return VaultBrain.get()

    def subscribe(self, event: str, handler: EventHandler) -> None:
        """Register an async event handler via VaultBrain."""
        self.brain.subscribe(event, handler)
        self._logger.debug(f"Registered handler for {event} (via VaultBrain)")

    async def emit(self, event: str, ctx: PipelineContext) -> None:
        """
        Emit a pipeline event sequentially.
        """
        if ctx.should_abort:
            return

        ctx.events_emitted.append(event)

        # Publish sequentially using VaultBrain
        # This will call all handlers: handler(ctx=ctx)
        # Note: Handlers must accept **kwargs, so 'ctx' will be passed as a kwarg.
        await self.brain.publish(event, sequential=True, ctx=ctx)
        
        if ctx.should_abort:
            self._logger.info(f"Pipeline aborted during {event}: {ctx.abort_reason}")

