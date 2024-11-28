# Data Extraction and Processing Project

## Overview

This project is designed to extract, process, and store data about supplements from various brands and websites in the Brazilian market. Using web scraping and data transformation techniques, the system consolidates product information into structured formats suitable for efficient storage and analysis.

The project employs a modular architecture to ensure scalability, maintainability, and clarity, following the ETL (Extract, Transform, Load) paradigm.

---

## Directory Structure

### `config/`
Contains configuration files and scripts for setting up the project environment.

- **`entrypoint/`**: Scripts for environment initialization:
  - `entrypoint.sh`: Automates environment setup.
  - `requirements.sh`: Installs required dependencies.
  - `requirements.txt`: Lists Python dependencies.

- **`setup/`**: Scripts for configuring services:
  - `display.py`: Manages data visualization settings.
  - `shopify.py`: Configures integration with Shopify.

---

### `jobs/`
Manages scheduled data extraction and processing tasks for various pages and brands.

- **`data_intelligence/`**: Processes and enriches product data:
  - `product_class/`: Handles product classification.
  - `product_description/`: Refines product descriptions.
  - `product_flavor/`: Identifies and processes product flavors.
  - `product_remake_description/`: Enhances and updates existing product descriptions.

- **`data_shelf/`**: Handles historical and structured data:
  - `history_price/`: Tracks product price history.
  - `load_master/`: Processes and loads master product lists.

- **`master_page/`**: Orchestrates the scraping of main website pages.
- **`slave_page/`**: Extracts data from subpages, organized by brands and regions:
  - `brazil/`: Includes configurations for scraping websites in Brazil.
  - `united_states/`: Configurations for scraping U.S.-based websites.

---

### `lib/`
Core library modules for implementing the ETL pipeline.

- **`extract/`**: Handles data extraction and crawling:
  - `crawler.py`: Implements web crawling functionality.
  - `extract.py`: Extracts specific data elements.
  - `selenium_service.py`: Automates web scraping using Selenium.

- **`transform/`**: Responsible for data transformation and enrichment:
  - `product_definition.py`: Refines and structures product information.
  - `transform_functions.py`: Contains auxiliary transformation logic.

- **`load/`**: Manages data storage and ingestion:
  - `image_ingestion.py`: Handles ingestion of product images.
  - `load_master.py`: Processes master data for loading.

---

### `utils/`
Utility functions used throughout the project.

- **`dataframe.py`**: Manages and manipulates dataframes.
- **`file_system.py`**: Handles file management and storage.
- **`log.py`**: Configures and manages logging.
- **`py_functions.py`**: General-purpose Python utility functions.
- **`wordlist/`**: Contains word lists and dictionaries specific to the Brazilian supplement market.

---

## Key Technologies

- **Python**: The main programming language for the project.
- **Selenium**: Used for web scraping and automation.
- **Docker**: Ensures a consistent and portable execution environment.
- **Shopify API**: Integrated for managing e-commerce data.

---
