#!/bin/bash

# Zmienne konfiguracyjne
RESOURCE_GROUP="MojaGrupaZasobów"
VM_NAME="MojaUbuntuVM"
REGION="westeurope"
IMAGE="UbuntuLTS"
SIZE="Standard_B1s"
ADMIN_USERNAME="mojuser"
SSH_KEY_PATH="~/.ssh/id_rsa.pub"

# Krok 1: Logowanie do Azure CLI (opcjonalne, wymagane tylko jeśli nie jesteś zalogowany)
# az login

# Krok 2: Tworzenie grupy zasobów (jeśli nie istnieje)
az group create --name $RESOURCE_GROUP --location $REGION

# Krok 3: Tworzenie maszyny wirtualnej
az vm create \
  --resource-group $RESOURCE_GROUP \
  --name $VM_NAME \
  --image $IMAGE \
  --size $SIZE \
  --admin-username $ADMIN_USERNAME \
  --authentication-type ssh \
  --ssh-key-values $SSH_KEY_PATH \
  --location $REGION

# Krok 4: Otwieranie portu 22 dla SSH
az vm open-port --port 22 --resource-group $RESOURCE_GROUP --name $VM_NAME

echo "Maszyna wirtualna $VM_NAME została utworzona pomyślnie."