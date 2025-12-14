## 1. `main()`

The `main()` function is the central orchestrator of the entire PDF-to-Markdown pipeline. It performs the following tasks:

### a. Argument Validation
- Checks that exactly one argument (the path to the input PDF) is provided.
- Exits the program with usage instructions if the argument is missing.
- Confirms that the input PDF file exists, exiting with an error message if not.

### b. Step 1: Split PDF into Chunks
- Calls `split_pdf(input_pdf)` to split the scanned PDF into smaller, manageable parts.
- Stores these chunks in the `raw_parts` directory.
- Returns the number of chunks created (`chunks_created`).

### c. Step 2: Clean and Enhance Pages
- Calls `clean_all_parts()` to enhance image quality for OCR:
  - Increases contrast, sharpness, and brightness.
  - Crops pages to the main content while keeping margins.
- Stores cleaned pages in `cleaned_parts`.
- Returns the total number of pages cleaned (`pages_cleaned`).

### d. Step 3: Split Double Pages
- Calls `process_all_pdfs_in_folder()` to split any double-page scans into single pages.
- Ensures that all pages are formatted properly for AI processing.
- Stores results in `formatted_parts`.

### e. Step 4: AI Conversion and Correction
- Calls `convert_all_parts_to_markdown()` to:
  - Correct OCR errors.
  - Convert scanned content into properly formatted Markdown.
  - Preserve headings, lists, citations, and French language specifics.
- Returns the final Markdown content (`final_markdown`).

### f. Step 5: Save Final Output
- Calls `save_final_markdown(final_markdown)` to:
  - Save the Markdown content to a file.
  - Return the path to the saved file (`output_file`).

### g. Logging and Summary
- Prints a clear, step-by-step summary of the entire pipeline:
  - Original PDF name.
  - Number of chunks created.
  - Pages cleaned.
  - Final Markdown output path.
  - Total characters in the Markdown file.

## 2. `if __name__ == "__main__": main()`
- Ensures that the `main()` function is executed only when the script is run directly.
- Prevents the code from running if imported as a module.
