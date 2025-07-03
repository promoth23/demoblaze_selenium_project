from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Setup
doc = SimpleDocTemplate("Demoblaze_Test_Strategy.pdf", pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
Story = []

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CustomHeading1", fontSize=14, leading=16, spaceAfter=10, spaceBefore=10))
styles.add(ParagraphStyle(name="CustomBody", fontSize=10.5, leading=14))

def add_section(title, body):
    Story.append(Paragraph(title, styles["CustomHeading1"]))
    Story.append(Paragraph(body.strip().replace("\n", "<br/>"), styles["CustomBody"]))
    Story.append(Spacer(1, 12))

def add_table(data, col_widths=None):
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    Story.append(table)
    Story.append(Spacer(1, 12))

# 1. Testing Levels Covered
add_section("1. Testing Levels Covered", """
- Unit Testing: Done at the function/method level. (e.g., login() or add_samsung_to_cart() methods)
- Functional Testing: Each feature tested for expected behavior (e.g., login, cart addition)
- Smoke Testing: Used @pytest.mark.smoke to verify critical paths like login and add-to-cart
- Regression Testing: Used @pytest.mark.regression to ensure new features don’t break old ones
""")

add_table([
    ["Level", "Description"],
    ["Unit Testing", "Function-level validation like login() or add_samsung_to_cart()"],
    ["Functional Testing", "Validates features like login or cart addition per requirements"],
    ["Smoke Testing", "Uses @pytest.mark.smoke to confirm core flows like login/cart work"],
    ["Regression Testing", "Ensures existing flows are stable with new changes using markers"]
], [140, 340])

# 2. Test Structure
add_section("2. Test Structure", "")
add_table([
    ["Layer", "Purpose"],
    ["tests/", "Contains all test cases (e.g., test_login.py, test_login_and_cart.py)"],
    ["pages/", "Page Object Model classes like LoginPage, CartPage"],
    ["utils/", "Helpers like take_screenshot(), popup handlers, Excel logging, logger"]
], [100, 380])

# 3. Test Design Approach
add_section("3. Test Design Approach", """
- Page Object Model (POM): Each web page is a class with methods for user actions and locators
- Modular Code: Reusable actions like login(), add_to_cart() etc., for test maintainability
- Utility Helpers: Abstracted logic for screenshots, logging, alerts, and Excel reporting
""")

# 4. Assertion Strategy
add_section("4. Assertion Strategy", "")
add_table([
    ["Test Case", "Assertion Used"],
    ["test_login.py", 'assert "Welcome" not in page_source'],
    ["test_cart_addition()", 'assert "Samsung galaxy s6" in page_source'],
    ["test_product_price_assertion()", 'assert "$360" in page_source']
], [200, 280])

# 5. Test Reporting
add_section("5. Test Reporting", """
- HTML Report: Generated using pytest-html with:
    pytest.main(["--html=reports/test_cart_report.html", "--self-contained-html"])

- Excel Report: Custom Excel log written via openpyxl to test_results.xlsx
""")

# 6. Reusability and Maintainability
add_section("6. Reusability and Maintainability", """
- Page classes like HomePage and CartPage can be extended easily
- Utilities like take_screenshot(), log_to_excel(), handle_popup() allow reuse across tests
""")

# 7. Error Handling Strategy
add_section("7. Error Handling Strategy", """
- All test logic is wrapped in try...except
- Failures trigger screenshot and Excel logging
- logger captures detailed tracebacks
- Popup alerts notify on UI about execution status
""")

# 8. Summary Table
add_section("8. Test Strategy Summary", "")
add_table([
    ["Feature", "Description"],
    ["Framework Type", "Selenium with PyTest using Page Object Model"],
    ["Execution Tools", "PyTest CLI, HTML Report, Excel Log"],
    ["Assertion Style", "Standard PyTest assert statements"],
    ["Error Recovery", "Try-Except + Alerts + Screenshots + Logging"],
    ["Modular Utilities", "Screenshot, Logger, Excel Log, Popups"],
    ["Test Coverage", "Login, Cart Addition, Price Assertion, Alerts"],
    ["Markers Used", "@pytest.mark.smoke, @pytest.mark.regression"]
], [160, 320])

# Final build
doc.build(Story)
print("✅ PDF generated: Demoblaze_Test_Strategy.pdf")
