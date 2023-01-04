provider "azurerm" {
  features {}
}

data "azurerm_client_config" "current" {}

locals {
  name        = "${var.deployment_name}-${var.location}"
  ad_app_name = "Some App"
}

resource "azurerm_resource_group" "this" {
  name     = "rg-${local.name}"
  location = var.location
}

resource "azurerm_confidential_ledger" "this" {
  name                = "acl-${local.name}"
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  ledger_type         = "Public"

  azuread_based_service_principal {
    principal_id     = data.azurerm_client_config.current.object_id
    tenant_id        = data.azurerm_client_config.current.tenant_id
    ledger_role_name = "Administrator"
  }
}
