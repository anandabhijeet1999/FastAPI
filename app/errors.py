from fastapi import HTTPException


def http_400(message: str):
    raise HTTPException(status_code=400, detail=message)


def http_404(message: str):
    raise HTTPException(status_code=404, detail=message)


def http_409(message: str):
    raise HTTPException(status_code=409, detail=message)

