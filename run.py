"""
after run docker compose run this command
"""
import os

os.system("docker-compose exec api python3 -m scripts.on_startup")
