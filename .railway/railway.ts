// Railway Infrastructure as Code (IaC), the supported path for new services.
// After installing Railway CLI, link an authorized project, run:
// railway config plan; railway config apply
// The service uses Dockerfile.standalone and demo-only observations by default.
import {defineRailway, github, project, service} from "railway/iac";

export default defineRailway(() => {
  const mission = service("astrasentinel-ai", {
    source: github("harshakavali81-collab/AstraSentinel-AI", {branch: "main"}),
    healthcheck: "/api/health",
    healthcheckTimeout: 120,
    env: {
      ASTRA_OFFLINE: "1",
      RAILWAY_DOCKERFILE_PATH: "Dockerfile.standalone",
    },
  });

  return project("astrasentinel-ai", {resources: [mission]});
});
