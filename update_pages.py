#!/usr/bin/env python3
"""
Script to automatically discover GitHub Pages deployments and update index.html
"""

import json
import os
import requests
from datetime import datetime

# GitHub API configuration
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_USERNAME = "oliynykmax"
API_BASE = "https://api.github.com"


def get_repos_with_pages():
    """Fetch all repositories with GitHub Pages enabled"""
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    # Get all public repositories
    repos = []
    page = 1
    while True:
        url = f"{API_BASE}/users/{GITHUB_USERNAME}/repos"
        params = {
            "type": "public",
            "sort": "updated",
            "direction": "desc",
            "per_page": 100,
            "page": page,
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error fetching repos: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        repos.extend(data)
        page += 1

    # Filter repositories with GitHub Pages enabled
    pages_repos = []
    for repo in repos:
        if repo.get("has_pages", False):
            pages_url = f"https://{GITHUB_USERNAME}.github.io/{repo['name']}/"
            pages_repos.append(
                {
                    "name": repo["name"],
                    "description": repo.get("description", ""),
                    "url": pages_url,
                    "updated_at": repo.get("updated_at", ""),
                    "homepage": repo.get("homepage", ""),
                }
            )

    return pages_repos


def generate_html(repos):
    """Generate HTML for the index page"""
    cards_html = ""

    for repo in repos:
        # Skip the main site itself
        if repo["name"] == "oliynykmax.github.io":
            continue

        description = repo["description"] or "No description available"
        name = repo["name"].replace("-", " ").title()

        cards_html += f'''
            <!-- Project Card: {repo["name"]} -->
            <a href="{repo["url"]}" class="group block p-6 border border-border bg-black/50 hover:border-yellow transition-all duration-300 card-glow">
                <div class="mb-2">
                    <h2 class="text-xl font-bold group-hover:text-yellow transition-colors">{name}</h2>
                </div>
                <p class="text-text-muted text-sm leading-relaxed">{description}</p>
            </a>
'''

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Max Oliinyk | Index</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect x='0' y='0' width='100' height='100' rx='20' fill='%23FFFF00'/><text x='50' y='72' font-size='70' font-family='monospace' font-weight='bold' fill='%23000000' text-anchor='middle'>H</text></svg>">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        mono: ['"JetBrains Mono"', 'monospace'],
                    }},
                    colors: {{
                        bg: '#000000',
                        text: '#ffffff',
                        'text-muted': '#888888',
                        yellow: '#FFFF00',
                        border: '#222222',
                    }},
                }}
            }}
        }}
    </script>
    <style type="text/tailwindcss">
        @layer base {{
            body {{ @apply font-mono bg-bg text-text antialiased min-h-screen flex flex-col justify-center items-center p-6; }}
            a:focus-visible {{ @apply outline-none ring-2 ring-yellow ring-offset-2 ring-offset-bg rounded-sm; }}
        }}
        .hex-grid {{
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='28' height='49' viewBox='0 0 28 49'%3E%3Cg fill-rule='evenodd'%3E%3Cg fill='%23FFFF00' fill-opacity='0.03'%3E%3Cpath d='M13.99 9.25l13 7.5v15l-13 7.5L1 31.75v-15l12.99-7.5zM3 17.9v12.7l10.99 6.34 11-6.35V17.9l-11-6.34L3 17.9zM0 15l12.98-7.5V0h-2v6.35L0 12.69v2.3zm0 18.5L12.98 41v8h-2v-6.85L0 35.81v-2.3zM15 0v7.5L27.99 15H28v-2.31h-.01L17 6.35V0h-2zm0 49v-8l12.99-7.5H28v2.31h-.01L17 42.15V49h-2z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        }}
        .stripe-bg {{
            background-image: repeating-linear-gradient(
                45deg,
                transparent,
                transparent 10px,
                rgba(255, 255, 0, 0.05) 10px,
                rgba(255, 255, 0, 0.05) 20px
            );
        }}
        .card-glow:hover {{
            box-shadow: 0 0 20px rgba(255, 255, 0, 0.1);
        }}
    </style>
</head>
<body class="relative overflow-x-hidden">
    <div class="hex-grid fixed inset-0 pointer-events-none z-0"></div>
    
    <main class="relative z-10 w-full max-w-2xl my-12">
        <header class="mb-12 text-center">
            <h1 class="text-4xl font-bold tracking-tighter mb-2">MAX <span class="text-yellow">OLIINYK</span></h1>
            <p class="text-text-muted text-[10px] uppercase tracking-[0.4em]">Public Index & Project Hub</p>
        </header>

        <div class="space-y-4">
            <!-- Project Card: oliinyk.dev -->
            <a href="https://oliinyk.dev" class="group block p-6 border border-border bg-black/50 stripe-bg hover:border-yellow transition-all duration-300 card-glow">
                <div class="flex justify-between items-start mb-2">
                    <h2 class="text-xl font-bold group-hover:text-yellow transition-colors">oliinyk.dev</h2>
                    <span class="text-yellow text-[10px] border border-yellow px-2 py-1 rounded-sm uppercase tracking-wider font-bold">Main Site</span>
                </div>
                <p class="text-text-muted text-sm leading-relaxed">Portfolio & Blog. Central hub for software engineering projects, research, and technical writeups.</p>
            </a>
            
            <!-- Auto-discovered separator -->
            <div class="text-center my-8">
                <div class="border-t border-border"></div>
                <span class="text-text-muted text-xs uppercase tracking-wider bg-bg px-4 -mt-2 inline-block">auto discovered from GitHub</span>
                <div class="border-t border-border"></div>
            </div>
            
{cards_html}
        </div>
        
        <footer class="mt-12 text-center text-text-muted text-xs">
            <p>Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}</p>
            <p class="mt-2">Auto-discovered from GitHub Pages</p>
        </footer>
    </main>
</body>
</html>
"""
    return html


def main():
    """Main function"""
    print("Fetching repositories with GitHub Pages...")
    repos = get_repos_with_pages()

    print(f"Found {len(repos)} repositories with Pages:")
    for repo in repos:
        print(f"  - {repo['name']}: {repo['url']}")

    print("\nGenerating index.html...")
    html = generate_html(repos)

    # Write to index.html
    with open("index.html", "w") as f:
        f.write(html)

    print("index.html updated successfully!")


if __name__ == "__main__":
    main()
