




# Dockerfile image
- Use minimal base image
- Only install necessary packages, and use the --no-cache flag to prevent the package manager from caching the downloaded packages.
- Avoid using the ENTRYPOINT instruction with shell form, as it can be vulnerable to command injection attacks. Use the exec form (CMD ["executable", "param1", "param2"]) to reduce the risk.

