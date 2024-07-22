# File Management

This project provides a Python-based solution for managing files and vector stores using the OpenAI API. It allows you to upload, delete, and manage files and vector stores, which are essential components for working with OpenAI's language models and other AI services.

# Features
2024-07-20 Features


### General recursive file search for specific directory
Recursively search a specified directory for files with a specified extension. Useful for seeing what will be uploaded automateically before performing the batch upload operation. 



```zsh

% cowgirl-ai search-files src .py 

```

Planned:

### Batch uploading files with recursive search for specific directory
Recursively search a specified directory for files with a specified extension. Requires a vector id to perform a batch upload to openai file storage. Command automatically sends files to vector store, useages vary depending on assistant and project goals.


```zsh

% cowgirl-ai batch-upload <vector_id> src .py 

```

------------

## Installation

1. Clone the repository:

```zsh
git clone https://github.com/your-username/file-management.git
```

2. Install required dependencies:
```zsh
pip install -r requirements.txt
```

3. Set your OpenAI API key as an environment variable:
```
export OPENAI_API_KEY=your_api_key_here
```

This README provides an overview of the project, its features, installation instructions, usage examples, contributing guidelines, and licensing information. 


