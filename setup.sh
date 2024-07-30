#!/bin/bash

# Exit on error
set -e

# Install Dapr
echo "Installing Dapr..."
# Check if Dapr is installed
if dapr --version > /dev/null 2>&1; then
  echo "Dapr is already installed"
else
  echo "Installing Dapr..."
  dapr init -k --runtime-version 1.14.0-rc.7
fi

# Default context
DEFAULT_CONTEXT="kind-kind"

# Set context from argument or use default
CONTEXT=${1:-$DEFAULT_CONTEXT}

# Set namespace to the specified context
echo "Setting kubectl context to $CONTEXT..."
kubectl config use-context $CONTEXT

# Create namespaces if they don't exist
echo "Creating namespaces..."
for ns in ns1 ns2; do
  if kubectl get namespace $ns > /dev/null 2>&1; then
    echo "Namespace $ns already exists"
  else
    kubectl create namespace $ns
  fi
done

# Build app images and load them in the kind cluster
echo "Building and loading app images..."
docker build -t demoactor-client:latest -f client/Dockerfile client
docker build -t demoactor-server:latest -f service/Dockerfile service
kind load docker-image demoactor-client:latest
kind load docker-image demoactor-server:latest



# Install Redis
echo "Installing Redis..."
if helm ls --all --short | grep -q '^redis$'; then
  echo "Redis is already installed"
else
  helm install redis bitnami/redis
fi

# Create secret with the password if it doesn't exist
echo "Creating Redis secrets..."
REDIS_PASSWORD=$(kubectl get secret --namespace default redis -o jsonpath="{.data.redis-password}" | base64 -d)
for ns in ns1 ns2; do
  if kubectl get secret redis-secret -n $ns > /dev/null 2>&1; then
    echo "Secret redis-secret already exists in namespace $ns"
  else
    kubectl create secret generic redis-secret -n $ns --from-literal=redis-password=$REDIS_PASSWORD
  fi
done

# Deploy the apps
echo "Deploying the apps..."
kubectl apply -f deploy/ns1.yml
kubectl apply -f deploy/ns2.yml

# Print instructions in green
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "\n\n"
echo -e "${GREEN}Your application is deployed. Run the following port-forward commands to access the app:${NC}"
echo -e "${GREEN}------------------------------------------${NC}"
echo "kubectl port-forward svc/demoactor-client-app-service 3001:3000 -n ns1"
echo "kubectl port-forward svc/demoactor-client-app-service 3002:3000 -n ns2"
echo "kubectl port-forward svc/demoactor-server-app-service 4001:5000 -n ns1"
echo "kubectl port-forward svc/demoactor-server-app-service 4002:5000 -n ns2"
echo ""
echo -e "${GREEN}Once the port-forward commands are running, you can access the app at the following URLs:${NC}"
echo -e "${GREEN}------------------------------------------${NC}"
echo "Client ns1: http://localhost:3001"
echo "Client ns2: http://localhost:3002"
echo "Server ns1: http://localhost:4001"
echo "Server ns2: http://localhost:4002"

# Wait to keep the port forwards open
wait
