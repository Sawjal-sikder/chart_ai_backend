Docker usage for this project

Production build

1. Build the Docker image:

```bash
# from the project root
docker build -t admin_panel_nestorc:latest .
```

2. Run the container (maps host port 8080 -> container port 80):

```bash
# run the production image (uses a small Node static server)
docker run --rm -p 8080:80 admin_panel_nestorc:latest
```

Or use docker-compose:

```bash
docker compose up --build
```

Development (fast iteration with bind mounts)

This starts the Vite dev server inside a container and exposes port 5173.

```bash
# start dev container
docker compose -f docker-compose.dev.yml up
```

Notes

- The production Dockerfile now uses a multi-stage build (Node builder -> Node runner) and serves the Vite `dist` output using the `serve` static server (no nginx).
- The dev compose file mounts your working directory and runs `npm run dev -- --host 0.0.0.0` so the dev server is reachable from the host.
- If you use yarn or pnpm, adapt the install/run commands inside the Dockerfiles/compose files accordingly.
