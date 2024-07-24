from cowgirl_ai.client import Client
from cowgirl_ai.error_handler import error_handler

import logging

logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d", format="%(levelname)s - %(asctime)s - %(message)s")

class AssistantInteractions(Client):
    """
    Assistant Interactions 
    ----------------------

    Class for defining OpenAI assistant interaction methods
    """
    def __init__(self, assistant_name=None):
        super().__init__()
        self.assistant_name = assistant_name
        self.assistant_dict = {}
    
    @error_handler
    def get_assistants(self):
        """
        Get Assistants
        --------------

        Returns 1 assistant at a time.
        However, if the assistant name is provided and the variable is not none, 
        returns that assistant instead.
        """

        response = self.client.beta.assistants.list(order="desc")
        for assistant in response.data: 
            yield from assistant
    
    @error_handler
    def create_assistant_dict(self):
        """
        Create Assistant Dictionary
        ---------------------------

        Method that updates an empty dictionary 
        with key-value pairs containing current assistant names and their id's. 
        
        Usage::

            >>> assistant_interactions = AssistantInteractions()
            >>> assistant_interactions.create_assistant_dict()
            >>> print(assistant_interactions.assistant_dict)
        """
        for assistant in self.get_assistants():
            self.assistant_dict[assistant.name] = assistant.id

    @error_handler
    def update_assistant_to_use_vector(self, vector_id):
        """
        Get the id from the latest created vector store 
        using the newly created vector store name and upload to 
        assistant.

        Usage::
            >>> interactions = Interactions(vector_name='Development -
              Data Ingestion Vector', assistant_name='Data Engineer')
            >>> interactions.update_assistant_to_use_vector() 

        """

        if self.assistant_name is None:
            logging.info('Updating latest created assistant to reference vector stores')
        else:
            logging.info(f'Updating {self.assistant_name} to reference vector store')

        success = False
        try:
            # Create a dictionary with current assistant names & id
            self.create_assistant_dict()
            assistant_id = self.assistant_dict.get(f'{self.assistant_name}')

            self.client.beta.assistants.update(
                assistant_id=assistant_id,
                tool_resources={"file_search": {"vector_store_ids": [vector_id]}},
            )
            logging.info(f"Assistant {assistant_id} updated with {vector_id}")
            success = True
        except Exception as err: 
            logging.info(f'Unable to update assistant with vector, see issue: \n\n{err}')
        return success


if __name__=="__main__":
    AssistantInteractions()
