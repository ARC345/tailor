import pytest
import asyncio
import json
import shutil
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock

from sidecar.vault_brain import VaultBrain
from sidecar.services.llm_service import LLMService

@pytest.mark.asyncio
async def test_memory_branching():
    # Setup paths
    vault_path = Path("/home/arc/Dev/tailor/example-vault")
    memory_dir = vault_path / ".memory"
    chat_id = "chat_branch_test"
    memory_file = memory_dir / f"{chat_id}.json"
    
    # Clean up
    if memory_dir.exists():
        shutil.rmtree(memory_dir)
        
    # Reset Singleton
    if VaultBrain._instance:
        VaultBrain._instance = None
    
    # Initialize
    brain = VaultBrain(vault_path, MagicMock())
    
    # Mock LLM
    mock_llm = MagicMock(spec=LLMService)
    mock_llm.complete = AsyncMock()
    # Responses:
    # 1. Main branch response
    # 2. Side branch response
    mock_llm.complete.side_effect = [
        MagicMock(content="Response 1", model="test", usage={}),
        MagicMock(content="Response 2", model="test", usage={})
    ]
    
    await brain.initialize()
    brain._llm_service = mock_llm
    import sidecar.services.llm_service as llm_module
    llm_module._llm_service = mock_llm
    
    # 1. Start Chat (Main Branch)
    # User: Msg 1 -> Assistant: Response 1
    await brain.chat_send(message="Msg 1", chat_id=chat_id)
    
    # Verify file
    with open(memory_file, "r") as f:
        data = json.load(f)
    assert data["active_branch"] == "main"
    assert len(data["branches"]["main"]) == 2
    
    # 2. Create Branch from index 0 (User Msg 1)
    # Note: History index 0 is User Msg 1. Index 1 is Response 1.
    # If we branch from 0, we keep Msg 1. We drop Response 1?
    # Logic in code: new_history = current_history[:message_index+1]
    # If index=0, we keep item 0.
    result = await brain.execute_command("memory.create_branch", 
        chat_id=chat_id, 
        message_index=0, 
        name="experiment_a"
    )
    
    assert result["status"] == "success"
    assert result["branch"] == "experiment_a"
    assert len(result["history"]) == 1
    assert result["history"][0]["content"] == "Msg 1"
    
    # Verify file updated
    with open(memory_file, "r") as f:
        data = json.load(f)
    assert data["active_branch"] == "experiment_a"
    assert "experiment_a" in data["branches"]
    assert len(data["branches"]["experiment_a"]) == 1
    
    # 3. Continue Chat on New Branch
    # User sends Msg 2 (which is arguably redundant context wise if we are just testing storage, but pipeline will run)
    # Actually, if we are in a branch, next chat_send should append to it.
    await brain.chat_send(message="Msg 2", chat_id=chat_id)
    
    # Verify file
    with open(memory_file, "r") as f:
        data = json.load(f)
        
    branch_hist = data["branches"]["experiment_a"]
    # Should have: Msg 1, Msg 2, Response 2
    assert len(branch_hist) == 3
    assert branch_hist[0]["content"] == "Msg 1"
    assert branch_hist[1]["content"] == "Msg 2"
    assert branch_hist[2]["content"] == "Response 2"
    
    # Verify Main Branch Unchanged
    main_hist = data["branches"]["main"]
    assert len(main_hist) == 2
    assert main_hist[1]["content"] == "Response 1"
    
    # Cleanup
    await brain.shutdown()
    if memory_dir.exists():
        shutil.rmtree(memory_dir)
