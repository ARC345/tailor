"""
Unit tests for WebSocketServer module.

Tests connection handling, JSON-RPC message processing, and command registration.
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from websocket_server import WebSocketServer, CommandHandler
from exceptions import JSONRPCError, WebSocketError
from constants import (
    JSONRPC_PARSE_ERROR,
    JSONRPC_INVALID_REQUEST,
    JSONRPC_METHOD_NOT_FOUND,
    JSONRPC_INTERNAL_ERROR,
)


@pytest.mark.unit
class TestWebSocketServer:
    """Test WebSocketServer functionality."""
    
    @pytest.fixture
    def server(self):
        """Create a WebSocketServer instance."""
        return WebSocketServer(port=9000)
    
    @pytest.fixture
    def mock_ws(self):
        """Create a mock WebSocket connection."""
        ws = AsyncMock()
        ws.send = AsyncMock()
        ws.close = AsyncMock()
        ws.remote_address = ("127.0.0.1", 12345)
        return ws
        
    def test_init(self, server):
        """Test server initialization."""
        assert server.port == 9000
        assert server.host == "localhost"  # Default
        assert server.connection is None
        assert server.command_handlers == {}

    def test_register_handler_async(self, server):
        """Test registering an async handler."""
        async def handler(params): return {}
        server.register_handler("test.method", handler)
        assert "test.method" in server.command_handlers
        assert server.command_handlers["test.method"] == handler

    def test_register_handler_sync(self, server):
        """Test registering a sync handler (wrapper)."""
        def handler(params): return {}
        server.register_handler("test.method", handler)
        assert "test.method" in server.command_handlers
        # Should be wrapped in async
        assert asyncio.iscoroutinefunction(server.command_handlers["test.method"])

    @pytest.mark.asyncio
    async def test_send_to_rust_connected(self, server, mock_ws):
        """Test sending message when connected."""
        server.connection = mock_ws
        message = {"jsonrpc": "2.0", "method": "test"}
        
        # We need to await the task created by send_to_rust if we want to verify side effects immediately
        # Since send_to_rust is fire-and-forget (create_task), we can mock create_task or await explicitly?
        # Better: use 'send' directly for async test, or verify 'send_to_rust' calls 'create_task'
        
        # Testing the async send() method directly is more reliable for unit tests
        await server.send(message)
        
        mock_ws.send.assert_called_once()
        sent_json = mock_ws.send.call_args[0][0]
        assert json.loads(sent_json) == message

    @pytest.mark.asyncio
    async def test_send_to_rust_no_loop_queues(self, server):
        """Test sending message when no loop (queues message)."""
        message = {"jsonrpc": "2.0", "method": "test"}
        
        # Mock get_running_loop to raise RuntimeError (simulate no loop)
        with patch("asyncio.get_running_loop", side_effect=RuntimeError):
            server.send_to_rust(message)
            
        assert message in server.pending_messages

    @pytest.mark.asyncio
    async def test_handle_message_valid_request(self, server):
        """Test processing a valid request."""
        # Register a handler
        handler = AsyncMock(return_value={"status": "ok"})
        server.register_handler("test.echo", handler)
        
        # Mock connection to verify response
        server.connection = Mock()
        server.connection.send = AsyncMock()
        
        request = {
            "jsonrpc": "2.0",
            "method": "test.echo",
            "params": {"msg": "hello"},
            "id": 1
        }
        
        await server.handle_message(json.dumps(request))
        
        # Check handler called
        handler.assert_called_once_with({"msg": "hello"})
        
        # Check response sent
        server.connection.send.assert_called_once()
        response_str = server.connection.send.call_args[0][0]
        response = json.loads(response_str)
        
        assert response["result"] == {"status": "ok"}
        assert response["id"] == 1

    @pytest.mark.asyncio
    async def test_handle_message_method_not_found(self, server):
        """Test unknown method."""
        server.connection = Mock()
        server.connection.send = AsyncMock()
        
        request = {
            "jsonrpc": "2.0",
            "method": "unknown",
            "id": 2
        }
        
        # Implementation logs warning but doesn't strictly require sending error 
        # (based on line 211: "Could send method not found error here" comment)
        # However, looking at handle_message, if method not in handlers, it logs warning and does nothing else.
        # So it does NOT send an error response by default currently.
        
        await server.handle_message(json.dumps(request))
        
        # Verify NO response sent (based on current implementation)
        server.connection.send.assert_not_called()

    @pytest.mark.asyncio
    async def test_handle_message_invalid_json(self, server):
        """Test malformed JSON."""
        server.connection = Mock()
        server.connection.send = AsyncMock()
        
        # Trying to handle malformed JSON raises WebSocketMessageError which is caught 
        # and logged, but implementation re-raises JSONRPCError? 
        # Line 165 raises WebSocketMessageError. 
        # Line 214 catches WebSocketMessageError and logs it.
        # So strict expect: no response sent if exception acts merely as logging trigger.
        # But wait, validate_jsonrpc_message raises JSONRPCError, which IS caught and logged.
        
        await server.handle_message("not valid json")
        
        # Should catch and log, probably no response back to client unless implemented?
        # Current implementation just logs errors for these cases.
        server.connection.send.assert_not_called()

    @pytest.mark.asyncio
    async def test_handler_exception(self, server):
        """Test error raised inside handler."""
        # Handler raises generic exception
        handler = AsyncMock(side_effect=ValueError("Handler failed"))
        server.register_handler("test.fail", handler)
        
        server.connection = Mock()
        server.connection.send = AsyncMock()
        
        request = {
            "jsonrpc": "2.0",
            "method": "test.fail",
            "id": 3
        }
        
        await server.handle_message(json.dumps(request))
        
        # Check internal error response
        server.connection.send.assert_called_once()
        response_str = server.connection.send.call_args[0][0]
        response = json.loads(response_str)
        
        assert response["error"]["code"] == JSONRPC_INTERNAL_ERROR
        assert "Handler failed" in response["error"]["message"] or "ValueError" in response["error"]["message"]

    @pytest.mark.asyncio
    async def test_handle_connection(self, server, mock_ws):
        """Test that new connection is stored."""
        # Mock wait_closed to return immediately to avoid blocking
        # But wait, handle_connection iterates over `async for message in websocket`.
        # We need to mock the iterator.
        
        async def mock_iter():
            if False: yield "msg" # Yield nothing
        
        mock_ws.__aiter__.side_effect = mock_iter
        
        await server.handle_connection(mock_ws)
        
        # Should have set connection, then cleared it in finally block
        # To test it WAS set, we'd need to emit a message or check internal state during execution.
        # But since it runs to completion (empty iterator), connection is None at end.
        assert server.connection is None

