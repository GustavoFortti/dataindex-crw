# Data Extraction and Processing Project

## Overview

This project is designed to extract, process, and store data about supplements from various brands and websites in the market. Using web scraping and data transformation techniques, the system consolidates product information into structured formats suitable for efficient storage and analysis.

The project employs a modular architecture to ensure scalability, maintainability, and clarity, following the ETL (Extract, Transform, Load) paradigm.

[ETL Process](https://drive.google.com/file/d/1uEEMiGHl6CrHUqqyXI-wdVhJH490tlc1/view?usp=drive_link)

---

## Directory Structure

### `jobs/`
Manages scheduled data extraction and processing tasks.

- `data_extract.py`: Handles the extraction of raw data.
- `data_load.py`: Loads processed data into storage.
- `data_transform.py`: Applies transformations to the extracted data.
- `pipeline.py`: Orchestrates the ETL workflow.
- `product_description.py`: Processes and enriches product descriptions.

---

### `lib/`
Core library modules for implementing the ETL pipeline.

- **`extract/`**: Handles data extraction and crawling.
  - `crawler.py`: Implements web crawling functionality.
  - `selenium_service.py`: Automates web scraping using Selenium.

- **`load/`**: Manages data ingestion and components for loading data.
  - **`components/`**: Contains modular functions for specific tasks:
    - `cupom_code_button.py`: Manages coupon-related data.
    - `generate_price_chart.py`: Generates price trend visualizations.
    - `redirecionamento_button.py`: Handles redirect button functionality.
  - `shopify.py`: Configures Shopify integration.

- **`transform/`**: Responsible for data transformation and enrichment.
  - `product_definition.py`: Structures product definitions.
  - `product_info.py`: Processes product-specific information.
  - `transform_functions.py`: Contains helper functions for transformations.

- **`utils/`**: Utility functions used throughout the project.
  - `dataframe.py`: Handles dataframe manipulation.
  - `data_quality.py`: Ensures the integrity of data.
  - `file_system.py`: Manages file I/O operations.
  - `log.py`: Configures project logging.
  - `text_functions.py`: Processes and manipulates text.

- **`wordlist/`**: Contains word lists and dictionaries for processing.
  - `wordlist_flavor.py`: Handles flavor-related terms.
  - `wordlist_format.py`: Manages product format vocabulary.
  - `collection.py`: System of rules for classifying products into collections.

---

### `pages/`
Manages website-specific scraping configurations and elements.

- **`a1supplements/`**: Contains configurations for the A1 Supplements website.
  - `page_elements.py`: Defines page elements to be scraped.
  - `page.py`: Contains page-specific scraping logic.
  - `page_url.py`: Manages URL definitions for crawling.
  - `seed.json`: Provides initial configuration for scraping.

- `page.py`: Generic scraping logic applicable to multiple pages.

---

### Key Technologies

- **Python**: Main programming language for the project.
- **Selenium**: Used for web scraping and automation.
- **Shopify API**: Integrated for managing e-commerce data.

---

## Additional Information

The project is designed to adapt to new sources and requirements with minimal effort. Each module can be enhanced or replaced independently, ensuring flexibility and scalability.