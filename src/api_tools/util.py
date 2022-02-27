

def print_result(result):
    print("=" * 80)
    print("response headers")
    print("-" * 80)
    print(result.headers)
    print("=" * 80)
    print("response body")
    print("-" * 80)
    print(result.text)
    print("=" * 80)