# Python PDF Resume Builder (ReportLab)

This Python script leverages the ReportLab library to generate a professional, dark-themed PDF resume. It uses a class-based approach (`ResumeBuilder`) combining low-level canvas operations for layout control with Platypus `Paragraph` objects for rich text formatting (including bold, italics, and clickable links).

## Features

*   **PDF Resume Generation:** Creates a multi-page A4 PDF document.
*   **Class-Based Design:** Encapsulates resume building logic within the `ResumeBuilder` class for organization and reusability.
*   **Custom Dark Theme:** Features a dark blue background with white text and configurable accent colors.
*   **Rich Text Formatting:** Utilizes ReportLab Paragraphs to support:
    *   Bold and Italic text.
    *   Clickable hyperlinks (e.g., for email, websites).
    *   Bulleted lists.
*   **Structured Layout:** Provides methods for adding standard resume sections:
    *   Name and Contact Information.
    *   Section Headers with Dividers.
    *   Work Experience / Education / Projects with titles and dates aligned.
    *   Paragraphs and bullet points with indentation options.
*   **Skills Section with Progress Bars:** Visually represents skill proficiency with percentage text and graphical bars.
*   **Automatic Page Breaking:** Handles content overflow by creating new pages and redrawing the background.
*   **Configurable Styling:** Class attributes allow easy modification of colors, margins, font sizes, and spacing.
*   **Example Included:** A `build_resume` function demonstrates how to use the `ResumeBuilder` class with sample data.

## Sample Style Description

The generated resume features a distinct dark theme:
*   **Background:** Deep Blue (`#202938`)
*   **Text:** White
*   **Layout:** Standard A4 with defined margins. Sections are clearly separated by headers and horizontal lines. Skills are presented with text labels, percentages, and horizontal progress bars.

*(Note: Consider adding a screenshot of the generated PDF here if possible)*

## Prerequisites

*   **Python 3.x**
*   **ReportLab Library:** The core dependency for PDF generation.

## Installation

1.  Ensure you have Python 3 installed.
2.  Install the ReportLab library using pip:
    ```bash
    pip install reportlab
    ```

## Usage

1.  Save the Python script (e.g., `generate_resume.py`).
2.  Run the script from your terminal:
    ```bash
    python generate_resume.py
    ```
3.  By default, this will execute the `build_resume()` function and generate a PDF file named `abdelfattah_zowail_resume.pdf` (or `resume_builder_output.pdf` if `build_resume` is not called directly) in the same directory as the script.

## Customization Guide

To generate your own resume using this script:

1.  **Modify the `build_resume()` Function:** This is the primary place to input your personal information.
    *   Change the arguments to `builder.add_name()`, `builder.add_contact_info()`, etc., to reflect your details.
    *   Update the content within the Work Experience, Education, and Projects sections by calling `builder.add_title_with_date()`, `builder.add_paragraph()`, `builder.add_bullet_point()`, and `builder.add_link()` as needed.
    *   Modify the `skills_data` list within `build_resume()` with your skills and proficiency percentages.
    *   Update the Technologies & Languages list using `builder.add_tech_language_item()`.
    *   Change the output filename in the `build_resume` function call if desired: `build_resume(filename="your_name_resume.pdf")`.

2.  **Adjust `ResumeBuilder` Class Constants (Optional):** For global style changes:
    *   Modify color definitions (e.g., `DARK_BLUE`, `TEXT_COLOR`, `LINK_COLOR`) at the top of the `ResumeBuilder` class. Note that `LINK_COLOR` is converted to hex internally for use in Paragraph HTML tags.
    *   Adjust margins, font sizes, and spacing constants (e.g., `LEFT_MARGIN`, `NAME_SIZE`, `SPACE_MEDIUM`) within the class definition. *Be aware that significant changes to spacing or font sizes might require adjustments to layout calculations or method calls in `build_resume()`.*

3.  **Advanced Style Changes (Optional):**
    *   Modify the `ParagraphStyle` definitions within the `_setup_styles()` method for finer control over text appearance (e.g., different fonts, line spacing). Requires understanding ReportLab styles.

## Code Structure Overview

*   **`ResumeBuilder` Class:**
    *   `__init__()`: Initializes the canvas, sets up styles, draws the initial background.
    *   `_setup_styles()`: Defines various `ParagraphStyle` objects used for formatting text.
    *   `_draw_background()`: Fills the current page with the background color.
    *   `_check_page_break()`: Determines if content fits and triggers a new page if necessary.
    *   `_update_y()`: Manages the current vertical drawing position (`self.current_y`).
    *   `add_*()` methods (e.g., `add_name`, `add_section_header`, `add_paragraph`, `add_skill`, `add_link`): Public methods to add specific types of content to the resume. They handle text formatting, positioning, calling `_check_page_break`, and updating the Y coordinate.
    *   `save()`: Saves the generated PDF document.
*   **`build_resume()` Function:**
    *   An example function demonstrating how to instantiate `ResumeBuilder` and call its methods sequentially to populate the resume with specific content.
*   **`if __name__ == "__main__":` block:**
    *   Ensures that `build_resume()` is called when the script is executed directly.
