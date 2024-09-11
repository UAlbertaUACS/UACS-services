from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin.auth import verify_id_token

bearer_scheme = HTTPBearer(auto_error=False)

def get_firebase_user_from_token(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """Uses bearer token to identify firebase user id
    Args:
        token : the bearer token. Can be None as we set auto_error to False
    Returns:
        dict: the firebase user on success
    Raises:
        HTTPException 401 if user does not exist or token is invalid
    """
    try:
        if not token:
            # raise and catch to return 401, only needed because fastapi returns 403
            # by default instead of 401 so we set auto_error to False
            raise ValueError("No token")
        user = verify_id_token(token.credentials)
        if user["email"].split("@")[1] != "ualberta.ca":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User email is not a valid UAlberta email",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    # lots of possible exceptions, see firebase_admin.auth,
    # but most of the time it is a credentials issue
    except Exception:
        # we also set the header
        # see https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in or Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )