import base64
import json
import time

import os
from typing import Optional

import boto3
from langchain_aws import ChatBedrockConverse
from pydantic import BaseModel, Field
from typing import List
from src.util.prompt_manager import prompt_manager


# Defining unified structural output
class DrinkItem(BaseModel):
  item: Optional[str] = Field(description="Name of the drink. Can be only string.")
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


def get_bedrock_llm_model_client_raw(bedrock_model_id, output_model, temperature):
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
      temperature=temperature)).with_structured_output(output_model, include_raw=True)

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


def call_bedrock_record_tokens_usage(bedrock_mpdel_id=None, output_model=None, temperature=0, prompt_name=None):
  img_dir_path = '/Users/ibahr/projects/menu_eval/resources/img/menu/price_evaluation/img'

  file_paths = [ os.path.join(img_dir_path, f) for f in os.listdir(img_dir_path) if os.path.isfile(os.path.join(img_dir_path, f))]

  for image_path in file_paths:
    # time.sleep(5)
    try:
      with open(image_path, "rb") as f:
        image_bytes = f.read()

      image_base64 = base64.b64encode(image_bytes).decode("utf-8")

      llm = get_bedrock_llm_model_client_raw(bedrock_mpdel_id, output_model, temperature)

      prompt = prompt_manager.get_prompt(prompt_name)

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

      response = llm.invoke([system_message, user_message])

      latency = response['raw'].response_metadata['metrics']['latencyMs'][0]
      input_token = response['raw'].usage_metadata['input_tokens']
      output_token = response['raw'].usage_metadata['output_tokens']

      token_data = {'latency': latency, 'input_token': input_token, 'output_token': output_token}

      results = response['parsed']

      json_output = results.model_dump_json(indent=2)

      parent_dir = os.path.dirname(os.path.dirname(image_path))
      file_name = os.path.splitext(os.path.basename(image_path))[0]


      new_subfolder = os.path.join(parent_dir, 'model_output', bedrock_mpdel_id, 'actual')
      new_file_path = os.path.join(new_subfolder, file_name + '.json')
      os.makedirs(new_subfolder, exist_ok=True)
      with open(new_file_path, 'w', encoding='utf-8') as f:
        f.write(json_output)

      new_subfolder = os.path.join(parent_dir, 'model_output', bedrock_mpdel_id, 'tokens')
      new_file_path = os.path.join(new_subfolder, file_name + '.json')
      os.makedirs(new_subfolder, exist_ok=True)
      with open(new_file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(token_data))

      print(json_output)
    except Exception as e:
      print(f"Error processing {image_path}: {e}")
      continue


def call_for_quality_evaluation():
  # image_path = '/Users/ibahr/projects/menu_eval/resources/img/menu/medium/2/image.jpg'
  image_path = '/Users/ibahr/projects/menu_eval/resources/img/menu/hard/2/image.jpeg'
  available_models = [
    "anthropic.claude-3-sonnet-20240229-v1:0",
    # "us.anthropic.claude-3-5-sonnet-20241022-v2:0",

    "amazon.nova-lite-v1:0",
    "us.amazon.nova-premier-v1:0",

    # "us.meta.llama4-maverick-17b-instruct-v1:0",
    # "us.anthropic.claude-opus-4-1-20250805-v1:0",
  ]

  for model in available_models:
    call_bedrock_detect_menu(
        image_path,
        model,
        DrinkItems,
        temperature=0,
        prompt_name='detailed_polished')
  pass


def token_usage_evaluation():
  available_models = [
    "anthropic.claude-3-sonnet-20240229-v1:0",
    # "us.anthropic.claude-3-5-sonnet-20241022-v2:0",

    # "amazon.nova-lite-v1:0",
    # "us.amazon.nova-premier-v1:0",

    # "us.meta.llama4-maverick-17b-instruct-v1:0",
    # "us.anthropic.claude-opus-4-1-20250805-v1:0",
  ]

  for model in available_models:
    call_bedrock_record_tokens_usage(
        model,
        DrinkItems,
        temperature=0,
        prompt_name='detailed')



if __name__ == "__main__":
  # call_for_quality_evaluation()
  token_usage_evaluation()
