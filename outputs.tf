output "ledger_id" {
  value = azurerm_confidential_ledger.this.id
}

output "identity_service_endpoint" {
  value = azurerm_confidential_ledger.this.identity_service_endpoint
}

output "ledger_ednpoint" {
  value = azurerm_confidential_ledger.this.ledger_endpoint
}
