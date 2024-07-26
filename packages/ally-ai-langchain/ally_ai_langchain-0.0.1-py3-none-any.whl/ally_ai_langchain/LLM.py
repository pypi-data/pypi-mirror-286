from langchain_openai import AzureChatOpenAI
from typing import Optional, Union
from pydantic import BaseModel
from ally_ai_core import Settings

class LLM(AzureChatOpenAI):
    """
    Interited from AzureChatOpenAI Model
    """
    settings: Settings = None
    
    def __init__(self, settings: Optional[Settings] = None, **kwargs) -> None:
        
        if settings is None:
            settings = Settings(section='llm')

        settings['azure_endpoint'] = settings.pop('endpoint')
        settings['azure_deployment'] = settings.pop('deployment_name')

        super().__init__(**settings, **kwargs)
        
        self.settings = settings

    def __call__(self, schema: Union[dict, BaseModel, None] = None) -> AzureChatOpenAI:
        """ 
        Returns llm model
        """
        if schema:
            return self.with_structured_output(schema=schema)

        return self
