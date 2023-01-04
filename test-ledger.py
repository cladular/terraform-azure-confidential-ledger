from azure.identity import DefaultAzureCredential
from azure.mgmt.confidentialledger import ConfidentialLedger as ConfidentialLedgerAPI
from azure.mgmt.confidentialledger.models import ConfidentialLedger
from azure.confidentialledger import ConfidentialLedgerClient
from azure.confidentialledger.certificate import ConfidentialLedgerCertificateClient

resource_group = "rg-confidentialledger-eastus"
ledger_name = "acl-confidentialledger-eastus"
subscription_id = "<azure-subscription-id>"

identity_url = "https://identity.confidential-ledger.core.azure.com"
ledger_url = "https://" + ledger_name + ".confidential-ledger.azure.com"

credential = DefaultAzureCredential()
confidential_ledger_mgmt = ConfidentialLedgerAPI(
    credential, subscription_id
)

properties = {
    "location": "eastus",
    "tags": {},
    "properties": {
        "ledgerType": "Public",
        "aadBasedSecurityPrincipals": [],
    },
}
ledger_properties = ConfidentialLedger(**properties)

print(f"{resource_group} / {ledger_name}")

myledger = confidential_ledger_mgmt.ledger.get(resource_group, ledger_name)

print("Ledger details:")
print(f"  Name: {myledger.name}")
print(f"  Location: {myledger.location}")
print(f"  ID: {myledger.id}")

identity_client = ConfidentialLedgerCertificateClient(identity_url)
network_identity = identity_client.get_ledger_identity(
     ledger_id=ledger_name
)

ledger_tls_cert_file_name = "ledgercert.pem"
with open(ledger_tls_cert_file_name, "w") as cert_file:
    cert_file.write(network_identity['ledgerTlsCertificate'])

ledger_client = ConfidentialLedgerClient(
     endpoint=ledger_url, 
     credential=credential,
     ledger_certificate_path=ledger_tls_cert_file_name
)

sample_entry = {"contents": "Hello world!"}
ledger_client.create_ledger_entry(entry=sample_entry)

latest_entry = ledger_client.get_current_ledger_entry()
print("Latest entry:")
print(f"  Transaction ID: {latest_entry['transactionId']}")
print(f"  Collection ID: {latest_entry['collectionId']}")
print(f"  Contents: {latest_entry['contents']}")
