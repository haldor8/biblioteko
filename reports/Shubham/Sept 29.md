Today I created:

## 1) Markdown Converter
   
   1.1 Sends each PDF page to an AI model for OCR correction. 
   The script uploads each scanned PDF part to Gemini AI (Using API) and asks it to correct OCR errors such as spelling mistakes, broken characters, wrong accents, and incorrect French grammar.

    1.2 Converts each corrected page into clean Markdown format

    Using a detailed prompt, the AI reformats the content into structured Markdown with proper headings, lists, italics, quotes, citations, and layout matching the original book.

   1.3 Processes all PDF parts in order and assembles them

    The script processes each PDF file (part 1, part 2, etc.), adds a labeled section (e.g., “Partie 1”), and concatenates all corrected Markdown text.

   1.4 Saves the final combined Markdown to a clean output file

    After processing all pages, it writes the full corrected Markdown content to a final .md file in the output directory.    


