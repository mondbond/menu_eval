def evaluate_metrics(expected_json, llm_json):
    size_percentage = (len(llm_json) / len(expected_json) * 100) if len(expected_json) > 0 else 0
    item_matched = 0
    price_matched = 0
    volume_matched = 0
    total_matched = 0

    expected_json = expected_json['drinks']
    llm_json = llm_json['drinks']

    for expected_item in expected_json:
        test_name = str(expected_item.get('item', '')).lower()
        expected_price = expected_item.get('price', None)
        expected_volume = expected_item.get('volume', None)

        candidates = [llm_item for llm_item in llm_json if test_name in str(llm_item.get('item', '')).lower()]
        if expected_price is not None and candidates:
            price_candidates = [c for c in candidates if c.get('price') is not None and abs(c.get('price') - expected_price) < 0.1]
            if price_candidates:
                candidates = price_candidates

        if expected_volume is not None and candidates:
            volume_candidates = [c for c in candidates if c.get('volume') is not None and abs(c.get('volume') - expected_volume) < 0.01]
            if volume_candidates:
                candidates = volume_candidates
        found = candidates[0] if candidates else None

        if found:
            item_matched += 1
            total_matched += 1
            found_price = found.get('price', None)
            if expected_price is None and found_price is None:
                price_matched += 1
            elif expected_price is not None and found_price is not None and abs(expected_price - found_price) < 0.1:
                price_matched += 1
            else:
              print("price mismatch:", test_name, "expected:", expected_price, "found:", found_price)
            found_volume = found.get('volume', None)
            if expected_volume is None and found_volume is None:
                volume_matched += 1
            elif expected_volume is not None and found_volume is not None and abs(expected_volume - found_volume) < 0.01:
                volume_matched += 1
            else:
              print("volume mismatch:", test_name, "expected:", expected_volume, "found:", found_volume)
        else:
            print("item missing:", test_name, "expected price:", expected_price, "expected volume:", expected_volume)


    item_percentage = (item_matched / len(expected_json) * 100) if len(expected_json) > 0 else 0
    price_percentage = (price_matched / total_matched * 100) if total_matched > 0 else 0
    volume_percentage = (volume_matched / total_matched * 100) if total_matched > 0 else 0

    return {
        "size_percent": size_percentage,
        "item_percent": item_percentage,
        "price_percent": price_percentage,
        "volume_percent": volume_percentage}
