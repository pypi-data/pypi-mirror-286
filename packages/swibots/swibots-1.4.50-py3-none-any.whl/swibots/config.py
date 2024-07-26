import os


APP_CONFIG = {
    "CHAT_SERVICE": {
        "BASE_URL": os.getenv("CHAT_SERVICE_BASE_URL") or "https://chat.switch.pe",
        "WS_URL": os.getenv("CHAT_SERVICE_WS_URL")
        or "wss://chat.switch.pe/v1/websocket/message/ws",
    },
    "BOT_SERVICE": {
        "BASE_URL": os.getenv("BOT_SERVICE_BASE_URL") or "https://chat.switch.pe",
    },
    "AUTH_SERVICE": {
        "BASE_URL": os.getenv("AUTH_SERVICE_BASE_URL")
        or "https://api-gateway.switch.pe/user-service",
    },
    "AIRDROP_SERVICE": {
        "BASE_URL": os.getenv("AIRDROP_SERVICE_BASE_URL")
        or "https://api-gateway.switch.pe/airdrop-service"
    },
    "COMMUNITY_SERVICE": {
        "BASE_URL": os.getenv("COMMUNITY_SERVICE_BASE_URL")
        or "https://api-gateway.switch.pe/community-service",
        "WS_URL": os.getenv("COMMUNITY_SERVICE_WS_URL")
        or "wss://api-gateway.switch.pe/v1/websocket/community/ws",
    },
    "BACKBLAZE": {
        "BUCKET_ID": os.getenv("BACKBLAZE_BUCKET_ID") or "ae385c1697b5d6459a03051f",
        "ACCOUNT_ID": os.getenv("BACKBLAZE_ACCOUNT_ID") or "e8c67565a35f",
        "APPLICATION_KEY": os.getenv("BACKBLAZE_APPLICATION_KEY")
        or "005533701cf8a07cceaf64d50328ea8ef004fef66b",
    },
}


def get_config():
    return APP_CONFIG


def reload_config():
    APP_CONFIG["CHAT_SERVICE"]["BASE_URL"] = (
        os.getenv("CHAT_SERVICE_BASE_URL") or "https://chat.switch.pe"
    )
    APP_CONFIG["CHAT_SERVICE"]["WS_URL"] = (
        os.getenv("CHAT_SERVICE_WS_URL")
        or "wss://chat.switch.pe/v1/websocket/message/ws"
    )
    APP_CONFIG["BOT_SERVICE"]["BASE_URL"] = (
        os.getenv("BOT_SERVICE_BASE_URL") or "https://chat.switch.pe"
    )
    APP_CONFIG["AUTH_SERVICE"]["BASE_URL"] = (
        os.getenv("AUTH_SERVICE_BASE_URL")
        or "https://api-gateway.switch.pe/user-service"
    )
    APP_CONFIG["COMMUNITY_SERVICE"]["BASE_URL"] = (
        os.getenv("COMMUNITY_SERVICE_BASE_URL")
        or "https://api-gateway.switch.pe/community-service"
    )
    APP_CONFIG["COMMUNITY_SERVICE"]["WS_URL"] = (
        os.getenv("COMMUNITY_SERVICE_WS_URL")
        or "wss://api-gateway.switch.pe/v1/websocket/community/ws"
    )
    APP_CONFIG["AIRDROP_SERVICE"]["BASE_URL"] = (
        os.getenv("AIRDROP_SERVICE_BASE_URL")
        or "https://api-gateway.switch.pe/airdrop-service"
    )


reload_config()
