#!/usr/bin/env python3
"""
Observer-Eye CLI - Command-line interface for managing the Observer-Eye platform.

Usage:
    ./observercli.py <command>

Commands:
    start    - Start all containers
    stop     - Stop all containers
    status   - Show status of all containers
    restart  - Restart all containers
    build    - Build all images
    rebuild  - Force rebuild all images (no cache)
    clean    - Stop containers and remove them
    purge    - Remove all containers, images, volumes, and networks
    logs     - Show logs from all containers
    shell    - Open a shell in a container
    health   - Check health of all service endpoints
"""

import subprocess
import sys
import os
import urllib.request
import urllib.error
from typing import List, Tuple

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    """Print a styled header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}  👁️  Observer-Eye CLI - {text}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

def print_success(text: str):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_error(text: str):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def print_info(text: str):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")

def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")

def run_command(cmd: List[str], capture: bool = False) -> subprocess.CompletedProcess:
    """Run a shell command."""
    print_info(f"Running: {' '.join(cmd)}")
    try:
        if capture:
            return subprocess.run(cmd, capture_output=True, text=True, check=True)
        else:
            return subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed with exit code {e.returncode}")
        if capture and e.stderr:
            print(e.stderr)
        raise

def get_project_dir() -> str:
    """Get the project directory (where docker-compose.yml is located)."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return script_dir

def docker_compose_cmd() -> List[str]:
    """Get the docker compose command (supports both old and new syntax)."""
    # Try docker compose (new syntax) first
    try:
        subprocess.run(["docker", "compose", "version"], capture_output=True, check=True)
        return ["docker", "compose"]
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fall back to docker-compose (old syntax)
        return ["docker-compose"]

# =============================================================================
# COMMANDS
# =============================================================================

def cmd_start():
    """Start all containers."""
    print_header("Starting Observer-Eye")
    os.chdir(get_project_dir())
    run_command(docker_compose_cmd() + ["up", "-d"])
    print_success("All containers started successfully!")
    print_info("Frontend: http://localhost:80")
    print_info("Middleware API: http://localhost:8400/docs")
    print_info("Backend Admin: http://localhost:8000/admin")

def cmd_stop():
    """Stop all containers."""
    print_header("Stopping Observer-Eye")
    os.chdir(get_project_dir())
    run_command(docker_compose_cmd() + ["stop"])
    print_success("All containers stopped!")

def cmd_status():
    """Show status of all containers."""
    print_header("Container Status")
    os.chdir(get_project_dir())
    
    # Get container status
    run_command(docker_compose_cmd() + ["ps"])
    
    print(f"\n{Colors.BOLD}Health Checks:{Colors.ENDC}")
    
    # Check individual service health
    services = ["frontend", "middleware", "backend", "db", "redis"]
    for service in services:
        try:
            result = subprocess.run(
                docker_compose_cmd() + ["ps", "-q", service],
                capture_output=True, text=True
            )
            if result.stdout.strip():
                # Container exists, check health
                health_result = subprocess.run(
                    ["docker", "inspect", "--format", "{{.State.Status}}", result.stdout.strip()],
                    capture_output=True, text=True
                )
                status = health_result.stdout.strip()
                if status == "running":
                    print_success(f"{service}: running")
                else:
                    print_warning(f"{service}: {status}")
            else:
                print_error(f"{service}: not found")
        except Exception as e:
            print_error(f"{service}: error checking status")

def cmd_restart():
    """Restart all containers."""
    print_header("Restarting Observer-Eye")
    os.chdir(get_project_dir())
    run_command(docker_compose_cmd() + ["restart"])
    print_success("All containers restarted!")

def cmd_build():
    """Build all images."""
    print_header("Building Observer-Eye Images")
    os.chdir(get_project_dir())
    run_command(docker_compose_cmd() + ["build"])
    print_success("All images built successfully!")

def cmd_rebuild():
    """Force rebuild all images without cache."""
    print_header("Rebuilding Observer-Eye Images (No Cache)")
    os.chdir(get_project_dir())
    run_command(docker_compose_cmd() + ["build", "--no-cache", "--pull"])
    print_success("All images rebuilt successfully!")

def cmd_clean():
    """Stop and remove all containers."""
    print_header("Cleaning Observer-Eye")
    os.chdir(get_project_dir())
    
    print_info("Stopping containers...")
    run_command(docker_compose_cmd() + ["down"])
    
    print_success("All containers stopped and removed!")

def cmd_purge():
    """Remove all containers, images, volumes, and networks."""
    print_header("Purging Observer-Eye")
    os.chdir(get_project_dir())
    
    print_warning("This will remove ALL data, containers, images, and volumes!")
    confirm = input(f"{Colors.YELLOW}Are you sure? (yes/no): {Colors.ENDC}")
    
    if confirm.lower() != "yes":
        print_info("Purge cancelled.")
        return
    
    print_info("Stopping and removing containers, networks, and volumes...")
    run_command(docker_compose_cmd() + ["down", "-v", "--remove-orphans"])
    
    print_info("Removing images...")
    try:
        # Get project name for image filtering
        result = subprocess.run(
            docker_compose_cmd() + ["images", "-q"],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            images = result.stdout.strip().split('\n')
            for img in images:
                if img:
                    subprocess.run(["docker", "rmi", "-f", img], capture_output=True)
    except Exception:
        pass
    
    # Remove observer-eye related images
    print_info("Removing observer-eye images...")
    try:
        result = subprocess.run(
            ["docker", "images", "--filter", "reference=*observer*", "-q"],
            capture_output=True, text=True
        )
        if result.stdout.strip():
            subprocess.run(
                ["docker", "rmi", "-f"] + result.stdout.strip().split('\n'),
                capture_output=True
            )
    except Exception:
        pass
    
    print_info("Pruning unused Docker resources...")
    subprocess.run(["docker", "system", "prune", "-f"], capture_output=True)
    
    print_success("Purge complete! All Observer-Eye data has been removed.")

def cmd_logs():
    """Show logs from all containers."""
    print_header("Container Logs")
    os.chdir(get_project_dir())
    
    # Check if specific service was requested
    if len(sys.argv) > 2:
        service = sys.argv[2]
        run_command(docker_compose_cmd() + ["logs", "-f", "--tail=100", service])
    else:
        run_command(docker_compose_cmd() + ["logs", "-f", "--tail=50"])

def cmd_shell():
    """Open a shell in a container."""
    os.chdir(get_project_dir())
    
    services = {
        "1": ("frontend", "/bin/sh"),
        "2": ("middleware", "/bin/bash"),
        "3": ("backend", "/bin/bash"),
        "4": ("db", "psql -U observer observer_eye"),
        "5": ("redis", "redis-cli"),
    }
    
    print_header("Shell Access")
    print("Select a container:")
    print("  1) Frontend (nginx)")
    print("  2) Middleware (FastAPI)")
    print("  3) Backend (Django)")
    print("  4) Database (PostgreSQL)")
    print("  5) Redis")
    
    choice = input(f"\n{Colors.CYAN}Enter choice (1-5): {Colors.ENDC}")
    
    if choice in services:
        service, shell = services[choice]
        print_info(f"Connecting to {service}...")
        os.system(f"docker compose exec {service} {shell}")
    else:
        print_error("Invalid choice")

def cmd_health():
    """Check health of all service endpoints."""
    print_header("Health Check")
    
    endpoints: List[Tuple[str, str, str]] = [
        ("Frontend", "http://localhost:80", "/"),
        ("Middleware API", "http://localhost:8400", "/health"),
        ("Middleware Docs", "http://localhost:8400", "/docs"),
        ("Backend Admin", "http://localhost:8000", "/admin/"),
        ("Backend Health", "http://localhost:8000", "/api/core/health/"),
    ]
    
    all_healthy = True
    
    for name, base_url, path in endpoints:
        url = f"{base_url}{path}"
        try:
            req = urllib.request.Request(url, method='GET')
            req.add_header('User-Agent', 'ObserverCLI/1.0')
            with urllib.request.urlopen(req, timeout=5) as response:
                status = response.getcode()
                if 200 <= status < 400:
                    print_success(f"{name}: OK ({status}) - {url}")
                else:
                    print_warning(f"{name}: {status} - {url}")
                    all_healthy = False
        except urllib.error.HTTPError as e:
            if e.code in [401, 403]:  # Auth required is still "up"
                print_success(f"{name}: OK ({e.code} - auth required) - {url}")
            else:
                print_error(f"{name}: HTTP {e.code} - {url}")
                all_healthy = False
        except urllib.error.URLError as e:
            print_error(f"{name}: Connection failed - {url}")
            print_info(f"  Reason: {e.reason}")
            all_healthy = False
        except Exception as e:
            print_error(f"{name}: Error - {e}")
            all_healthy = False
    
    print()
    if all_healthy:
        print_success("All services are healthy!")
    else:
        print_warning("Some services are not healthy. Run './observercli.py logs' to investigate.")

def cmd_help():
    """Show help message."""
    print_header("Help")
    print(__doc__)
    print(f"\n{Colors.BOLD}Examples:{Colors.ENDC}")
    print("  ./observercli.py start      # Start the platform")
    print("  ./observercli.py status     # Check container status")
    print("  ./observercli.py logs       # View all logs")
    print("  ./observercli.py logs backend  # View backend logs only")
    print("  ./observercli.py rebuild    # Rebuild without cache")
    print("  ./observercli.py purge      # Remove everything")

# =============================================================================
# MAIN
# =============================================================================

COMMANDS = {
    "start": cmd_start,
    "stop": cmd_stop,
    "status": cmd_status,
    "restart": cmd_restart,
    "build": cmd_build,
    "rebuild": cmd_rebuild,
    "clean": cmd_clean,
    "purge": cmd_purge,
    "logs": cmd_logs,
    "shell": cmd_shell,
    "health": cmd_health,
    "help": cmd_help,
    "--help": cmd_help,
    "-h": cmd_help,
}

def main():
    if len(sys.argv) < 2:
        cmd_help()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command not in COMMANDS:
        print_error(f"Unknown command: {command}")
        print_info("Run './observercli.py help' for available commands")
        sys.exit(1)
    
    try:
        COMMANDS[command]()
    except subprocess.CalledProcessError:
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n")
        print_info("Operation cancelled")
        sys.exit(0)

if __name__ == "__main__":
    main()
