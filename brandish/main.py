"""
Main entry point for the Brandish application.
This script orchestrates the entire process by calling the appropriate functions from the other modules.
"""

from . import notion_interface
from . import agent_manager
from . import data_persistence
from . import output_generator
from . import log_manager

def main():
    """
    Main function to orchestrate the Brandish application process.
    """
    # Monitor Notion folder for new documents
    notion_interface.monitor_notion_folder()

    # Retrieve new brief and agent configurations from Notion
    notion_interface.retrieve_notion_brief()
    notion_interface.retrieve_agent_configurations()

    # Instantiate and invoke agents
    agent_manager.instantiate_agents()
    agent_manager.invoke_agents()

    # Persist data
    data_persistence.persist_data()

    # Generate output briefs from agents
    output_generator.generate_output()

    # Write output and logs back to Notion
    notion_interface.write_output_to_notion()
    log_manager.write_logs_to_notion()

if __name__ == "__main__":
    main()
