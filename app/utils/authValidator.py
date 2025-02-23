from fastapi import Request, HTTPException

class AuthValidator:
    """사용자 인증을 담당하는 클래스"""
    
    @staticmethod
    def get_user_id(request: Request) -> int:
        """세션에서 user_id를 가져오고, 없으면 인증 예외 발생"""
        user = request.session.get("user")
        if not user or not user.get("id"):
            raise HTTPException(status_code=401, detail="사용자 인증이 필요합니다.")
        return user["id"]
