from __future__ import annotations

import base64
import hashlib
import os


def encrypt_bytes(data: bytes, key_material: str) -> dict[str, str]:
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError as exc:
        raise RuntimeError("cryptography is required for encrypted capsule builds") from exc

    key = _derive_key(key_material)
    nonce = os.urandom(12)
    ciphertext = AESGCM(key).encrypt(nonce, data, None)
    return {
        "format": "ewos-encrypted-capsule",
        "cipher": "AES-256-GCM",
        "kdf": "SHA-256",
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
    }


def decrypt_bytes(payload: dict[str, str], key_material: str) -> bytes:
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError as exc:
        raise RuntimeError("cryptography is required for encrypted capsule verification") from exc

    if payload.get("format") != "ewos-encrypted-capsule":
        raise ValueError("Unsupported encrypted capsule format")
    key = _derive_key(key_material)
    nonce = base64.b64decode(payload["nonce"])
    ciphertext = base64.b64decode(payload["ciphertext"])
    return AESGCM(key).decrypt(nonce, ciphertext, None)


def _derive_key(key_material: str) -> bytes:
    if not key_material:
        raise RuntimeError("EWOS_CAPSULE_KEY must not be empty")
    return hashlib.sha256(key_material.encode("utf-8")).digest()
