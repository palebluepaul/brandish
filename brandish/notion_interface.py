from notion_client import Client
import logging
from datetime import datetime

class NotionHandler(logging.Handler):
    """
    Custom logging handler that logs messages to Notion.
    """

    def __init__(self, notion_interface):
        """
        Initializes a new NotionHandler instance with the specified NotionInterface.
        """
        super().__init__()
        self.notion_interface = notion_interface

        # Construct the name of the log page
        log_page_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Log"

        # Get the log page if it exists
        results = self.notion_interface.notion.databases.query(
            **{
                "database_id": self.notion_interface.database_id,
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
                    "database_id": self.notion_interface.database_id
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
            self.log_page = self.notion_interface.notion.pages.create(**new_page)

    def emit(self, record):
        """
        Logs the specified logging record to Notion.
        """
        #self.notion_interface.log(record.levelno, record.getMessage())

        """
        Appends the message formatted with a timestamp and the correct severity level to the log page.
        """

        # Ignore log messages from the httpx library
        if record.name.startswith("httpx"):
            return
        
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Convert the logging level to a string
        level_name = logging.getLevelName(record.levelno)

        # Create the log message
        log_message = f"[{level_name.upper()}] {timestamp}: {record.getMessage()}"

        # Retrieve the child blocks of the log page
        child_blocks = self.notion_interface.notion.blocks.children.list(self.log_page["id"])["results"]

        if child_blocks:
            # If there's at least one child block, append the log message to its content
            log_block = child_blocks[0]

            new_content = log_block["paragraph"]["rich_text"][0]["text"]["content"] + "\n" + log_message

            # Update the log block with the new content
            self.notion_interface.notion.blocks.update(
                log_block["id"],
                paragraph={
                    "rich_text": [
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
            self.notion_interface.notion.blocks.children.append(
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


    def retrieve_briefs(self):
        """
        Function to retrieve unprocessed briefs
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

        return results

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
                "Tags": {
                        "multi_select": [
                            {
                                "name": "Report"
                            }
                        ]
                    }
            }
        }
        self.notion.pages.create(**new_page)


    def retrieve_agent_configurations(self):
        """
        Function to retrieve agent configurations from Notion.
        """
        
        # TODO: Implement your processing logic here


