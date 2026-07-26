import requests
import json
import csv
import os
import re
import math
from datetime import datetime


API_URL = "https://dummyjson.com/products/search"
REQUEST_TIMEOUT = 10
OUTPUT_DIRECTORY = "output"

def get_number(prompt):
    while True:
        try:
            number = float(input(prompt))
            if not math.isfinite(number):
                print("Error: Please enter a finite number.")
                continue
            return number
        except ValueError:
            print("Error: Please enter a valid number.")


def get_price_range():
    while True:
        min_price = get_number("Enter minimum price: ")
        max_price = get_number("Enter maximum price: ")

        if min_price < 0 or max_price < 0:
            print("Error: Price values cannot be negative.")
            continue
        if min_price > max_price:
            print("Error: Minimum price cannot be greater than maximum price.")
            continue
        return min_price, max_price


def get_min_rating():
    while True:
        min_rating = get_number("Enter minimum rating: ")
        if 0 <= min_rating <= 5:
            return min_rating
        print("Error: Minimum rating must be between 0 and 5.")


def get_sort_choice():
    print("\nSort options:")
    print("1 - Price: Low to High")
    print("2 - Price: High to Low")
    print("3 - Rating: High to Low")
    print("4 - Stock: High to Low")
    while True:
        sort_choice = input("Choose a sort option (1-4): ").strip()
        if sort_choice in ("1", "2", "3", "4"):
            return sort_choice
        print("Error: Please choose a number between 1 and 4.")


def sort_products(products, sort_choice):
    sort_options = {
        "1": ("price", False),
        "2": ("price", True),
        "3": ("rating", True),
        "4": ("stock", True)
    }
    field, reverse = sort_options[sort_choice]
    return sorted(
        products,
        key=lambda product: product[field],
        reverse=reverse
    )


def fetch_products(search_keyword):
    response = requests.get(
        API_URL,
        params={
            "q": search_keyword,
            "limit": 0
        },
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    data = response.json()
    return data["products"]


def clean_product(product):
    price = product.get("price")
    discount_percentage = product.get("discountPercentage")
    rating = product.get("rating")
    stock = product.get("stock")
    return {
        "id": product.get("id"),
        "title": product.get("title") or "Unknown",
        "brand": product.get("brand") or "Unknown",
        "category": product.get("category") or "Unknown",
        "price": price if price is not None else 0,
        "discount_percentage": (
            discount_percentage if discount_percentage is not None else 0
        ),
        "rating": rating if rating is not None else 0,
        "stock": stock if stock is not None else 0,
        "availability_status": (
            product.get("availabilityStatus") or "Unknown"
        ),
        "shipping_information": (
            product.get("shippingInformation") or "Unknown"
        ),
        "thumbnail": product.get("thumbnail") or ""
    }


def is_valid_number(value):
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def is_valid_product(product):
    return (
        product["id"] is not None
        and product["title"] != "Unknown"
        and is_valid_number(product["price"])
        and product["price"] >= 0
        and is_valid_number(product["rating"])
        and 0 <= product["rating"] <= 5
        and is_valid_number(product["stock"])
        and product["stock"] >= 0
    )


def clean_products(products):
    cleaned_products = []
    invalid_products = []

    for product in products:
        cleaned_product = clean_product(product)

        if not is_valid_product(cleaned_product):
            invalid_products.append(cleaned_product)
            continue

        cleaned_products.append(cleaned_product)

    return cleaned_products, invalid_products


def remove_duplicate_products(products):
    unique_products = []
    seen_ids = set()

    for product in products:
        if product["id"] not in seen_ids:
            unique_products.append(product)
            seen_ids.add(product["id"])
    return unique_products


def filter_products(products, min_price, max_price, min_rating):
    filtered_products = []

    for product in products:
        if (
            min_price <= product["price"] <= max_price
            and product["rating"] >= min_rating
        ):
            filtered_products.append(product)

    return filtered_products


def save_json(products, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            products,
            file,
            indent=4,
            ensure_ascii=False
        )


def save_csv(products, output_file):
    if not products:
        return False

    fieldnames = products[0].keys()

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

    return True


def create_output_paths(search_keyword):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    safe_keyword = re.sub(
        r"[^a-zA-Z0-9_-]",
        "_",
        search_keyword.strip().lower()
    )

    json_output_file = os.path.join(
        OUTPUT_DIRECTORY,
        f"{safe_keyword}_{timestamp}.json"
    )

    csv_output_file = os.path.join(
        OUTPUT_DIRECTORY,
        f"{safe_keyword}_{timestamp}.csv"
    )

    return json_output_file, csv_output_file


def print_process_summary(
    total_products,
    cleaned_product_count,
    invalid_product_count,
    duplicate_count,
    removed_product_count,
    filtered_product_count
):
    print("\nProcess summary:")
    print("-" * 40)
    print("API connection: Successful")
    print("Products fetched:", total_products)
    print("Products cleaned:", cleaned_product_count)
    print("Invalid products removed:", invalid_product_count)
    print("Duplicate products removed:", duplicate_count)
    print("Products removed by filters:", removed_product_count)
    print("Products remaining:", filtered_product_count)
    print("-" * 40)


def print_products(products):
    if not products:
        print("No products matched the selected filters.")
        return

    print("\nFiltered products:")

    for index, product in enumerate(products, start=1):
        print(f"\n{index}. {product['title']}")
        print(f"Brand: {product['brand']}")
        print(f"Category: {product['category']}")
        print(f"Price: ${product['price']:.2f}")
        print(f"Rating: {product['rating']}")
        print(f"Stock: {product['stock']}")
        print(f"Availability: {product['availability_status']}")
        print("-" * 40)


def main():
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    search_keyword = input("Enter a product keyword: ").strip()
    if not search_keyword:
        print("Error: Search keyword cannot be empty.")
        raise SystemExit

    min_price, max_price = get_price_range()
    min_rating = get_min_rating()
    sort_choice = get_sort_choice()

    try:
        products = fetch_products(search_keyword)
        cleaned_products, invalid_products = clean_products(products)
        unique_products = remove_duplicate_products(cleaned_products)
        filtered_products = filter_products(
            unique_products,
            min_price,
            max_price,
            min_rating
        )

        total_products = len(products)
        cleaned_product_count = len(cleaned_products)
        unique_product_count = len(unique_products)
        duplicate_count = cleaned_product_count - unique_product_count
        filtered_product_count = len(filtered_products)
        removed_product_count = unique_product_count - filtered_product_count
        invalid_product_count = len(invalid_products)

        filtered_products = sort_products(filtered_products, sort_choice)

        json_output_file, csv_output_file = create_output_paths(
            search_keyword
        )
        
        save_json(filtered_products, json_output_file)
        print(f"JSON report saved to: {json_output_file}")

        if save_csv(filtered_products, csv_output_file):
            print(f"CSV report saved to: {csv_output_file}")
        else:
            print(
                "CSV report was not created because "
                "no products matched the filters."
            )

        print_process_summary(
            total_products,
            cleaned_product_count,
            invalid_product_count,
            duplicate_count,
            removed_product_count,
            filtered_product_count
        )

        print_products(filtered_products)

    except requests.exceptions.Timeout:
        print("Error: The API did not respond in time.")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the internet.")
    except requests.exceptions.HTTPError as error:
        print("HTTP error occurred:", error)
    except requests.exceptions.RequestException as error:
        print("An error occurred during the request:", error)
    except (KeyError, ValueError) as error:
        print("An error occurred while reading the data:", error)
    except OSError as error:
        print("An error occurred while saving output files:", error)


if __name__ == "__main__":
    main()