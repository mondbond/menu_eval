import matplotlib.pyplot as plt

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

def plot_model_pricing_comparison(pricing_map, input_tokens=2000, output_tokens=800, request_count=1000):
    models = list(pricing_map.keys())
    avg_prices = []
    batch_prices = []
    for model in models:
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
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("/Users/ibahr/projects/menu_eval/resources/out/charts/pricing_charts/model_pricing_comparison.png")
    plt.show()


if __name__ == "__main__":
  typical_image = {
    "input_tokens": 2052,
    "output_tokens": 790
  }

  typical_image = {
    "input_tokens": 2155,
    "output_tokens": 1031
  }

  calculate_for_count_of_requests = 1000
  model = "amazon-nova-lite"
  model = "claude-3.5-sonnet"
  # model = "amazon-premier"


  print(f"Price for {model} : {calculate_for_count_of_requests} requests with typical image: {calculate_price(typical_image['input_tokens'], typical_image['output_tokens'], pricing_map[model]['input_pricing'], pricing_map[model]['output_pricing'], calculate_for_count_of_requests)} USD")
  print(f"Batch price for {model} : {calculate_for_count_of_requests} requests with typical image: {calculate_price(typical_image['input_tokens'], typical_image['output_tokens'], pricing_map[model]['input_batch_pricing'], pricing_map[model]['output_batch_pricing'], calculate_for_count_of_requests)} USD")

  plot_model_pricing_comparison(pricing_map, typical_image['input_tokens'], typical_image['output_tokens'], calculate_for_count_of_requests)
