from notion_client import Client
import logging
from datetime import datetime

class NotionInterface:
    """
    Class to interface with Notion API using notion-client.
    """


    def __init__(self, auth_token, database_id):
        """
        Initializes a new NotionInterface instance with the specified authentication token and database ID.
        """
        # Initialize a new Notion client with the provided authentication token
        self.notion = Client(auth=auth_token)
        # Set the database ID
        self.database_id = database_id

        # Construct the name of the log page
        log_page_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Log"

        # Get the log page if it exists
        results = self.notion.databases.query(
            **{
                "database_id": self.database_id,
                "filter": {
                    "property": "Name",
                    "title": {
                        "equals": log_page_name
                    }
                }
            }
        ).get("results")
        self.log_page = results[0] if results else None

        # If the log page doesn't exist, create it
        if self.log_page is None:
            new_page = {
                "parent": {
                    "database_id": self.database_id
                },
                "properties": {
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": log_page_name
                                }
                            }
                        ]
                    },
                    "Tags": {
                        "multi_select": [
                            {
                                "name": "Log"
                            }
                        ]
                    }
                }
            }
            self.log_page = self.notion.pages.create(**new_page)

    def log(self, level, message):
        """
        Appends the message formatted with a timestamp and the correct severity level to the log page.
        """
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Convert the logging level to a string
        level_name = logging.getLevelName(level)

        # Create the log message
        log_message = f"[{level_name.upper()}] {timestamp}: {message}"

        # Retrieve the child blocks of the log page
        child_blocks = self.notion.blocks.children.list(self.log_page["id"])["results"]

        if child_blocks:
            # If there's at least one child block, append the log message to its content
            log_block = child_blocks[0]
            new_content = log_block["paragraph"]["text"][0]["text"]["content"] + "\n" + log_message

            # Update the log block with the new content
            self.notion.blocks.update(
                log_block["id"],
                paragraph={
                    "text": [
                        {
                            "type": "text",
                            "text": {
                                "content": new_content
                            }
                        }
                    ]
                }
            )
        else:
            # If there are no child blocks, create a new one with the log message
            self.notion.blocks.children.append(
                self.log_page["id"],
                children=[
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": log_message
                                    }
                                }
                            ]
                        }
                    }
                ]
            )




    def monitor_notion_folder(self):
        """
        Function to monitor a Notion folder for new documents.
        """
        results = self.notion.databases.query(
            **{
                "database_id": self.database_id,
                "filter": {
                    "property": "Status",
                    "status": {
                        "equals": "Pending Brief"
                    }
                }
            }
        ).get("results")

        for result in results:
            self.create_report_page(result)

    def create_report_page(self, brief):
        """
        Function to create a new report page for the specified brief.
        """
        # Construct the name of the new page
        report_name = brief["properties"]["Name"]["title"][0]["text"]["content"] + " Report"

        # Create a new page in the database
        new_page = {
            "parent": {
                "database_id": self.database_id
            },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": report_name
                            }
                        }
                    ]
                },
                "Status": {
                    "status": {
                        "name": "Done"
                    }
                },
                # Add other properties here
            }
        }
        self.notion.pages.create(**new_page)


    def retrieve_agent_configurations(self):
        """
        Function to retrieve agent configurations from Notion.
        """
        
        # TODO: Implement your processing logic here


