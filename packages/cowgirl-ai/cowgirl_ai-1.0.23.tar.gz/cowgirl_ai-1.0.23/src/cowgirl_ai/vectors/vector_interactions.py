# https://platform.openai.com/docs/assistants/tools/file-search
from src.cowgirl_ai.client import Client
from src.cowgirl_ai.error_handler import error_handler
from openai import OpenAI
import logging
import time 

logging.basicConfig(level=logging.INFO, datefmt="%Y-%m-%d", format="%(levelname)s - %(asctime)s - %(message)s")


class VectorInteractions(Client): 
    """
    Vector Interactions Class
    -------------------------

    A vector store wrapper for the open ai api storage features.
    Part of this was driven by the fact that the vector tab in storage doesn't load at all. 
    In order to validate / interact with open ai api vector stores, I needed to create an app interface.
    The second problem was the API request to vector_stores via LIST was cumbersome. 
    
    This class takes advantage of 'limit' and 'desc' - two attributes that the vector stores 
    list and retrieval properties use. This way, we can interface with one vector at a time (to 
    automate uploading and downloading files from open ai and vector).
    """

    def __init__(self, vector_name=None):
        super().__init__()
        self.vector_name = vector_name

    @error_handler
    def get_latest_vector_id(self):
        """ 
        Gets the most recently created vector store. However, if class attribute 
        self.vector_name is provided, uses that instead. 

        Returns a dictionary with key-value pair containing latest id / name
        This way a vector_id can be accessed by the name it was created with. 
        """

        vector_stores = self.client.beta.vector_stores.list(limit=1, order="desc")
        
        vector_dict = {}
        for vector in vector_stores.data: 
            vector_id = vector.id 

            if self.vector_name is None: 
                vector_name = vector.name 
                vector_dict[vector_name] = vector_id
            else:
                vector_dict[self.vector_name] = vector_id
        return vector_dict 
    
    @error_handler
    def check_if_vector_store_exists(self):
        """
        Check If Vector Store Exists
        ----------------------------
        Uses the get_latest_vector_id method to (returns the latest created, or gets the id of provided name)
        make a request to vector stores using retrieve/vectorID. 
        
        Compare the provided class attribute vector_name against the vector name result from the API request
        to validate if the vector store name is accurate. If the response name doesn't match the class attribute vector_name, fail. 
        Otherwise vector store exists

        Returns
        -------
            boolean: TRUE if store exists, FALSE if store does not exist
        """

        success = True     # Initialize boolean condition

        # Get ID attributed to class attribute vector_name
        vector_store_dict = self.get_latest_vector_id()
        vector_id = vector_store_dict.get(f'{self.vector_name}')
        response = self.client.beta.vector_stores.retrieve(vector_store_id=vector_id)

        # Check logic
        if response.name != self.vector_name:
            success = False
            logging.info(f"Vector'{self.vector_name}' is not current. Current vector: '{response.name}' ")
        else:
            logging.info(f"Vector store {self.vector_name} is current. {response.name}")
        return success
    
    @error_handler
    def create_vector(self):
        """
        Creates a new vector store. 
        Returns a bool if created successfully, otherwise returns False. 
        """
        success = True
        if self.check_if_vector_store_exists() == False:
            command = input(f'Vector store does not exist, would you like to create: {self.vector_name} (y/N) ?')
            if command == "y":
                logging.info(f"Creating {self.vector_name}")
                self.client.beta.vector_stores.create(name=self.vector_name)
                logging.info(f"Vector Store {self.vector_name} created")
                success = True
            else: 
                logging.info(f"Ok. {self.vector_name} not created.")
        return success

    @error_handler
    def upload_files(self, file_paths=None):
        """
        Upload Files from file path to vector store 
        
        file_paths = ["/Users/teraearlywine/Cowgirl-AI/file-management/setup.py", \
            "/Users/teraearlywine/Cowgirl-AI/file-management/requirements.txt"]
        """
        if self.check_if_vector_store_exists() == False:
            self.create_vector()

        vector_store_dict = self.get_latest_vector_id()
        vector_id = vector_store_dict.get(f'{self.vector_name}')
        if file_paths is not None:
            logging.info(f"Files to upload: {len(file_paths)}")
            file_streams = [open(path, "rb") for path in file_paths]
            file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_id, files=file_streams
            )
            logging.info(f"Status: {file_batch.status}")
            logging.info(f"File counts: {file_batch.file_counts}")
            return True
        else: 
            logging.info(f"No file object paths provided, please add.")
            return False

    @error_handler 
    def search_vectors(self):
        """
        Returns a list of 5 vector ids. 

        Usage:: 

            >>> vector_interactions = VectorInteractions()
            >>> vector_interactions.search_vectors()
        """

        vector_dict = self.get_latest_vector_id()
        vector_id = vector_dict.get(f'{self.vector_name}')

        counter=0
        vector_ids = []
        while counter <= 5: # Setting arbitrary limit to reach (no more than 5 vectors)
            response = self.client.beta.vector_stores.list(after=vector_id, limit=1, order="desc")
            result = response.data 
            id = [v.id for v in result]
            if not id:
                
                break       

            for vector in response.data: 
                next_vector_id = vector.id
                vector_ids.append(next_vector_id)
                vector_id = next_vector_id    # Update the cursor for the next iteration
                counter += 1

        return vector_ids

if __name__=="__main__":
    VectorInteractions()

    