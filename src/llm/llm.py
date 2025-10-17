import base64

import os
from typing import Optional

import boto3
from langchain_aws import ChatBedrockConverse
from pydantic import BaseModel, Field
from typing import List
from src.util.prompt_manager import prompt_manager


# Defining unified structural output
class DrinkItem(BaseModel):
  item: str = Field(description="Name of the drink. Can be only string.")
  price: Optional[float] = Field(description="Price of the drink. Can be only float number or null.")
  volume: Optional[float] = Field(description="Can be only float number or null. It means volume of the drink, e.g., 0.5.")

class DrinkItems(BaseModel):
  drinks: List[DrinkItem] = Field(description="List of drink items in the menu")

# unified function to get Bedrock LLM client
def get_bedrock_llm_model_client(bedrock_model_id, output_model, temperature):
  session = boto3.Session(profile_name="default", region_name="us-east-1")
  credentials = session.get_credentials().get_frozen_credentials()
  aws_access_key_id = credentials.access_key
  aws_secret_access_key = credentials.secret_key
  aws_session_token = credentials.token  # can be None if not using
  llm = (ChatBedrockConverse(
      model_id=bedrock_model_id,
      region_name="us-east-1",
      aws_access_key_id=aws_access_key_id,
      aws_secret_access_key=aws_secret_access_key,
      aws_session_token=aws_session_token,  # optional
      temperature=temperature)).with_structured_output(output_model)

  return llm

# call Bedrock model to detect menu items
def call_bedrock_detect_menu(image_path, bedrock_mpdel_id=None, output_model=None, temperature=0, prompt_name=None):
  with open(image_path, "rb") as f:
    image_bytes = f.read()

  image_base64 = base64.b64encode(image_bytes).decode("utf-8")

  llm = get_bedrock_llm_model_client(bedrock_mpdel_id, output_model, temperature)

  prompt = prompt_manager.get_prompt(prompt_name)
  prompt_lasr_version = prompt_manager.get_prompt_last_version(prompt_name)

  system_message = {
    "role": "system",
    "content": [
      {
        "type": "text",
        "text": prompt,
      },
    ],
  }
  user_message = {
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": "IMAGE:",
      },
      {
        "type": "image",
        "source_type": "base64",
        "data": image_base64,
        "mime_type": "image/jpeg",
      },
    ],
  }

  results = llm.invoke([system_message, user_message])

  json_output = results.model_dump_json(indent=2)

  parent_dir = os.path.dirname(image_path)
  new_subfolder = os.path.join(parent_dir, 'model_output', bedrock_mpdel_id, str(prompt_name), str(prompt_lasr_version))
  new_file_path = os.path.join(new_subfolder, 'actual.json')
  os.makedirs(new_subfolder, exist_ok=True)
  with open(new_file_path, 'w', encoding='utf-8') as f:
    f.write(json_output)

  print(json_output)


if __name__ == "__main__":
  image_path = '/Users/ibahr/projects/menu_eval/resources/img/menu/medium/2/image.jpg'
  available_models = [
    "anthropic.claude-3-sonnet-20240229-v1:0",
    "us.anthropic.claude-3-5-sonnet-20241022-v2:0",

    "amazon.nova-lite-v1:0",
    "us.amazon.nova-premier-v1:0",
  ]

  for model in available_models:
    call_bedrock_detect_menu(
        image_path,
        model,
        DrinkItems,
        temperature=0,
        prompt_name='detailed')
