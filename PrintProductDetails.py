def print_product_details(product_data):
    print("=" * 30 + " Product Details " + "=" * 30)

    for key, value in product_data.items():
        if key == 'Size Chart' and value is not None:
            print(f"{key}:")
            print(f"  Title: {value.get('title', 'N/A')}")
            print(f"  Headers: {', '.join(value.get('headers', []))}")
            print("  Data:")
            for row in value.get('data', []):
                print(row)
        elif key in ['Image Sources', 'Colors', 'Colored Img Src', 'Colored Img Src Modified', 'Sizes']:
            print(f"{key}:")
            value_list = value if isinstance(value, list) else [value]
            if value_list:
                print(value_list)
            else:
                print("None")
            # for item in value_list:
            #     print(f"  - {item}")
        elif isinstance(value, list):
            print(f"{key}:")
            for item in value:
                print(f"  - {item}")
        elif isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  - {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")

    print()
