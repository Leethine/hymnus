from markupsafe import escape

def createTable(table_rows=[{}], header_filter=[], show_first_col=True):
  # Make sure we have at lease 2 columns to display
  header = []
  if len(header_filter) > 1 and len(table_rows) > 0:
    header = header_filter
  elif len(table_rows) > 0 and len(table_rows[0].keys()) > 1:
    header = table_rows[0].keys()
  else:
    err_msg = "Cannot generate table from the given input!!!"
    err_msg += f"\n\n{header_filter}\n{table_rows}"
    return err_msg

  # Check if header filter are correct
  for col in header:
    if not col in table_rows[0].keys():
      msg = f"'{escape(col)}' is not a valid header "
      msg += "(does not exist in provided table data)"
      return msg

  # Create first header
  html = "<table class=\"table\"><thead><tr><th scope=\"col\"></th>"
  # Add other headers
  for h in header[1:]:
    html += f'<th scope="col">{escape(h)}</th>'
  html += "</tr></thead><tbody>"

  # Create table content
  for row in table_rows:
    html += "<tr>"
    if show_first_col:
      # create first column
      html += f"<th scope=\"row\">{escape(row[header[0]])}</th>"
    else:
      html += "<th scope=\"row\"></th>"
    # create other columns
    for h in header[1:]:
      html += f"<td class=\"text-left\">{row[h]}</td>"
    html += "</tr>"

  html += "</tbody></table>"
  return html

def createPagination(page_number=1, total_pages=1, parent_url=""):
  if not str(page_number).isdigit():
    return f"Invalid page number: {page_number}"
  if not str(total_pages).isdigit():
    return f"Invalid total pages: {total_pages}"

  # page number as in array indexing
  i_pagenumber = int(page_number) - 1
  
  # generate html page list
  pagination_html = []
  if i_pagenumber >= 0 and i_pagenumber < total_pages:
    for i in range(int(total_pages)):
      pagination_html.append("<a class=\"w3-button w3-hover-black\"" \
                             + f"href=\"/{escape(parent_url)}/{str(i+1)}\">{str(i+1)}</a>")
    pagination_html[i_pagenumber] = "<a class=\"w3-button w3-black\"" \
                                  + f"href=\"#\">{page_number}</a>"
    return " ".join(pagination_html)
  else:
    return "Page out of range"

