# Shared Kernel

Shared Kernel is a lightweight, modular Python library designed to facilitate rapid development of microservices. It provides essential utilities for data manipulation, logging, configuration management, and database connectivity, making it an ideal foundation for building scalable and maintainable microservices.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Importing Modules](#importing-modules)
  - [Initializing Database Connection](#initializing-database-connection)


## Getting Started

### Prerequisites

- Python 3.6+
- Pip

### Installation

To install Shared Kernel, clone the repository and install it using pip:

   ```sh
   git clone https://bitbucket.org/Weavers/shared-kernel.git 
   cd shared-kernel pip install .
   ```

##### Step 1: Set Up Your Environment
First, ensure you have Python installed on your system. Then, set up a virtual environment for your project to manage dependencies cleanly. Open your terminal and navigate to your project directory:

```sh
cd path/to/shared-kernel
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

##### Step 2: Install Python build frontend.
Ensure you python's build frontend. installed in your environment. This is necessary for building the wheel package from **.toml** file. You can install them using pip:
```sh
pip install --upgrade build
```

##### Step 3: Build the Wheel Package
```sh
python -m build
```
This command will build a wheel distribution and also a source distribution. After running this command, you'll find the .whl and a tar file inside the dist/ directory within your project folder.


##### Step 4: Distribute the Wheel
Now that you have a .whl file, you can distribute it to others. Users can install your library using pip by pointing to the .whl file:

```sh
pip install dist/shared_kernel-0.1.0-py3-none-any.whl
```


## Usage

### Importing Modules

Import the required modules from Shared Kernel into your project:

```
from shared_kernel.logger import Logger
from shared_kernel.config import Config
from dotenv import find_dotenv


def main():
    logger = Logger(name="my_app")
    logger.configure_logger()

    # Specify the path to the .env file if it's not in the current directory
    config_manager = Config(env_path=find_dotenv())

    # Access environment variables
    api_key = config_manager.get("KEY", "default_api_key")

    # Example usage
    logger.logger.info("This is an info message.")
    logger.logger.error("This is an error message.")
    logger.logger.info(api_key)


if __name__ == "__main__":
    main()

```


### Initializing Database Connection

Use the `DB` class to initialize a database connection:

```
from shared_kernel.DB import DB

db_instance = DB("postgresql://user:password@localhost/dbname") 
engine, SessionLocal = db_instance.init_db_connection()

```




### Initializing NATS Connection

Use the `NATSClient` class to initialize a messaging connection:

```
from shared_kernel.messaging import NATSClient
import asyncio

def run():
  nats_instance = NATSClient("nats://localhost:4222") 
    await nc_interface.connect()

    async def message_callback(data):
        print(f"Received a message: {data}")

    await nc_interface.subscribe("example_subject", message_callback)
    await nc_interface.publish("example_subject", "Hello NATS!")
    
if __name__ == '__main__':
    asyncio.run(run())
```