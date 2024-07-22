import pytest
from ai_function_helper import AIFunctionHelper
from pydantic import BaseModel

# Mock API key and base URL for testing
API_KEY = "test_api_key"
class TestResponseModel(BaseModel):
    result: str

@pytest.fixture
def ai_helper():
    return AIFunctionHelper(API_KEY)

@pytest.mark.asyncio
async def test_ai_function_decorator(ai_helper):
    @ai_helper.ai_function(model="test-model")
    async def test_function(ai_result: TestResponseModel, input_data: str) -> TestResponseModel:
        """Test function"""
        return ai_result

    # Mock the call_ai_function method
    ai_helper.call_ai_function = lambda options: {"result": "Test result"}

    result = await test_function(input_data="Test input")
    assert isinstance(result, TestResponseModel)
    assert result.result == "Test result"

# Add more tests for other methods and functionalities