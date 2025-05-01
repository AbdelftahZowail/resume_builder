import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import Color, white, blue  # Import necessary colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT

class ResumeBuilder:
    """
    A class to build a resume PDF using ReportLab's low-level canvas operations
    and Platypus Paragraph for formatted text and links.
    """
    # --- Configuration (Class Attributes) ---
    PAGE_WIDTH, PAGE_HEIGHT = A4

    # Colors
    DARK_BLUE = Color(32 / 255, 41 / 255, 56 / 255)
    TEXT_COLOR = white
    LINK_COLOR = white  # Default link color (can be overridden e.g., LINK_COLOR = "#4A90E2")
    LINE_COLOR = white
    PROGRESS_BAR_BG = Color(60 / 255, 70 / 255, 85 / 255)
    PROGRESS_BAR_FG = white

    # Margins & Dimensions
    LEFT_MARGIN = 1.5 * cm
    RIGHT_MARGIN = 1.5 * cm
    TOP_MARGIN = 1.5 * cm
    BOTTOM_MARGIN = 1.5 * cm
    CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN
    RIGHT_ALIGN_X = PAGE_WIDTH - RIGHT_MARGIN  # Right edge for alignment
    BOTTOM_DRAWABLE_Y = BOTTOM_MARGIN         # Bottom boundary for content

    # Font Sizes (Points)
    NAME_SIZE = 25
    CONTACT_SIZE = 12.5
    SECTION_HEADER_SIZE = 13.5
    TITLE_SIZE = 13.5
    BODY_TEXT_SIZE = 12.5
    SMALL_ITALIC_SIZE = 11.5
    SKILL_NAME_SIZE = 12.5
    SKILL_PERCENT_SIZE = 11.5

    # Spacing (ReportLab Units - cm)
    SPACE_VSMALL = 0.1 * cm
    SPACE_SMALL = 0.2 * cm
    SPACE_MEDIUM = 0.4 * cm
    SPACE_LARGE = 0.6 * cm
    SPACE_SECTION_HEADER = 0.15 * cm
    SPACE_AFTER_LINE = 0.3 * cm
    SPACE_AFTER_NAME = 0.2 * cm
    SPACE_AFTER_PERCENT = 0.2 * cm
    SPACE_BETWEEN_TITLE_DATE = 1 * cm

    # Skill Bar Dimensions
    SKILL_NAME_WIDTH = 3.5 * cm # Adjusted width
    SKILL_PERCENT_WIDTH = 1.5 * cm
    PROGRESS_BAR_WIDTH = 6 * cm # Adjusted width to fit with others
    PROGRESS_BAR_HEIGHT = 0.3 * cm

    # Indentation
    INDENT_AMOUNT = 0.5 * cm

    def __init__(self, filename="resume_builder_output.pdf"):
        """
        Initializes the ResumeBuilder.

        Args:
            filename (str): The name of the PDF file to be generated.
        """
        self.buffer = io.BytesIO() # Can be used if saving to buffer instead of file directly
        self.c = canvas.Canvas(filename, pagesize=A4)
        self.filename = filename
        self.current_y = self.PAGE_HEIGHT - self.TOP_MARGIN
        self.link_color_hex = "#ffffff" # Initialize with a default
        self._setup_styles()
        self._draw_background()  # Draw background on the first page

    def _setup_styles(self):
        """Initializes paragraph styles used throughout the resume."""
        styles = getSampleStyleSheet()

        # --- Correctly Convert LINK_COLOR to Hex String ---
        if isinstance(self.LINK_COLOR, Color):
            # Manually convert ReportLab Color object (RGB 0.0-1.0) to hex string #RRGGBB
            r, g, b = self.LINK_COLOR.red, self.LINK_COLOR.green, self.LINK_COLOR.blue
            r_int, g_int, b_int = int(r * 255), int(g * 255), int(b * 255)
            # Clamp values just in case
            r_int = max(0, min(255, r_int))
            g_int = max(0, min(255, g_int))
            b_int = max(0, min(255, b_int))
            self.link_color_hex = f"#{r_int:02x}{g_int:02x}{b_int:02x}"
        elif isinstance(self.LINK_COLOR, str):
             # Assume it's already a hex string (e.g., "#RRGGBB") or a color name ("blue")
             self.link_color_hex = self.LINK_COLOR
        else:
            # Fallback if LINK_COLOR is something unexpected
            print(f"Warning: Unexpected type for LINK_COLOR: {type(self.LINK_COLOR)}. Defaulting to white.")
            self.link_color_hex = "#ffffff" # Default to white hex

        # --- Define Base and Specific Styles ---
        self.base_style = ParagraphStyle(
            name='BaseWhite',
            parent=styles['Normal'],
            textColor=self.TEXT_COLOR,
            fontSize=self.BODY_TEXT_SIZE,
            leading=14, # Line spacing
            fontName='Helvetica'
        )

        self.styles = {
            'name': ParagraphStyle(
                name='NameStyle', parent=self.base_style, fontSize=self.NAME_SIZE,
                fontName='Helvetica-Bold', alignment=TA_LEFT
            ),
            'contact': ParagraphStyle(
                name='ContactStyle', parent=self.base_style, fontSize=self.CONTACT_SIZE,
                alignment=TA_LEFT, leading=12
            ),
            'section_header': ParagraphStyle(
                name='SectionHeaderStyle', parent=self.base_style, fontSize=self.SECTION_HEADER_SIZE,
                fontName='Helvetica-Bold'
            ),
            'title': ParagraphStyle(
                name='TitleStyle', parent=self.base_style, fontSize=self.TITLE_SIZE,
                fontName='Helvetica-Bold'
            ),
            'italic': ParagraphStyle( # General small italic (might not be used directly often)
                name='ItalicStyle', parent=self.base_style, fontSize=self.SMALL_ITALIC_SIZE,
                fontName='Helvetica-Oblique'
            ),
            'body': ParagraphStyle( # Standard body text
                name='BodyStyle', parent=self.base_style, fontSize=self.BODY_TEXT_SIZE
            ),
            'body_indent': ParagraphStyle( # Indented body text (e.g., bullets)
                name='BodyIndentStyle', parent=self.base_style, fontSize=self.BODY_TEXT_SIZE,
                leftIndent=self.INDENT_AMOUNT
            ),
            'body_italic': ParagraphStyle( # Non-indented italic body text
                name='BodyItalicStyle', parent=self.base_style, fontSize=self.BODY_TEXT_SIZE,
                fontName='Helvetica-Oblique'
            ),
            'body_italic_indent': ParagraphStyle( # Indented italic body text
                name='BodyItalicIndentStyle', parent=self.base_style, fontSize=self.BODY_TEXT_SIZE,
                fontName='Helvetica-Oblique', leftIndent=self.INDENT_AMOUNT
            ),
            'skill_name': ParagraphStyle(
                name='SkillNameStyle', parent=self.base_style, fontSize=self.SKILL_NAME_SIZE,
                alignment=TA_LEFT, leading=12
            ),
            'skill_percent': ParagraphStyle(
                name='SkillPercentStyle', parent=self.base_style, fontSize=self.SKILL_PERCENT_SIZE,
                alignment=TA_RIGHT, leading=12
            ),
            'date': ParagraphStyle( # Style for dates aligned right
                name='DateStyle', parent=self.base_style, fontSize=self.BODY_TEXT_SIZE,
                alignment=TA_RIGHT
            ),
            'tech_lang': ParagraphStyle( # Style for tech/languages list (not indented by default)
                name='TechLangList', parent=self.base_style, leftIndent=0,
                fontSize=self.BODY_TEXT_SIZE, leading=14
            )
        }

    def _draw_background(self):
        """Draws the background color on the current page."""
        self.c.saveState()
        self.c.setFillColor(self.DARK_BLUE)
        self.c.rect(0, 0, self.PAGE_WIDTH, self.PAGE_HEIGHT, fill=1, stroke=0)
        self.c.restoreState()

    def _check_page_break(self, required_height):
        """
        Checks if the required vertical space fits on the current page.
        If not, it finalizes the current page and starts a new one.

        Args:
            required_height (float): The height needed for the next element.
        """
        if self.current_y - required_height < self.BOTTOM_DRAWABLE_Y:
            self.c.showPage()  # Finalize current page, start new one
            self._draw_background()  # Redraw background on new page
            self.current_y = self.PAGE_HEIGHT - self.TOP_MARGIN  # Reset Y to top margin

    def _update_y(self, height_drawn, space_after=SPACE_SMALL):
        """
        Updates the current vertical drawing position (self.current_y).

        Args:
            height_drawn (float): The height of the element just drawn.
            space_after (float): The vertical space to add after the element.
        """
        self.current_y -= (height_drawn + space_after)

    # --- Content Adding Methods ---

    def add_name(self, text):
        """Adds the main name title."""
        p = Paragraph(text, self.styles['name'])
        p_w, p_h = p.wrapOn(self.c, self.CONTENT_WIDTH, 1000) # Max height arbitrary large
        self._check_page_break(p_h + self.SPACE_SMALL) # Check needed height + space after
        p.drawOn(self.c, self.LEFT_MARGIN, self.current_y - p_h)
        self._update_y(p_h, space_after=self.SPACE_SMALL)

    def add_contact_info(self, text_list):
        """Adds contact information lines."""
        total_h = 0
        paragraphs = []
        # First pass: wrap all paragraphs to calculate total height
        for text in text_list:
            p = Paragraph(text, self.styles['contact'])
            p_w, p_h = p.wrapOn(self.c, self.CONTENT_WIDTH, 1000)
            paragraphs.append((p, p_h))
            total_h += p_h + self.SPACE_VSMALL # Add space between contact lines
        # Remove last vsmall space and add the final medium space
        total_h = total_h - self.SPACE_VSMALL + self.SPACE_MEDIUM

        self._check_page_break(total_h) # Check total height needed

        # Second pass: draw the paragraphs
        for p, p_h in paragraphs:
            p.drawOn(self.c, self.LEFT_MARGIN, self.current_y - p_h)
            self._update_y(p_h, space_after=self.SPACE_VSMALL) # Space between lines

        # Add the final larger space after the block
        self.add_space(self.SPACE_MEDIUM - self.SPACE_VSMALL, check_break=False)


    def add_divider(self, space_before=0, space_after=SPACE_AFTER_LINE):
        """Adds a horizontal line separator."""
        line_height = 1  # Minimal height for check
        required_total_height = space_before + line_height + space_after
        self._check_page_break(required_total_height)

        self.current_y -= space_before # Apply space before drawing

        self.c.saveState()
        self.c.setStrokeColor(self.LINE_COLOR)
        self.c.setLineWidth(0.5)
        # Ensure Y hasn't dipped below margin somehow (extra safety)
        draw_y = max(self.current_y, self.BOTTOM_DRAWABLE_Y + line_height)
        self.c.line(self.LEFT_MARGIN, draw_y, self.RIGHT_ALIGN_X, draw_y)
        self.c.restoreState()

        # Update Y position based on where line was drawn + space after
        # We drew at 'draw_y', so reduction is from the original self.current_y
        # Effectively, we just subtract space_after from the line position
        self.current_y = draw_y - space_after

    def add_section_header(self, text):
        """Adds a section header followed by a divider."""
        # Calculate height needed for space, header, space, divider, space
        header_p = Paragraph(text, self.styles['section_header'])
        h_w, h_h = header_p.wrapOn(self.c, self.CONTENT_WIDTH, 1000)
        line_height = 1
        required_height = (self.SPACE_MEDIUM + h_h + self.SPACE_SECTION_HEADER +
                           line_height + self.SPACE_AFTER_LINE)

        self._check_page_break(required_height)

        self.add_space(self.SPACE_MEDIUM, check_break=False) # Add space before header
        header_p.drawOn(self.c, self.LEFT_MARGIN, self.current_y - h_h)
        self._update_y(h_h, space_after=self.SPACE_SECTION_HEADER) # Space after header text
        self.add_divider(space_before=0, space_after=self.SPACE_AFTER_LINE) # Divider adds its own space after

    def _draw_right_aligned_text(self, text, style, current_y_for_calc):
        """Internal helper to draw text aligned to the right margin."""
        # Estimate available width somewhat conservatively
        available_width = self.CONTENT_WIDTH * 0.4
        p = Paragraph(text, style)
        p_w, p_h = p.wrapOn(self.c, available_width, 1000)
        p_w = min(p_w, available_width) # Prevent overflow if text wider than estimate
        draw_x = self.RIGHT_ALIGN_X - p_w
        # Align bottom of text with the calculated bottom Y of the line
        draw_y = current_y_for_calc - p_h
        p.drawOn(self.c, draw_x, draw_y)
        return p_h # Return actual height drawn

    def _add_left_right_line(self, left_text, right_text, left_style_key, right_style_key='date',
                             space_after=SPACE_SMALL):
        """Internal helper for lines with left/right aligned text (e.g., Title/Date)."""
        # 1. Wrap both paragraphs to get their heights
        left_p = Paragraph(left_text, self.styles[left_style_key])
        # Allocate width proportionally (e.g., 60% left, 40% right minus gap)
        max_left_width = self.CONTENT_WIDTH * 0.6 - self.SPACE_BETWEEN_TITLE_DATE / 2
        left_w, left_h = left_p.wrapOn(self.c, max_left_width, 1000)

        right_p = Paragraph(right_text, self.styles[right_style_key])
        max_right_width = self.CONTENT_WIDTH * 0.4 - self.SPACE_BETWEEN_TITLE_DATE / 2
        right_w, right_h = right_p.wrapOn(self.c, max_right_width, 1000)

        # 2. Determine max height and check for page break
        required_height = max(left_h, right_h)
        self._check_page_break(required_height + space_after)

        # 3. Calculate drawing positions
        # Both elements should align their bottoms at this Y coordinate
        target_bottom_y = self.current_y - required_height

        # 4. Draw right text first (using helper) relative to the top Y (current_y)
        # The helper calculates the correct draw_y based on element height
        actual_right_h = self._draw_right_aligned_text(right_text, self.styles[right_style_key], self.current_y)

        # 5. Draw left text, aligning its bottom with target_bottom_y
        left_draw_y = target_bottom_y
        left_p.drawOn(self.c, self.LEFT_MARGIN, left_draw_y)

        # 6. Update Y position based on the max height of the line
        self._update_y(required_height, space_after=space_after)

    def add_title_with_date(self, title_text, date_text):
        """Adds a line with a title (bold) on the left and date on the right."""
        self._add_left_right_line(title_text, date_text, 'title', 'date', space_after=self.SPACE_SMALL)

    def add_text_with_date(self, text, date_text, italic=False, indent=False, space_after=SPACE_SMALL):
        """Adds a line with standard/italic text on left, date on right."""
        style_key = 'body'
        if indent and italic: style_key = 'body_italic_indent'
        elif indent: style_key = 'body_indent'
        elif italic: style_key = 'body_italic'

        # Indentation on left/right lines can look odd, warn or adjust if needed
        if indent:
             print("Warning: Indent=True for add_text_with_date might produce unexpected alignment.")
             # Consider overriding style_key or applying indent logic differently here
             style_key = 'body_italic' if italic else 'body' # Revert to non-indent for now

        self._add_left_right_line(text, date_text, style_key, 'date', space_after=space_after)

    def add_paragraph(self, text, italic=False, indent=False, space_after=SPACE_VSMALL):
        """Adds a standard text paragraph, optionally italic or indented."""
        style_key = 'body'
        if indent and italic: style_key = 'body_italic_indent'
        elif indent: style_key = 'body_indent'
        elif italic: style_key = 'body_italic'

        style = self.styles[style_key]
        p = Paragraph(text, style)
        # Width available depends on whether it's indented (style handles the indent)
        wrap_width = self.CONTENT_WIDTH - (self.INDENT_AMOUNT if indent else 0)
        p_w, p_h = p.wrapOn(self.c, wrap_width, 1000)

        self._check_page_break(p_h + space_after) # Check before drawing

        # Draw at the left margin; the style's leftIndent will handle shifting the text
        draw_x = self.LEFT_MARGIN
        p.drawOn(self.c, draw_x, self.current_y - p_h)
        self._update_y(p_h, space_after=space_after)

    def add_bullet_point(self, text, space_after=SPACE_VSMALL):
        """Adds an indented paragraph prefixed with a bullet character."""
        bullet_char = "■"  # Or "•"
        bullet_text = f"{bullet_char} {text}"
        # Use the body_indent style which has leftIndent set
        style = self.styles['body_indent']
        p = Paragraph(bullet_text, style)
        # Wrap width already considers the style's indent
        wrap_width = self.CONTENT_WIDTH - self.INDENT_AMOUNT
        p_w, p_h = p.wrapOn(self.c, wrap_width, 1000)

        self._check_page_break(p_h + space_after)

        # Draw at the margin, the style handles indenting the text content
        p.drawOn(self.c, self.LEFT_MARGIN, self.current_y - p_h)
        self._update_y(p_h, space_after=space_after)

    def add_link(self, display_text, url, prefix="", italic=False, indent=False, space_after=SPACE_VSMALL):
        """
        Adds a clickable, underlined link with custom display text.

        Args:
            display_text (str): The text to display for the link.
            url (str): The URL the link should point to.
            prefix (str): Optional text to appear before the link (e.g., "■ ", "Website: ").
            italic (bool): If True, makes the display_text italic.
            indent (bool): If True, indents the entire line using the indent style.
            space_after (float): Vertical space to add after this element.
        """
        # Choose base style based on indent flag
        style = self.styles['body_indent'] if indent else self.styles['body']

        # Prepare the link text with HTML tags
        # self.link_color_hex should be set correctly in _setup_styles
        inner_text = f"<i>{display_text}</i>" if italic else display_text
        link_html = f'<a href="{url}"><font color="{self.link_color_hex}"><u>{inner_text}</u></font></a>'

        # Combine prefix and link HTML
        full_text = f"{prefix}{link_html}"

        # Create and wrap the paragraph
        p = Paragraph(full_text, style)
        wrap_width = self.CONTENT_WIDTH - (self.INDENT_AMOUNT if indent else 0)
        p_w, p_h = p.wrapOn(self.c, wrap_width, 1000)

        # Check page break BEFORE drawing
        self._check_page_break(p_h + space_after)

        # Draw the paragraph (indentation handled by the style)
        draw_x = self.LEFT_MARGIN
        p.drawOn(self.c, draw_x, self.current_y - p_h)

        # Update Y position
        self._update_y(p_h, space_after=space_after)

    def add_skill(self, skill_name, percentage):
        """Adds a skill entry with name, percentage, and progress bar."""
        # Estimate row height for vertical centering and page break check
        # Use max of font sizes (via leading) and bar height for consistency
        name_style = self.styles['skill_name']
        percent_style = self.styles['skill_percent']
        # Convert points (leading, font size) to cm approximately
        pt_to_cm = cm / 28.346 # Roughly points per cm
        row_height_estimate = max(name_style.leading * pt_to_cm,
                                  percent_style.leading * pt_to_cm,
                                  self.PROGRESS_BAR_HEIGHT + 0.1*cm) # Add slight buffer to bar height

        self._check_page_break(row_height_estimate) # Check BEFORE drawing

        # Base Y for drawing this row (bottom edge)
        row_base_y = self.current_y - row_height_estimate
        # Center Y for aligning elements vertically
        row_center_y = row_base_y + row_height_estimate / 2

        # --- Draw Skill Name ---
        p_skill = Paragraph(skill_name, name_style)
        p_skill_w, p_skill_h = p_skill.wrapOn(self.c, self.SKILL_NAME_WIDTH+20, 1000)
        # Align bottom of text slightly above row_base_y or center based on height
        draw_y_skill = row_center_y - p_skill_h / 2 # Center align
        p_skill.drawOn(self.c, self.LEFT_MARGIN, draw_y_skill)

        # --- Draw Percentage Text ---
        percent_text = f"{percentage}%"
        p_percent = Paragraph(percent_text, percent_style)
        percent_x = self.LEFT_MARGIN + self.SKILL_NAME_WIDTH + self.SPACE_AFTER_NAME + 20
        p_percent_w, p_percent_h = p_percent.wrapOn(self.c, self.SKILL_PERCENT_WIDTH, 1000)
        # Align bottom or center similarly to skill name
        draw_y_percent = row_center_y - p_percent_h / 2 # Center align
        p_percent.drawOn(self.c, percent_x, draw_y_percent)

        # --- Draw Progress Bar ---
        bar_x = percent_x + self.SKILL_PERCENT_WIDTH + self.SPACE_AFTER_PERCENT
        # Align vertical center of the bar with the row's center Y
        bar_y = row_center_y - self.PROGRESS_BAR_HEIGHT / 2
        self.c.saveState()
        # Background rectangle
        self.c.setFillColor(self.PROGRESS_BAR_BG)
        self.c.rect(bar_x, bar_y, self.PROGRESS_BAR_WIDTH, self.PROGRESS_BAR_HEIGHT, fill=1, stroke=0)
        # Foreground (filled) rectangle
        filled_width = self.PROGRESS_BAR_WIDTH * (percentage / 100.0)
        if filled_width > 0:
            self.c.setFillColor(self.PROGRESS_BAR_FG)
            self.c.rect(bar_x, bar_y, filled_width, self.PROGRESS_BAR_HEIGHT, fill=1, stroke=0)
        self.c.restoreState()

        # --- Update Y position ---
        # Use the estimated row height, NO extra space_after added here
        # Spacing between skills should be handled by calling add_space externally
        self._update_y(row_height_estimate, space_after=0)

    def add_tech_language_item(self, text, space_after=SPACE_SMALL):
        """Adds an item for the Technologies/Languages list (usually bulleted)."""
        # Use Paragraph, include bullet/bold tags directly in the text string
        # The 'tech_lang' style itself is not indented.
        bullet_char = "•"
        item_text = f"{bullet_char} {text}"
        p = Paragraph(item_text, self.styles['tech_lang'])
        p_w, p_h = p.wrapOn(self.c, self.CONTENT_WIDTH, 1000) # Use full width

        self._check_page_break(p_h + space_after)

        p.drawOn(self.c, self.LEFT_MARGIN, self.current_y - p_h)
        self._update_y(p_h, space_after=space_after)

    def add_space(self, height, check_break=True):
        """Adds vertical whitespace."""
        if height <= 0:
            return # Don't add negative or zero space

        if check_break:
            # Check if adding this space *itself* would cross the boundary
            self._check_page_break(height)

        # Ensure we don't go below the drawable boundary just by adding space
        potential_y = self.current_y - height
        if potential_y < self.BOTTOM_DRAWABLE_Y:
            # If it goes below, just move Y to the boundary.
            # The next element's check_page_break will handle the new page.
            self.current_y = self.BOTTOM_DRAWABLE_Y
        else:
            self.current_y = potential_y

    def add_space_to_next_page(self):
        """
        Forces subsequent content onto the next page by adding space
        to fill the remainder of the current page.
        """
        remaining_space = self.current_y - self.BOTTOM_DRAWABLE_Y
        # Add a small tolerance (e.g., 1 point) to ensure break
        if remaining_space > 0.05 * cm :
            self.add_space(remaining_space, check_break=False) # Fill the rest

        # Force Y below the threshold to guarantee next item triggers a page break
        self.current_y = self.BOTTOM_DRAWABLE_Y - 1 # Use a small negative offset


    def save(self):
        """Saves the PDF document to the filename specified during initialization."""
        try:
            self.c.save()
            print(f"PDF saved successfully as {self.filename}")
        except Exception as e:
            print(f"Error saving PDF {self.filename}: {e}")

# --- Build Function (Example Usage) ---
def build_resume(filename="abdelfattah_zowail_resume.pdf"):
    """Creates and populates the resume using the ResumeBuilder class."""
    builder = ResumeBuilder(filename)

    # --- Header ---
    builder.add_name("Abdelfattah Zowail")
    builder.add_space(0.4 * cm)
    builder.add_contact_info([
        # Make email clickable using add_link within the list text
        f'Email: <a href="mailto:abdelftah.2004.com@gmail.com"><font color="{builder.link_color_hex}"><u>abdelftah.2004.com@gmail.com</u></font></a>',
        f'Phone: <a href="tel:+201067179860"><font color="{builder.link_color_hex}"><u>+201067179860</u></font></a>',
        "Location: Nasr City, Cairo, Egypt"
        # Add LinkedIn or GitHub link here if desired, e.g.:
        # f'LinkedIn: <a href="https://linkedin.com/in/yourprofile"><font color="{builder.link_color_hex}"><u>linkedin.com/in/yourprofile</u></font></a>'
    ])
    # Note: add_contact_info adds space after the block automatically now.
    # builder.add_space(builder.SPACE_MEDIUM) # Remove this if using updated add_contact_info
    builder.add_divider()

    # --- Work Experience ---
    builder.add_section_header("WORK EXPERIENCE")
    builder.add_title_with_date("Freelancer", "Feb 2023 - Present") # Assuming still active
    builder.add_paragraph("Flutter Mobile Developer | May 2023 - Present", italic=True, space_after=builder.SPACE_VSMALL)
    builder.add_paragraph("Android App Developer (Java) | Feb 2023 - May 2023", italic=True, space_after=builder.SPACE_SMALL)
    # Add bullet points describing responsibilities/achievements if needed
    # builder.add_bullet_point("Developed feature X resulting in Y improvement.")
    builder.add_space(builder.SPACE_MEDIUM) # Space before next section header

    # --- Education ---
    builder.add_section_header("EDUCATION")
    builder.add_title_with_date("Higher Institute for Computer Sciences and Information Systems", "2022 - 2026 (Expected)")
    builder.add_paragraph("Major: Computer Science", italic=True, space_after=builder.SPACE_SMALL)
    # builder.add_paragraph("Relevant Coursework: Data Structures, Algorithms, Database Systems", italic=False, indent=True) # Example
    builder.add_space(builder.SPACE_MEDIUM)

    # --- Projects ---
    builder.add_section_header("PROJECTS")

    # Saaffir App
    builder.add_title_with_date("Saaffir - Android/iOS App", "May 2023 - Mar 2025")
    builder.add_bullet_point("Led full-stack development (Flutter/Dart frontend, Firebase backend/database).")
    builder.add_bullet_point("Implemented server functions, deep linking, iOS compilation, and deployment to Play Store & App Store.")
    # Use add_link for the website, indented like a bullet point
    builder.add_link("Saaffir App", "https://Saaffir.com", prefix="■ Visit: ", indent=True, space_after=builder.SPACE_VSMALL)
    builder.add_space(builder.SPACE_MEDIUM) # Space between projects

    # ShortFormFunnels
    builder.add_title_with_date("ShortFormFunnels - Landing Page", "Feb 2024")
    builder.add_bullet_point("Developed a professional, modern landing page using React (with limited prior experience).")
    builder.add_bullet_point("Handled UI/UX design integration and basic 3D elements using Three.js.")
    builder.add_link("ShortFormFunnels.com", "https://ShortFormFunnels.com", prefix="■ Visit: ", indent=True, space_after=builder.SPACE_VSMALL)
    builder.add_space(builder.SPACE_MEDIUM)

    # Python Micro Projects
    builder.add_title_with_date("Python Micro-Projects", "") # No date range needed
    builder.add_link("github.com", "https://github.com/AbdelftahZowail/resume_builder", prefix="■ Resume Builder ", indent=True)
    builder.add_link("github.com", "https://github.com/AbdelftahZowail/youtube_leads_categorization", prefix="■ YouTube Leads Categorization ", indent=True)
    builder.add_link("github.com", "https://github.com/AbdelftahZowail/mp4_segment_downlaoder", prefix="■ MP4 Segment Downloader ", indent=True)
    builder.add_link("github.com", "https://github.com/AbdelftahZowail/arabic_english_switcher", prefix="■ Arabic/English Text Switcher ", indent=True)
    builder.add_space(builder.SPACE_MEDIUM)

    # JS Micro Projects
    builder.add_title_with_date("JavaScript Chrome Extension Micro-Projects", "")
    builder.add_link("github.com", "https://github.com/AbdelftahZowail/youtube_lead_getter", prefix="■ YouTube Leads Getter ", indent=True)
    builder.add_link("github.com", "https://github.com/AbdelftahZowail/lookup_lead", prefix="■ Lookup Lead Information ", indent=True)
    builder.add_link("github.com", "https://github.com/AbdelftahZowail/better_ig_videoplayer", prefix="■ Better Instagram Video Player ", indent=True)
    builder.add_link("github.com", "https://github.com/AbdelftahZowail/website_editor", prefix="■ Simple Webpage Interceptor/Editor ", indent=True)

    # --- Skills Section ---
    # Force skills to start on a new page if there isn't much space left
    builder.add_space_to_next_page()
    builder.add_section_header("SKILLS, TECHNOLOGIES & LANGUAGES")
    builder.add_space(builder.SPACE_SMALL) # Little space before first skill

    skills_data = [
        ("Dart / Flutter", 90),
        ("Firebase Suite", 90),
        ("Java (Android)", 75),
        ("Python", 60),
        ("JavaScript (React)", 50),
    ]
    for i, (name, perc) in enumerate(skills_data):
        builder.add_skill(name, perc)
        # Add space between skills, but not after the last one
        if i < len(skills_data) - 1:
            builder.add_space(builder.SPACE_LARGE / 2) # Smaller space between skills

    builder.add_space(builder.SPACE_LARGE) # Space after skills list before tech/lang

    # Use add_tech_language_item which adds bullets automatically via text
    builder.add_tech_language_item(
        "<b>AI Tools</b> Gemini, ChatGPT, GitHub Copilot"
    )
    builder.add_tech_language_item(
        "<b>Tools & Platforms:</b> IntelliJ IDEA, VS Code, Git"
    )
    builder.add_tech_language_item(
        "<b>Languages:</b> Arabic; English"
    )

    # --- Finalize ---
    builder.save()


# --- Run the Build Process ---
if __name__ == "__main__":
    build_resume()