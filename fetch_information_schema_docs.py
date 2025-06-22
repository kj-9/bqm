#!/usr/bin/env python3
"""
Script to fetch BigQuery INFORMATION_SCHEMA documentation from Google Cloud docs
and save it as markdown using only standard library.
"""

import html
import re
import sys
import time
import urllib.parse
import urllib.request


def fetch_page(url):
    """Fetch the webpage content."""
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode("utf-8")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_text_between_tags(html_content, tag, class_name=None):
    """Extract text content between HTML tags."""
    if class_name:
        pattern = f'<{tag}[^>]*class="[^"]*{class_name}[^"]*"[^>]*>(.*?)</{tag}>'
    else:
        pattern = f"<{tag}[^>]*>(.*?)</{tag}>"

    matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
    return matches


def clean_html_text(text):
    """Remove HTML tags and decode HTML entities."""
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Decode HTML entities
    text = html.unescape(text)
    # Clean up whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_table_links(html_content):
    """Extract links to individual INFORMATION_SCHEMA table documentation pages."""
    links = []
    base_url = "https://cloud.google.com"

    # Look for links that contain "information-schema-" in the href
    link_pattern = r'<a[^>]*href="([^"]*information-schema-[^"]*)"[^>]*>(.*?)</a>'

    for match in re.finditer(link_pattern, html_content, re.DOTALL | re.IGNORECASE):
        href = match.group(1)
        link_text = clean_html_text(match.group(2))

        # Construct full URL if it's a relative path
        if href.startswith("/"):
            full_url = base_url + href
        else:
            full_url = href

        # Skip duplicate links and ensure it's actually a table documentation page
        if (
            full_url not in [link["url"] for link in links]
            and "information-schema-" in href
        ):
            links.append(
                {
                    "url": full_url,
                    "text": link_text,
                    "table_name": extract_table_name_from_url(href),
                }
            )

    return links


def extract_table_name_from_url(url):
    """Extract the table name from the documentation URL."""
    # Remove the base path and extract the table name
    url = url.replace("/bigquery/docs/information-schema-", "")
    # Convert hyphens to underscores and uppercase
    table_name = url.replace("-", "_").upper()
    return table_name


def extract_table_definition(html_content):
    """Extract table schema definition from individual table documentation page."""
    schema_info = {"description": "", "columns": [], "example_queries": []}

    # Look for table schema in various formats
    # Try to find schema table first
    tables = extract_tables_from_html(html_content)

    # Look for the schema table (usually has Column name, Data type, Description)
    for table in tables:
        if (
            "Column name" in table
            or "Field name" in table
            or "column_name" in table.lower()
        ):
            schema_info["schema_table"] = table
            break

    # Extract description from the page
    main_content_patterns = [
        r'<div[^>]*class="[^"]*devsite-article-body[^"]*"[^>]*>(.*?)</div>',
        r"<main[^>]*>(.*?)</main>",
        r"<article[^>]*>(.*?)</article>",
    ]

    main_html = ""
    for pattern in main_content_patterns:
        matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
        if matches:
            main_html = matches[0]
            break

    if main_html:
        # Extract first paragraph as description
        paragraph_pattern = r"<p[^>]*>(.*?)</p>"
        paragraphs = re.findall(paragraph_pattern, main_html, re.DOTALL | re.IGNORECASE)
        if paragraphs:
            schema_info["description"] = clean_html_text(paragraphs[0])

        # Look for example queries
        code_pattern = r"<pre[^>]*><code[^>]*>(.*?)</code></pre>"
        code_blocks = re.findall(code_pattern, main_html, re.DOTALL | re.IGNORECASE)
        for code in code_blocks:
            clean_code = clean_html_text(code)
            if (
                "SELECT" in clean_code.upper()
                and "INFORMATION_SCHEMA" in clean_code.upper()
            ):
                schema_info["example_queries"].append(clean_code)

    return schema_info


def extract_tables_from_html(html_content):
    """Extract table data from HTML and convert to markdown."""
    tables = []
    table_pattern = r"<table[^>]*>(.*?)</table>"

    for table_match in re.finditer(
        table_pattern, html_content, re.DOTALL | re.IGNORECASE
    ):
        table_html = table_match.group(1)

        # Extract rows
        row_pattern = r"<tr[^>]*>(.*?)</tr>"
        rows = []

        for row_match in re.finditer(
            row_pattern, table_html, re.DOTALL | re.IGNORECASE
        ):
            row_html = row_match.group(1)

            # Extract cells (th or td)
            cell_pattern = r"<t[hd][^>]*>(.*?)</t[hd]>"
            cells = []

            for cell_match in re.finditer(
                cell_pattern, row_html, re.DOTALL | re.IGNORECASE
            ):
                cell_text = clean_html_text(cell_match.group(1))
                cells.append(cell_text)

            if cells:
                rows.append(cells)

        if rows:
            # Convert to markdown table
            markdown_table = []
            if rows:
                # Header row
                markdown_table.append("| " + " | ".join(rows[0]) + " |")
                # Separator
                markdown_table.append("|" + "|".join([" --- " for _ in rows[0]]) + "|")
                # Data rows
                for row in rows[1:]:
                    if len(row) == len(rows[0]):  # Ensure consistent column count
                        markdown_table.append("| " + " | ".join(row) + " |")

            tables.append("\n".join(markdown_table))

    return tables


def extract_headers_and_content(html_content):
    """Extract headers and relevant content."""
    content = []

    # Look for main content sections
    main_content_patterns = [
        r'<div[^>]*class="[^"]*devsite-article-body[^"]*"[^>]*>(.*?)</div>',
        r"<main[^>]*>(.*?)</main>",
        r"<article[^>]*>(.*?)</article>",
    ]

    main_html = ""
    for pattern in main_content_patterns:
        matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
        if matches:
            main_html = matches[0]
            break

    if not main_html:
        print("Could not find main content area, using full page")
        main_html = html_content

    # Extract headers (h1-h6)
    header_pattern = r"<h([1-6])[^>]*>(.*?)</h[1-6]>"

    for match in re.finditer(header_pattern, main_html, re.DOTALL | re.IGNORECASE):
        level = int(match.group(1))
        header_text = clean_html_text(match.group(2))

        # Filter for relevant headers
        if any(
            keyword in header_text.upper()
            for keyword in ["TABLE", "VIEW", "SCHEMA", "INFORMATION"]
        ):
            content.append(f"{'#' * level} {header_text}\n")

    # Extract paragraphs near relevant sections
    paragraph_pattern = r"<p[^>]*>(.*?)</p>"
    for match in re.finditer(paragraph_pattern, main_html, re.DOTALL | re.IGNORECASE):
        para_text = clean_html_text(match.group(1))
        if (
            any(
                keyword in para_text.upper()
                for keyword in ["INFORMATION_SCHEMA", "TABLE", "VIEW"]
            )
            and len(para_text) > 20
        ):
            content.append(f"{para_text}\n")

    return content


def main():
    url = "https://cloud.google.com/bigquery/docs/information-schema-intro"

    print(f"Fetching BigQuery INFORMATION_SCHEMA documentation from {url}")

    html_content = fetch_page(url)
    if not html_content:
        sys.exit(1)

    # Extract content from main page
    content_lines = extract_headers_and_content(html_content)
    tables = extract_tables_from_html(html_content)

    # Extract links to individual table documentation pages
    print("Extracting links to individual table documentation pages...")
    table_links = extract_table_links(html_content)
    print(f"Found {len(table_links)} table documentation links")

    # Fetch individual table definitions
    table_definitions = {}
    print("Fetching individual table definitions...")

    for i, link in enumerate(table_links, 1):
        print(f"Fetching {i}/{len(table_links)}: {link['table_name']}")

        table_html = fetch_page(link["url"])
        if table_html:
            table_def = extract_table_definition(table_html)
            table_definitions[link["table_name"]] = {
                "url": link["url"],
                "definition": table_def,
            }

        # Add a small delay to be respectful to the server
        time.sleep(0.5)

    # Write to markdown file
    output_file = "bigquery_information_schema.md"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# BigQuery INFORMATION_SCHEMA Documentation\n\n")
        f.write(f"Source: {url}\n")
        f.write("Generated automatically using pure Python\n\n")

        # Write extracted content from main page
        for line in content_lines:
            f.write(line + "\n")

        # Write main tables from index page
        if tables:
            f.write("\n## Overview Tables\n\n")
            for i, table in enumerate(tables):
                f.write(f"### Table {i + 1}\n\n")
                f.write(table + "\n\n")

        # Write individual table definitions
        if table_definitions:
            f.write("\n## Table Definitions\n\n")

            for table_name, info in sorted(table_definitions.items()):
                f.write(f"### {table_name}\n\n")
                f.write(f"**Source:** {info['url']}\n\n")

                definition = info["definition"]

                if definition["description"]:
                    f.write(f"**Description:** {definition['description']}\n\n")

                if "schema_table" in definition:
                    f.write("**Schema:**\n\n")
                    f.write(definition["schema_table"] + "\n\n")

                if definition["example_queries"]:
                    f.write("**Example Queries:**\n\n")
                    for query in definition["example_queries"]:
                        f.write("```sql\n")
                        f.write(query + "\n")
                        f.write("```\n\n")

                f.write("---\n\n")

    print(f"Documentation saved to {output_file}")
    print(f"Content sections: {len(content_lines)}")
    print(f"Overview tables: {len(tables)}")
    print(f"Individual table definitions: {len(table_definitions)}")


if __name__ == "__main__":
    main()
