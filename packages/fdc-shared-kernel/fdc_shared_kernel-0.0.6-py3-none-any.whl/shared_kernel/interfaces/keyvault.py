from abc import ABC, abstractmethod


class KeyVaultInterface(ABC):

    @abstractmethod
    def __init__(self, config: dict):
        """Initialize the key vault connection with the given configuration dictionary."""
        pass

    @abstractmethod
    def store_secret(self, name: str, secret: str) -> None:
        """Store a secret in the key vault."""
        pass

    @abstractmethod
    def retrieve_secret(self, name: str) -> str:
        """Retrieve a secret from the key vault."""
        pass

    @abstractmethod
    def delete_secret(self, name: str) -> None:
        """Delete a secret from the key vault."""
        pass

    @abstractmethod
    def list_secrets(self) -> list:
        """List all secrets in the key vault."""
        pass
