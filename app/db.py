from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings


class Mongo:
    client: AsyncIOMotorClient | None = None


mongo = Mongo()


def get_db():
    if mongo.client is None:
        raise RuntimeError("Mongo client not initialized")
    return mongo.client[settings.db_name]


async def connect_to_mongo():
    client_kwargs: dict = {}

    # For MongoDB Atlas / TLS connections on macOS, certificate verification can fail
    # if the CA bundle isn't found. Using certifi fixes this reliably.
    uri = settings.mongodb_uri
    is_tls_uri = uri.startswith("mongodb+srv://") or "tls=true" in uri or "ssl=true" in uri
    if is_tls_uri:
        try:
            import certifi

            client_kwargs["tlsCAFile"] = certifi.where()
        except Exception:
            # If certifi isn't available for some reason, we'll fall back to defaults.
            pass

        # Only disable verification when explicitly requested (NOT recommended for production).
        if settings.mongodb_tls_insecure:
            client_kwargs["tlsAllowInvalidCertificates"] = True

    mongo.client = AsyncIOMotorClient(uri, **client_kwargs)


async def close_mongo_connection():
    if mongo.client is not None:
        mongo.client.close()
        mongo.client = None

