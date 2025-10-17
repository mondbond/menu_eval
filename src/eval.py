import os
import json
from src.metrics.metrics import evaluate_metrics
from src.util import prompt_manager
import matplotlib.pyplot as plt

def draw_bars(list_of_maps, chart_name="eval_chart"):
  n_items = len(list_of_maps)
  bar_width = 0.06
  x = range(n_items)

  bar_values = []
  labels = []
  for item in list_of_maps:

    labels.append(item['label'])
    bar1 = item['size_percent']
    bar2 = item['item_percent']

    bar3 = item['price_percent']
    bar4 = item['volume_percent']
    bar_values.append([bar1, bar2, bar3, bar4])

  bar_values = list(zip(*bar_values))

  plt.figure(figsize=(10, 6))
  plt.bar([i - 1.5*bar_width for i in x], bar_values[0], width=bar_width, color='black', label='size_percent')
  plt.bar([i - 0.5*bar_width for i in x], bar_values[1], width=bar_width, color='red', label='item_percent')
  plt.bar([i + 0.5*bar_width for i in x], bar_values[2], width=bar_width, color='green', label='price_percent')
  plt.bar([i + 1.5*bar_width for i in x], bar_values[3], width=bar_width, color='blue', label='volume_percent')

  plt.xticks(x, labels, rotation=45, ha='right')
  plt.legend()
  plt.tight_layout()
  plt.savefig(f'/Users/ibahr/projects/menu_eval/resources/out/charts/{chart_name}.png')
  plt.show()

def run_item_eval(expected_path, actual_path_list:list):
  expected_json = None
  with open(expected_path, "r", encoding="utf-8") as f:
    expected_json = json.load(f)

  results = []
  for actual_path, label in actual_path_list:
    actual_json = None
    with open(actual_path, "r", encoding="utf-8") as f:
      actual_json = json.load(f)

    print("Evaluating:", actual_path)
    eval_map = evaluate_metrics(expected_json, actual_json)
    eval_map['label'] = label
    results.append(eval_map)
  return results


if __name__ == "__main__":
  # expected = "/Users/ibahr/projects/menu_eval/resources/img/menu/easy/1/expected.json"
  # actuals = [
  #   ("/Users/ibahr/projects/menu_eval/resources/img/menu/easy/1/model_output/anthropic.claude-3-sonnet-20240229-v1:0/base_menu/1/actual.json", "claude-3-sonnet"),
  #   ("/Users/ibahr/projects/menu_eval/resources/img/menu/easy/1/model_output/us.anthropic.claude-3-5-sonnet-20241022-v2:0/base_menu/1/actual.json", "claude-3-5-sonnet"),
  #   ("/Users/ibahr/projects/menu_eval/resources/img/menu/easy/1/model_output/amazon.nova-lite-v1:0/base_menu/1/actual.json", "nova-lite"),
  #   ("/Users/ibahr/projects/menu_eval/resources/img/menu/easy/1/model_output/us.amazon.nova-premier-v1:0/base_menu/1/actual.json", "nova-premier")
  # ]

  # actuals = [
  #   ("/Users/ibahr/projects/menu_eval/resources/img/menu/easy/1/model_output/anthropic.claude-3-sonnet-20240229-v1:0/detailed/1/actual.json", "claude-3-sonnet"),
  #   ("/Users/ibahr/projects/menu_eval/resources/img/menu/easy/1/model_output/us.anthropic.claude-3-5-sonnet-20241022-v2:0/detailed/1/actual.json", "claude-3-5-sonnet"),
  #   ("/Users/ibahr/projects/menu_eval/resources/img/menu/easy/1/model_output/amazon.nova-lite-v1:0/detailed/1/actual.json", "nova-lite"),
  #   ("/Users/ibahr/projects/menu_eval/resources/img/menu/easy/1/model_output/us.amazon.nova-premier-v1:0/detailed/1/actual.json", "nova-premier")
  # ]

  # medium
  # expected = "/Users/ibahr/projects/menu_eval/resources/img/menu/medium/2/expected.json"
  # actuals = [
  #   ("/Users/ibahr/projects/menu_eval/resources/img/menu/medium/2/model_output/anthropic.claude-3-sonnet-20240229-v1:0/base_menu/1/actual.json", "claude-3-sonnet"),
  #   ("/Users/ibahr/projects/menu_eval/resources/img/menu/medium/2/model_output/us.anthropic.claude-3-5-sonnet-20241022-v2:0/base_menu/1/actual.json", "claude-3-5-sonnet"),
  #   ("/Users/ibahr/projects/menu_eval/resources/img/menu/medium/2/model_output/amazon.nova-lite-v1:0/base_menu/1/actual.json", "nova-lite"),
  #   ("/Users/ibahr/projects/menu_eval/resources/img/menu/medium/2/model_output/us.amazon.nova-premier-v1:0/base_menu/1/actual.json", "nova-premier"),
  #
  # ]
  # actuals = [
  #   ("/Users/ibahr/projects/menu_eval/resources/img/menu/medium/2/model_output/anthropic.claude-3-sonnet-20240229-v1:0/detailed/1/actual.json", "claude-3-sonnet"),
  #   ("/Users/ibahr/projects/menu_eval/resources/img/menu/medium/2/model_output/us.anthropic.claude-3-5-sonnet-20241022-v2:0/detailed/1/actual.json", "claude-3-5-sonnet"),
  #   ("/Users/ibahr/projects/menu_eval/resources/img/menu/medium/2/model_output/amazon.nova-lite-v1:0/detailed/1/actual.json", "nova-lite"),
  #   ("/Users/ibahr/projects/menu_eval/resources/img/menu/medium/2/model_output/us.amazon.nova-premier-v1:0/detailed/1/actual.json", "nova-premier"),
  #
  # ]


# hard 1
  expected = "/Users/ibahr/projects/menu_eval/resources/img/menu/hard/2/expected.json"
#   actuals = [
#     ("/Users/ibahr/projects/menu_eval/resources/img/menu/hard/2/model_output/anthropic.claude-3-sonnet-20240229-v1:0/base_menu/1/actual.json", "claude-3-sonnet"),
#      ("/Users/ibahr/projects/menu_eval/resources/img/menu/hard/2/model_output/us.anthropic.claude-3-5-sonnet-20241022-v2:0/base_menu/1/actual.json", "claude-3-5-sonnet"),
#       ("/Users/ibahr/projects/menu_eval/resources/img/menu/hard/2/model_output/amazon.nova-lite-v1:0/base_menu/1/actual.json", "nova-lite"),
#        ("/Users/ibahr/projects/menu_eval/resources/img/menu/hard/2/model_output/us.amazon.nova-premier-v1:0/base_menu/1/actual.json" , "nova-premier")
# ]

  # expected = "/Users/ibahr/projects/menu_eval/resources/img/menu/hard/2/expected.json"
  actuals = [
  ("/Users/ibahr/projects/menu_eval/resources/img/menu/hard/2/model_output/anthropic.claude-3-sonnet-20240229-v1:0/detailed/1/actual.json", "claude-3-sonnet"),
  ("/Users/ibahr/projects/menu_eval/resources/img/menu/hard/2/model_output/us.anthropic.claude-3-5-sonnet-20241022-v2:0/detailed/1/actual.json", "claude-3-5-sonnet"),
  ("/Users/ibahr/projects/menu_eval/resources/img/menu/hard/2/model_output/amazon.nova-lite-v1:0/detailed/1/actual.json", "nova-lite"),
  ("/Users/ibahr/projects/menu_eval/resources/img/menu/hard/2/model_output/us.amazon.nova-premier-v1:0/detailed/1/actual.json" , "nova-premier")
  ]

  draw_bars(run_item_eval(expected, actuals), 'hard_case_detailed_prompt.png')
