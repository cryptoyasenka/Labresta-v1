import ftplib
import logging
import os

logger = logging.getLogger(__name__)


def upload_to_ftp(
    local_path: str,
    remote_path: str,
    host: str,
    username: str,
    password: str,
) -> dict:
    """Upload a local file to FTP server.

    Tries plain FTP first, falls back to FTP_TLS if connection refused.
    Returns dict with 'success' (bool) and 'error' (str or None).
    """
    if not os.path.isfile(local_path):
        return {"success": False, "error": f"Local file not found: {local_path}"}

    for ftp_class in (ftplib.FTP, ftplib.FTP_TLS):
        try:
            ftp = ftp_class(host, timeout=30)
            ftp.login(username, password)

            if isinstance(ftp, ftplib.FTP_TLS):
                ftp.prot_p()

            remote_dir = os.path.dirname(remote_path)
            if remote_dir:
                try:
                    ftp.cwd(remote_dir)
                except ftplib.error_perm:
                    pass  # directory may not exist or already at root

            remote_filename = os.path.basename(remote_path)
            with open(local_path, "rb") as f:
                ftp.storbinary(f"STOR {remote_filename}", f)

            ftp.quit()
            logger.info("FTP upload OK: %s -> %s:%s", local_path, host, remote_path)
            return {"success": True, "error": None}

        except (ConnectionRefusedError, OSError) as e:
            if ftp_class is ftplib.FTP:
                logger.warning("Plain FTP failed (%s), trying FTP_TLS...", e)
                continue
            logger.error("FTP_TLS also failed: %s", e)
            return {"success": False, "error": str(e)}

        except Exception as e:
            logger.error("FTP upload error: %s", e)
            return {"success": False, "error": str(e)}

    return {"success": False, "error": "All FTP connection methods failed"}
