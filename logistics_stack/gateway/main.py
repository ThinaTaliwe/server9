"""
FastAPI gateway for the logistics stack.

This service unifies access to the Fleetbase API, Karrio API and OSRM route
service. In a production system you would implement authentication,
authorization, validation and comprehensive error handling. For the purpose
of this demonstration the gateway proxies a few basic endpoints and exposes
an example route optimisation handler.

Environment variables:
  FLEETBASE_API_URL: base URL for the Fleetbase API
  KARRIO_API_URL:   base URL for the Karrio API
  OSRM_URL:         base URL for the OSRM route service
"""

import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx

app = FastAPI(title="Logistics Gateway", version="0.1.0")

# Resolve service URLs from the environment or fall back to sensible defaults
FLEETBASE_API_URL = os.getenv("FLEETBASE_API_URL", "http://fleetbase_api:8000")
KARRIO_API_URL = os.getenv("KARRIO_API_URL", "http://karrio_api:5002")
OSRM_URL = os.getenv("OSRM_URL", "http://osrm:5000")

# Shared asynchronous HTTP client. Using a single client improves connection
# pooling and performance when proxying requests.
client = httpx.AsyncClient(timeout=30.0)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Simple health endpoint to verify the gateway is running."""
    return {"status": "ok"}


@app.api_route("/fleetbase/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_fleetbase(path: str, request: Request) -> JSONResponse:
    """
    Proxy any request to the Fleetbase API. The HTTP method and body are
    preserved. This function forwards incoming requests to the corresponding
    path on the Fleetbase service defined in the environment.

    Example: GET /fleetbase/api/ping → forwards to
    {FLEETBASE_API_URL}/api/ping
    """
    url = f"{FLEETBASE_API_URL}/{path}"
    try:
        response = await client.request(
            method=request.method,
            url=url,
            headers=request.headers.raw,
            content=await request.body()
        )
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    return JSONResponse(status_code=response.status_code, content=response.json())


@app.api_route("/karrio/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_karrio(path: str, request: Request) -> JSONResponse:
    """
    Proxy any request to the Karrio API. This allows the caller to use
    /karrio/... endpoints instead of accessing the Karrio server directly.
    """
    url = f"{KARRIO_API_URL}/{path}"
    try:
        response = await client.request(
            method=request.method,
            url=url,
            headers=request.headers.raw,
            content=await request.body()
        )
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    return JSONResponse(status_code=response.status_code, content=response.json())


@app.get("/optimize-route", tags=["routing"])
async def optimize_route(origin: str, destination: str):
    """
    Compute a route between two coordinate pairs using OSRM.

    Query parameters:
      origin:      "lon,lat" pair for the origin point
      destination: "lon,lat" pair for the destination point

    For example: /optimize-route?origin=18.4233,-33.9188&destination=18.4241,-33.9190

    The OSRM service returns a JSON object with route information including
    distance and duration.
    """
    # Compose the OSRM request path. OSRM expects coordinates in
    # longitude,latitude order separated by a semicolon.
    coords = f"{origin};{destination}"
    osrm_endpoint = f"{OSRM_URL}/route/v1/driving/{coords}"
    params = {"overview": "false"}
    try:
        resp = await client.get(osrm_endpoint, params=params)
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    data = resp.json()
    if "routes" not in data:
        raise HTTPException(status_code=502, detail="Unexpected OSRM response")
    return data


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Ensure the shared HTTP client is closed on shutdown."""
    await client.aclose()