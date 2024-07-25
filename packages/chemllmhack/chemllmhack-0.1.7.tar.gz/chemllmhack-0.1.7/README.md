# QDX ChemLLMHack SDK

Welcome to the QDX Computational Chemistry and Large Language Model (LLM) Hackathon! This SDK is tailored specifically for the hackathon and is designed to seamlessly integrate with the most advanced RUSH's computational cloud platform (https://rush.cloud). It enables the community to effortlessly develop and apply cutting-edge LLM and Artificial Intelligence (AI) technologies in computational chemistry.

## Installation

To install the QDX ChemLLMHack SDK, simply run the following command:

```bash
pip install chemllmhack
```

## Features

- Get help information about the Rex language.
Retrieve specific expressions used in RUSH modules from Rex Database.


- Download the paper dataset and Chroma vector database. The Paper Dataset comprises a comprehensive collection of scientific papers sourced from open-access databases including arXiv, bioRxiv, chemRxiv, and medRxiv. Below are the statistics for the dataset:

    | Tool    | Number of Papers |
    |---------|:----------------:|
    | MMseqs2 |       1000       |
    | PLIP    |       2000       |
    | Gina    |       3000       |
    | RDock   |       4000       |
    | Auto3d  |       5000       |


- Use MongoDB Atlas cloud vector database to retrieve vectors and query online.


- Submit your Rex expression to the RUSH platform.


- Retrieve the results and stats against benchmark of your submitted Rex expression.

## QDX Hackathon Setup Guide

### Prerequisites
Before you begin, make sure you have a Google account. You'll need this to register for the QDX Hackathon. You also need a OPENAI_API_KEY set up in your environment. You will be granted a RUSH token, make sure you set it up in your environment.
```bash
TENGU_TOKEN=<your-rush-token>
```

### Registration
Register for the QDX Hackathon [here](https://qdx-hackathon-registration-link.com).

### Getting Help Information for Rex Language
To get help information about the Rex language, use the following command:
```bash
chemllmhack --rex-help language
```

### Retrieving Specific Rex Expressions
To retrieve a specific Rex expression associated with a module, use the command below:
```bash
chemllmhack --rex-help expression -rex <module_name>
```
Replace <module_name> with the actual name of the module you're interested in.
or you could use python language to query the rex expression:
```python
from chemllmhack import get_rex_expression
get_rex_expression('module_name')
```

### Querying with natural language
The SDK allows a LLM friendly way to query, to query with natural language, use the following command:
```python
from chemllmhack import query
query('your-natural-language-query')
```

### Submitting Rex Expressions to RUSH
To submit a Rex expression to the RUSH platform, use the following command:
```python
from chemllmhack import submit_rex_expression
submit_rex_expression('your-rex-expression')
```

### Downloading Datasets
you can download the necessary datasets:

- Paper Dataset
- Chroma Vector Database


#### Configuring Google Cloud CLI
To interact with Cloud Storage using the Google Cloud CLI, follow these steps:

1. Run the following command to authenticate:
   ```bash
   sudo gcloud auth login
   ```
   or
   ```bash
   sudo gcloud auth application-default login
   ```
2. Provide the path to your credentials file. Typically, it is located at:
   ```
   /Users/<your_user_name>/.config/gcloud/application_default_credentials.json
   ```

Replace `<your_user_name>` with your actual username on your system. Make sure you grant appropriate permissions to the json file.
For more information, refer to the [Google Cloud CLI documentation](https://cloud.google.com/storage/docs/authentication?hl=en).

#### Downloading Datasets with the Command Line
Use the following command to initiate the download:
```bash
command-to-download-datasets
````

#### Downloading Datasets with functions
```python
from chemllmhack import download_vector_db
download_vector_db(credential_path='your-credential-path', destination_file_name='your-destination-file-name')
```

## Your Task
Build an AI experiment system with the provided paper database and RAG Database LLM and RUSH platform to beat the benchmark.

## Contributing
We welcome contributions from the community. If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Contact Information
For any questions or comments, please email bowen.zhang@qdx.co. Alternatively, you can open an issue in this repository's issue tracker.

## Acknowledgments
Thanks to everyone participating in the development and use of this SDK. We hope it serves you well in the QDX Hackathon.