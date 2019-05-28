# Api Gateway Service

## Overview
Api-gateway is the only public-facing service from Datadeck's backend. It has the following responsibilities:
- Authenticates user
- Dispatches requests to appropriate downstream services
- Handles coexistence of different versions of the same downstream service/api
- Rate limiting
