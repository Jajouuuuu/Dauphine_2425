#!/usr/bin/env python3
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USER') 
password = os.getenv('NEO4J_PASSWORD')

print(f'Testing connection to: {uri}')
print(f'User: {user}')
print(f'Password: {password[:3]}***')

try:
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        result = session.run('RETURN "Hello Neo4j!" as message')
        message = result.single()['message']
        print(f'✅ Success: {message}')
    driver.close()
except Exception as e:
    print(f'❌ Connection failed: {e}') 