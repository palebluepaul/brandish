"""
Main entry point for the Brandish application.
This script orchestrates the entire process by calling the appropriate functions from the other modules.
"""

from brandish import agent_manager
from brandish import data_persistence
from brandish import output_generator
from brandish.notion_interface import NotionInterface
from brandish.notion_interface import NotionHandler
import os
import logging
import promptlayer
from llama_index import ListIndex, NotionPageReader
#from IPython.display import Markdown, display
import os


def main():
    """
    Main function to orchestrate the Brandish application process.
    """

    # Initialize a new NotionInterface instance with the specified authentication token and database ID
    notion_auth_token = os.environ.get("NOTION_AUTH_TOKEN")
    notion_database_id = os.environ.get("NOTION_BRANDISH_DATABASE_ID")
    notion_interface = NotionInterface(auth_token=notion_auth_token, database_id=notion_database_id)

    # Create a new Notion handler
    notion_handler = NotionHandler(notion_interface)

    # Create a new logger
    logger = logging.getLogger()

    # Set the logger's level to INFO
    logger.setLevel(logging.INFO)

    # Add the Notion handler to the logger
    logger.addHandler(notion_handler)

    # Log that the processing run has started
    logger.info("Started a processing run")

    # Monitor Notion folder for new documents
    briefs = notion_interface.retrieve_briefs()

    # Log the number of briefs retrieved
    logger.info(f"Retrieved {len(briefs)} briefs.")

    for brief in briefs:
        page_ids = [brief["id"]]
        documents = NotionPageReader(integration_token=notion_auth_token).load_data(page_ids=page_ids)

        # Retrieve agent configurations from Notion
        notion_interface.retrieve_agent_configurations(brief)

        # Instantiate and invoke agents
        agent_manager.instantiate_agents()
        response = agent_manager.invoke_agents(documents)

        # Persist data
        data_persistence.persist_data()

        # Generate output briefs from agents
        output_generator.generate_output()

        # Create report page in Notion
        notion_interface.create_report_page(brief, response)

    # Log that the processing run has completed
    logger.info("Completed a processing run")
   

if __name__ == "__main__":
    main()
