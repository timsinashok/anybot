# from notion_client import Client

# # Initialize the Notion client
# notion = Client(auth="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")

# # Get a database or page
# response = notion.pages.query(page_id="c66d5236e8ea40df8af114f6d447ab48")
# print(response)

from notion_client import Client

# Initialize the Notion client
notion = Client(auth="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")

# Get the content of a page
page_id = "c66d5236e8ea40df8af114f6d447ab48"  # Ensure the page ID is in the correct format
response = notion.pages.retrieve(page_id=page_id)

# Print the response
print(response)