import importlib
import os
import time
from typing import Any, Dict, List, Optional

import openai
from dotenv import load_dotenv

from jobs.job_manager import JobBase
from src.lib.utils.dataframe import (create_or_read_df,
                                     read_and_stack_csvs_dataframes)
from src.lib.utils.file_system import (create_directory_if_not_exists,
                                       create_file_if_not_exists,
                                       file_exists_with_modification_time,
                                       list_directory, read_file, read_json,
                                       save_file_with_line_breaks, save_json)
from src.lib.utils.log import message
from src.lib.utils.page_functions import get_pages_with_status_true
from src.lib.utils.text_functions import generate_hash
from src.pages.page import Page

# Load environment variables
load_dotenv()
OPEN_AI_CHAT_KEY: Optional[str] = os.getenv("OPEN_AI_CHAT_KEY")


def run(job_base: JobBase) -> Optional[None]:
    """
    Executes the data transformation pipeline for a given job.

    Args:
        job_base (JobBase): An instance of JobBase containing job-specific configurations.

    Returns:
        Optional[None]: Exits the program after transformations and saves the result.
    """
    # Step 1: Initialize and load the pages
    message("Product description process started.")
    pages: List[str] = list_directory(job_base.pages_path)
    pages = [page for page in pages if "." not in page and "__" not in page]

    for page_name in pages:
        page_module = importlib.import_module(f"src.pages.{page_name}.page")
        page_args: Dict[str, Any] = page_module.page_arguments
        page: Page = Page(**page_args)
        job_base.append_pages(page)

    create_directory_if_not_exists(job_base.data_path)

    # Control file path
    control_file_path: str = os.path.join(job_base.data_path, "control.json")
    create_file_if_not_exists(control_file_path, "{}")
    control_data: Dict[str, Any] = read_json(control_file_path)

    # Current date in YYYY-MM-DD format
    date_today: str = job_base.date_today

    # Initialize entry for the current date if it doesn't exist
    if date_today not in control_data:
        control_data[date_today] = {
            "limit": 3000,
            "requests": 0,
            "tokens_in": 0,
            "tokens_out": 0
        }

    message(f"Requests: {control_data[date_today]['requests']}")
    message(f"Limit: {control_data[date_today]['limit']}")

    if control_data[date_today]["requests"] >= control_data[date_today]["limit"]:
        message(
            f"Daily limit of {control_data[date_today]['limit']} descriptions reached for {date_today}."
        )
        return

    # Load pages with status 'True'
    active_pages: List[str] = get_pages_with_status_true(job_base)

    # Load the DataFrame with product data
    df: Any = read_and_stack_csvs_dataframes(
        job_base.src_data_path,
        active_pages,
        job_base.file_name_transform_csl,
        dtype={'ref': str}
    )

    df = df[['ref', 'brand', 'page_name']]
    product_info_path: str = os.path.join(job_base.data_path, "product_info.csv")
    df_product_info: Any = create_or_read_df(
        path=product_info_path,
        columns=[
            "ref",
            "brand",
            "page_name",
            "hash",
            "has_origin",
            "origin_is_updated",
            "description_exists",
            "latest_description_update",
        ],
        dtype={'ref': str}
    )

    # Initialize new columns
    df["hash"] = None
    df["has_origin"] = False
    df["origin_is_updated"] = 0
    df["description_exists"] = 0
    df["latest_description_update"] = None

    for idx, row in df.iterrows():
        ref: str = str(row['ref'])
        page_name: str = str(row['page_name'])

        products_path: str = os.path.join(job_base.src_data_path, page_name, "products")
        description_file_path: str = os.path.join(products_path, f"{ref}_description.txt")
        product_description: Optional[str] = read_file(description_file_path)

        hash_value: Optional[str] = None
        if product_description:
            hash_value = generate_hash(product_description)
            df.at[idx, "hash"] = hash_value
            df.at[idx, "has_origin"] = True

        existing_product = df_product_info[df_product_info["ref"] == ref]
        old_hash: Optional[str] = (
            existing_product["hash"].values[0]
            if not existing_product.empty else None
        )

        if old_hash and hash_value:
            df.at[idx, "origin_is_updated"] = int(old_hash != hash_value)
        else:
            df.at[idx, "origin_is_updated"] = 0

        file_status: Any = file_exists_with_modification_time(
            products_path,
            f"{ref}_description_ai.txt"
        )
        df.at[idx, "description_exists"] = int(file_status[0])
        df.at[idx, "latest_description_update"] = file_status[1]

    # Sort the DataFrame based on multiple criteria
    df_sorted = df.sort_values(
        ["description_exists", "origin_is_updated", "latest_description_update", "has_origin"],
        ascending=[False, False, False, False]
    )
    df_sorted.to_csv(product_info_path, index=False)

    # Filter DataFrame for processing
    df_to_process: Any = df_sorted[
        (df_sorted['has_origin'] == True) &
        ((df_sorted['origin_is_updated'] == 0) | (df_sorted['description_exists'] == 0))
    ]

    # Iterate over DataFrame rows for processing
    for _, row in df_to_process.iterrows():
        ref: str = str(row['ref'])
        page_name: str = str(row['page_name'])

        # Construct the product description file path
        products_path: str = os.path.join(job_base.src_data_path, page_name, "products")
        description_file_path: str = os.path.join(products_path, f"{ref}_description.txt")
        product_description: Optional[str] = read_file(description_file_path)

        if not product_description:
            continue

        message(f"REQUEST - {control_data[date_today]['requests']}")
        message(f"Ref: {ref}")
        message(f"Path: {description_file_path}")
        description_ai_path: str = os.path.join(products_path, f"{ref}_description_ai.txt")

        product_description_ai: Optional[str] = refine_description(
            product_description,
            OPEN_AI_CHAT_KEY
        )

        if product_description_ai:
            message(f"{ref} - product_description_ai - OK")
            save_file_with_line_breaks(description_ai_path, product_description_ai)
            save_json(control_file_path, control_data)

        control_data[date_today]["requests"] += 1
        time.sleep(2)

        if control_data[date_today]["requests"] >= control_data[date_today]["limit"]:
            save_json(control_file_path, control_data)
            message(
                f"Daily limit of {control_data[date_today]['limit']} descriptions reached for {date_today}."
            )
            return


def refine_description(description: str, assistant_id: str) -> Optional[str]:
    """
    Uses the OpenAI API to generate a refined version of the product description.

    Args:
        description (str): The product description to be refined.
        assistant_id (str): The OpenAI assistant ID.

    Returns:
        Optional[str]: Refined text or None in case of an error.
    """
    try:
        # Set up the OpenAI client
        client = openai.OpenAI()

        # Create a new thread
        thread = client.beta.threads.create()

        # Add a message to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=description
        )

        # Execute the assistant to generate a response
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # Periodically check the run status
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                break
            elif run_status.status == 'failed':
                raise Exception("The execution failed.")

        # List all the messages in the thread
        messages = client.beta.threads.messages.list(thread_id=thread.id)

        # Get the last message from the assistant
        for msg in messages.data:
            if msg.role == "assistant" and hasattr(msg.content[0], 'text'):
                return msg.content[0].text.value

        return None

    except Exception as e:
        print(f"Error calling the OpenAI API: {e}")
        return None
