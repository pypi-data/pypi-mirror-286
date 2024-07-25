import json
import re
from typing import List, Union, TypeVar, Type, Dict
from agentifyme.ml.llm.base import LLMCacheType, LLMModel
from pydantic import BaseModel
from agentifyme.tools import Tool
from agentifyme.ml.llm.openai import OpenAILLM

T = TypeVar("T")


class StructuredDataExtractorTask:
    """Task for extracting structured data from unstructured data."""

    validate_output: bool

    def __init__(
        self,
        objective: str,
        instructions: str,
        tools: List[Tool],
        llm: str,
        validate_output: bool = False,
    ) -> None:
        self.objective = objective
        self.instructions = instructions
        self.tools = tools
        self.llm = llm
        self.validate_output = validate_output

    def __call__(
        self, task_input: Union[str, BaseModel], task_output_type: Type[T]
    ) -> T:
        return self.run(task_input, task_output_type)

    def parse_json_string(self, json_blob: str) -> Dict[str, str]:
        try:
            first_accolade_index = json_blob.find("{")
            last_accolade_index = [
                a.start() for a in list(re.finditer("}", json_blob))
            ][-1]
            json_blob = json_blob[
                first_accolade_index : last_accolade_index + 1
            ].replace('\\"', "'")
            json_data = json.loads(json_blob, strict=False)
            return json_data
        except json.JSONDecodeError as e:
            place = e.pos
            if json_blob[place - 1 : place + 2] == "},\n":
                raise ValueError(
                    "JSON is invalid: you probably tried to provide multiple tool calls in one action. PROVIDE ONLY ONE TOOL CALL."
                )
            raise ValueError(
                f"The JSON blob you used is invalid due to the following error: {e}.\n"
                f"JSON blob was: {json_blob}, decoding failed on that specific part of the blob:\n"
                f"'{json_blob[place-4:place+5]}'."
            )
        except Exception as e:
            raise ValueError(f"Error in parsing the JSON blob: {e}")

    def run(self, task_input: Union[str, BaseModel], task_output_type: Type[T]) -> T:
        # Extract structured data from the unstructured data

        task_output_type_data_definition = ""
        if issubclass(task_output_type, BaseModel):
            json_schema = task_output_type.model_json_schema()
            task_output_type_data_definition = json.dumps(json_schema, indent=2)

        prompt = f"""
        
        # Objective 
        Extract the key skills, experiences, and qualifications from the job posting.
        
        # Instructions
        Understand the data definition below, parse the objects from the provided text, and return the structured data in the JSON format.

        # Data Definition
        {task_output_type_data_definition}

        # Provided Text
        {task_input}

        Strictly extract the data provided in the data definition.
        """

        # Call the LLM to extract the structured dataec
        _llm = OpenAILLM(
            llm_model=LLMModel.OPENAI_GPT4o,
            api_key="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",
            llm_cache_type=LLMCacheType.NONE,
        )
        response = _llm.generate_from_prompt(prompt)

        # Validate the output
        if response.message is not None:
            data = self.parse_json_string(response.message)
            return task_output_type(**data)

        return task_output_type()
