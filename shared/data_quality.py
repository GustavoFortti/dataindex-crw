from utils import check_url_existence, is_price

def status_tag(new_row):
    errors = []

    if not is_price(new_row["price"]):
        errors.append("Invalid price format.")

    if not check_url_existence(new_row["image_url"]):
        errors.append("Image URL does not exist.")

    if not check_url_existence(new_row["product_url"]):
        errors.append("Product URL does not exist.")

    if errors:
        for error in errors:
            print(error)
        exit(1)
    else:
        print("status_tag: All validations passed successfully.")
        exit(0)