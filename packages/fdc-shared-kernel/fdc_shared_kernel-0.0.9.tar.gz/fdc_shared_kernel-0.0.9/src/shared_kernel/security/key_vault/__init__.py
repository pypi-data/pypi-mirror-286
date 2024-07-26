from shared_kernel.interfaces import KeyVaultInterface
from shared_kernel.security.key_vault.aws_secret_manager import AWSSecretsManager
from shared_kernel.security.key_vault.azure_keyvault import AzureKeyVault


class KeyVaultManager:
    @staticmethod
    def create_key_vault(vault_type: str, config: dict) -> KeyVaultInterface:
        if vault_type == 'AZURE':
            return AzureKeyVault(config)
        elif vault_type == 'AWS':
            return AWSSecretsManager(config)
        else:
            raise ValueError(f"Unknown vault type: {vault_type}")
