# Security Policy

AstraSentinel AI is a local educational demonstrator. It currently does not include production authentication, user isolation, rate limiting, public Internet abuse protection, or security certification.

## Supported release

The `main` branch is the actively tested source. A security maintenance SLA or independently audited guarantee is not offered.

## Reporting potential security problems

Use GitHub's private vulnerability reporting if the repository has it enabled, or contact the owner privately. Do not include private credentials or exploitable details in public issues.

## Secure usage

- Keep the FastAPI backend private until authenticated, rate-limited and served behind HTTPS.
- Publish only the standalone static landing page on a public static web host unless interactive hosting controls are added.
- Avoid committing environment secrets and private data.
- Review dependency updates, pin production images, and monitor resource-intensive numerical endpoints.
- Do not rely on test success to claim aerospace or production security certification.


## Hosted demo credential gate

The standalone deployment offers `ASTRA_DEMO_AUTH=1` plus `ASTRA_DEMO_USER` and `ASTRA_DEMO_PASSWORD`. When enabled, the process **fails to start** if credentials are missing; GET /api/health remains open for provider probes. The browser uses HTTP Basic authentication, which **must** be wrapped in trusted HTTPS. Render and Railway deployment manifests opt into this protection and require private host variables. It is a single-account gate, not multiuser identity, access policy, brute-force mitigation, SSO or a security audit. Use strong unique credentials, short-lived demos, and trusted provider access controls.
