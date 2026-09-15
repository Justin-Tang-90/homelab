# Homelab Infrastructure

Built a self-hosted infrastructure environment using
virtualization, Linux administration, containerization, networking,
reverse proxies, and database administration.

## Architecture

Proxmox VE
    +-- Linux VM 
    |
          +-- Docker
          |
                +-- Nginx
                +-- Application
                +-- PostgreSQL
                +-- Portainer

## Technologies

- Proxmox VE
- Linux
- Docker
- Docker Compose
- Portainer
- Nginx
- PostgreSQL

## What I implemented

- Created and configured virtual machines in Proxmox
- Installed and configured Docker
- Created a multi-container application using Docker Compose
- Configured Nginx as a reverse proxy
- Connected the application to PostgreSQL
- Configured Docker networking and service discovery
- Managed containers through Portainer
- Configured persistent configuration using Docker volumes
- Implemented container restart policies
- Troubleshot container and networking issues
