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
