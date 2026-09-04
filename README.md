# ZopNight Tailored Brief

Step-by-step, role-tailored product brief for ZopNight, built as a single static page.

- `index.html` is self-contained: styles, script and every product screenshot are inlined.
- Query parameters set what the reader sees: `?role=finance|engineering|finops|leadership`, `&depth=plain|detailed`, `&for=Company%20Name`. The hash (`#optimise`) deep-links to a step.
- No build step. Serve the folder from any static host.

Source of truth for the copy: ZopNight Product Brief, Cloud and AI, V9 (September 2026).

## Deploying

The deck is a single file, so any static host works. For ZopDay, which deploys container images through Helm, the repo also ships a container:

- `Dockerfile` serves `index.html` with nginx on port `8080`, health check at `/healthz`.
- `.github/workflows/image.yml` builds and pushes `ghcr.io/<owner>/zopnight-tailored-brief:latest` on every push to `main`.

In ZopDay, create a Service in the target Environment with that image, port `8080`, and the `/healthz` health check.
