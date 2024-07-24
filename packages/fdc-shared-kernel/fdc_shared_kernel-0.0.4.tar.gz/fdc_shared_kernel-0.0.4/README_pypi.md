# FDC Shared Kernel

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
      pip install fdc-shared-kernel
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