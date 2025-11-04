import matplotlib.pyplot as plt
import os
import json
from glob import glob

from src.eval import draw_bars

pricing_map = {
  "claude-3-sonnet": {
    "input_pricing": 0.003,
    "output_pricing": 0.015,
    "input_batch_pricing": 0.0015,
    "output_batch_pricing": 0.0075,
  },
  "claude-3.5-sonnet": {
    "input_pricing": 0.003,
    "output_pricing": 0.015,
    "input_batch_pricing": 0.0015,
    "output_batch_pricing": 0.0075,
  },
  "amazon-nova-lite": {
    "input_pricing": 0.00006,
    "output_pricing": 0.00024,
    "input_batch_pricing": 0.00003,
    "output_batch_pricing": 0.00012,
  },
  "amazon-premier": {
    "input_pricing": 0.0025,
    "output_pricing": 0.0125,
    "input_batch_pricing": 0.00125,
    "output_batch_pricing": 0.00625,
  },
}


def calculate_price(input_tokens: int, output_tokens: int, input_pricing:float, output_pricing: float, request_count = 1000):
    total_input_cost = (input_pricing / 1000) * input_tokens * request_count
    total_output_cost = (output_pricing / 1000) * output_tokens * request_count
    total_cost = total_input_cost + total_output_cost
    return total_cost

def plot_model_pricing_comparison(pricing_map, request_count=1000):
    models = list(pricing_map.keys())
    avg_prices = []
    batch_prices = []
    for model in models:
      if model == "claude-3.5-sonnet" or model == "claude-3-sonnet":
        input_tokens = 3000
        output_tokens = 1000
      elif model == "amazon-nova-lite" or model == "amazon-premier":
        input_tokens = 3500
        output_tokens = 1150


      p = pricing_map[model]
      avg_price = calculate_price(
          input_tokens, output_tokens, p["input_pricing"], p["output_pricing"], request_count
      )
      batch_price = calculate_price(
          input_tokens, output_tokens, p["input_batch_pricing"], p["output_batch_pricing"], request_count
      )
      avg_prices.append(avg_price)
      batch_prices.append(batch_price)

    x = range(len(models))
    bar_width = 0.35
    plt.figure(figsize=(10, 6))
    plt.bar([i - bar_width/2 for i in x], avg_prices, width=bar_width, label='Average Pricing')
    plt.bar([i + bar_width/2 for i in x], batch_prices, width=bar_width, label='Batch Pricing')
    plt.xticks(x, models, rotation=30, ha='right')
    plt.ylabel('Total Price ($)')
    plt.title('Model Pricing Comparison (Average vs Batch)')
    plt.legend()
    plt.grid()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("/Users/ibahr/projects/menu_eval/resources/out/charts/pricing_charts/model_pricing_comparison.png")
    plt.show()


def print_model_token_latency_stats():
    base_path = "/Users/ibahr/projects/menu_eval/resources/img/menu/price_evaluation/model_output"
    model_dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

    overall_latency = []
    overall_input_tokens = []
    overall_output_tokens = []

    for model in model_dirs:
        token_dir = os.path.join(base_path, model, "tokens")
        if not os.path.isdir(token_dir):
            continue
        json_files = glob(os.path.join(token_dir, "*.json"))
        latencies = []
        input_tokens = []
        output_tokens = []
        for jf in json_files:
            try:
                with open(jf, "r") as f:
                    data = json.load(f)
                latencies.append(data.get("latency", 0))
                input_tokens.append(data.get("input_token", 0))
                output_tokens.append(data.get("output_token", 0))
            except Exception as e:
                print(f"Error reading {jf}: {e}")
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            avg_input = sum(input_tokens) / len(input_tokens)
            avg_output = sum(output_tokens) / len(output_tokens)
            print(f"Model: {model}")
            print(f"  Avg Latency: {avg_latency:.2f} ms")
            print(f"  Avg Input Tokens: {avg_input:.2f}")
            print(f"  Avg Output Tokens: {avg_output:.2f}")
            overall_latency.extend(latencies)
            overall_input_tokens.extend(input_tokens)
            overall_output_tokens.extend(output_tokens)
        else:
            print(f"Model: {model} (no data)")
    if overall_latency:
        print("\nOverall Averages:")
        print(f"  Avg Latency: {sum(overall_latency)/len(overall_latency):.2f} ms")
        print(f"  Avg Input Tokens: {sum(overall_input_tokens)/len(overall_input_tokens):.2f}")
        print(f"  Avg Output Tokens: {sum(overall_output_tokens)/len(overall_output_tokens):.2f}")
    else:
        print("No data found for any model.")



def calculate_price_chart():
  typical_image_aws = {
    "input_tokens": 3100,
    "output_tokens": 1150
  }

  typical_image_sonet = {
    "input_tokens": 2600,
    "output_tokens": 1031
  }

  calculate_for_count_of_requests = 1000
  model = "amazon-nova-lite"
  model = "claude-3.5-sonnet"


  # print(f"Price for {model} : {calculate_for_count_of_requests} requests with typical image: {calculate_price(typical_image['input_tokens'], typical_image['output_tokens'], pricing_map[model]['input_pricing'], pricing_map[model]['output_pricing'], calculate_for_count_of_requests)} USD")

  model = "amazon-premier"
  # print(f"Batch price for {model} : {calculate_for_count_of_requests} requests with typical image: {calculate_price(typical_image['input_tokens'], typical_image['output_tokens'], pricing_map[model]['input_batch_pricing'], pricing_map[model]['output_batch_pricing'], calculate_for_count_of_requests)} USD")

  # plot_model_pricing_comparison(pricing_map, typical_image['input_tokens'], typical_image['output_tokens'], calculate_for_count_of_requests)
  # print_model_token_latency_stats()

  plot_model_pricing_comparison(pricing_map, calculate_for_count_of_requests)
if __name__ == "__main__":
  # print_model_token_latency_stats()
  calculate_price_chart()

