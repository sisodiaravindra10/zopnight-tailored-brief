# ZopNight Tailored Brief

Step-by-step, role-tailored product brief for ZopNight, built as a single static page.

- `index.html` carries the styles and script; product screenshots live in `img/` and load per step.
- Query parameters set what the reader sees: `?role=finance|engineering|finops|leadership`, `&depth=plain|detailed`, `&for=Company%20Name`. The hash (`#optimise`) deep-links to a step.
- No build step. Serve the folder from any static host.

Source of truth for the copy: ZopNight Product Brief, Cloud and AI, V9 (September 2026).

## Deploying

The deck is a single file, so any static host works. For ZopDay, which deploys container images through Helm, the repo also ships a container:

- `Dockerfile` serves `index.html` with nginx on port `8080`, health check at `/healthz`.
- `.github/workflows/image.yml` builds and pushes `ghcr.io/<owner>/zopnight-tailored-brief:latest` on every push to `main`.

In ZopDay, create a Service in the target Environment with that image, port `8080`, and the `/healthz` health check.

## Building

`index.html` is generated from `deck.template.html`, so edit the template, never the output.

```
python3 build.py
```

It writes two things from one source: the hosted page here, with screenshots as separate
cached files, and an inlined single-file copy for sharing as an artifact.

The rep control strip (role, depth, company presets) is off on the hosted page and on for the
inlined copy. Add `?rep=1` to any hosted URL to bring it back for internal use.
