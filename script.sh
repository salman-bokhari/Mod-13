#!/bin/bash

# API base URL
BASE_URL="http://localhost:8000"

# User credentials
EMAIL="salman1@example.com"
PASSWORD="pass123"

echo "===> Registering user..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")

echo "Register response: $REGISTER_RESPONSE"

# Extract token from registration response
ACCESS_TOKEN=$(echo $REGISTER_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo "Access token from registration: $ACCESS_TOKEN"

echo "===> Logging in user..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")

echo "Login response: $LOGIN_RESPONSE"

# Extract token from login response
ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
echo "Access token from login: $ACCESS_TOKEN"

echo "===> Creating a calculation..."
CALC_RESPONSE=$(curl -s -X POST "$BASE_URL/calculations/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"operand1":5,"operand2":3,"operation":"add"}')

echo "Calculation create response: $CALC_RESPONSE"

echo "===> Listing all calculations..."
LIST_RESPONSE=$(curl -s -X GET "$BASE_URL/calculations/" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

echo "List calculations response: $LIST_RESPONSE"

