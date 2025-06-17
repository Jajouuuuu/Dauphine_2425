#!/usr/bin/env python3
"""
Neo4j Setup Script for Community Features

This script helps set up Neo4j for the community features of the Media Finder application.
It provides instructions and checks for Neo4j installation.
"""

import os
import subprocess
import sys
from pathlib import Path

def check_neo4j_installation():
    """Check if Neo4j is installed"""
    print("🔍 Checking Neo4j installation...")
    
    # Check if neo4j command is available
    try:
        result = subprocess.run(['neo4j', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Neo4j found: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Check if Docker is available for Neo4j container
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Docker found: {result.stdout.strip()}")
            print("   Neo4j can be run in Docker container")
            return "docker"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ Neo4j not found")
    return False

def install_neo4j_instructions():
    """Provide installation instructions"""
    print("\n📋 Neo4j Installation Options:")
    print("=" * 50)
    
    print("\n🐳 Option 1: Docker (Recommended)")
    print("   1. Install Docker:")
    print("      sudo apt update && sudo apt install docker.io")
    print("      sudo systemctl start docker")
    print("      sudo usermod -aG docker $USER")
    print("      # Log out and back in")
    print()
    print("   2. Run Neo4j container:")
    print("      docker run -d \\")
    print("        --name neo4j \\")
    print("        -p 7474:7474 -p 7687:7687 \\")
    print("        -e NEO4J_AUTH=neo4j/password \\")
    print("        neo4j:latest")
    print()
    print("   3. Access Neo4j Browser: http://localhost:7474")
    print("      Username: neo4j")
    print("      Password: password")
    
    print("\n💾 Option 2: Direct Installation")
    print("   1. Install Neo4j:")
    print("      wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -")
    print("      echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list")
    print("      sudo apt update && sudo apt install neo4j")
    print()
    print("   2. Configure and start:")
    print("      sudo systemctl enable neo4j")
    print("      sudo systemctl start neo4j")
    print("      sudo neo4j-admin set-initial-password password")

def start_neo4j_docker():
    """Start Neo4j using Docker"""
    print("\n🐳 Starting Neo4j with Docker...")
    
    # Check if container already exists
    try:
        result = subprocess.run(['docker', 'ps', '-a', '--filter', 'name=neo4j'], 
                              capture_output=True, text=True)
        if 'neo4j' in result.stdout:
            print("   Neo4j container exists, starting...")
            subprocess.run(['docker', 'start', 'neo4j'])
        else:
            print("   Creating new Neo4j container...")
            subprocess.run([
                'docker', 'run', '-d',
                '--name', 'neo4j',
                '-p', '7474:7474', '-p', '7687:7687',
                '-e', 'NEO4J_AUTH=neo4j/password',
                'neo4j:latest'
            ])
        
        print("✅ Neo4j container started!")
        print("   Browser: http://localhost:7474")
        print("   Bolt: bolt://localhost:7687")
        print("   Username: neo4j")
        print("   Password: password")
        
    except Exception as e:
        print(f"❌ Error starting Neo4j container: {e}")
        return False
    
    return True

def test_neo4j_connection():
    """Test connection to Neo4j"""
    print("\n🔗 Testing Neo4j connection...")
    
    try:
        from neo4j import GraphDatabase
        
        driver = GraphDatabase.driver(
            "bolt://localhost:7687", 
            auth=("neo4j", "password")
        )
        
        with driver.session() as session:
            result = session.run("RETURN 'Hello Neo4j!' as message")
            message = result.single()["message"]
            print(f"✅ Connection successful: {message}")
        
        driver.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def setup_sample_data():
    """Setup sample data for community features"""
    print("\n📊 Setting up sample community data...")
    
    try:
        from neo4j import GraphDatabase
        
        driver = GraphDatabase.driver(
            "bolt://localhost:7687", 
            auth=("neo4j", "password")
        )
        
        with driver.session() as session:
            # Create sample users
            session.run("""
            MERGE (u1:User {name: 'Alice', avatarUrl: 'https://via.placeholder.com/100'})
            MERGE (u2:User {name: 'Bob', avatarUrl: 'https://via.placeholder.com/100'})
            MERGE (u3:User {name: 'Charlie', avatarUrl: 'https://via.placeholder.com/100'})
            """)
            
            # Create sample content
            session.run("""
            MERGE (c1:Content {
                title: 'The Matrix', 
                type: 'movie', 
                platform: 'Netflix',
                posterUrl: 'https://via.placeholder.com/200x300'
            })
            MERGE (c2:Content {
                title: 'Cyberpunk 2077', 
                type: 'game', 
                platform: 'Steam',
                posterUrl: 'https://via.placeholder.com/200x300'
            })
            """)
            
            # Create sample reviews
            session.run("""
            MATCH (u:User {name: 'Alice'}), (c:Content {title: 'The Matrix'})
            MERGE (u)-[:REVIEWED]->(r:Review {
                id: randomUUID(),
                rating: 9,
                comment: 'Amazing sci-fi movie with groundbreaking effects!',
                createdAt: datetime()
            })-[:ABOUT]->(c)
            """)
            
            print("✅ Sample data created successfully!")
        
        driver.close()
        return True
        
    except Exception as e:
        print(f"❌ Error setting up sample data: {e}")
        return False

def main():
    """Main setup function"""
    print("🎬 Neo4j Setup for Media Finder Community Features")
    print("=" * 60)
    
    # Check current installation
    neo4j_status = check_neo4j_installation()
    
    if neo4j_status is True:
        print("✅ Neo4j is already installed!")
        if test_neo4j_connection():
            setup_sample_data()
        else:
            print("⚠️  Neo4j is installed but not running or not configured properly")
    
    elif neo4j_status == "docker":
        print("\n🐳 Docker is available. Would you like to start Neo4j in Docker?")
        response = input("Start Neo4j container? (y/n): ").lower().strip()
        
        if response in ['y', 'yes']:
            if start_neo4j_docker():
                # Wait a moment for Neo4j to start
                import time
                print("   Waiting for Neo4j to start...")
                time.sleep(10)
                
                if test_neo4j_connection():
                    setup_sample_data()
        else:
            install_neo4j_instructions()
    
    else:
        install_neo4j_instructions()
    
    print("\n🎯 Next Steps:")
    print("1. Ensure Neo4j is running on bolt://localhost:7687")
    print("2. Verify .env file contains:")
    print("   NEO4J_URI=bolt://localhost:7687")
    print("   NEO4J_USER=neo4j")
    print("   NEO4J_PASSWORD=password")
    print("3. Run: python main.py")
    print("\n🌟 The Community page will be fully functional once Neo4j is running!")

if __name__ == "__main__":
    main() 