from fastapi import APIRouter, Request, Query
from pymongo import MongoClient
from fastapi.responses import JSONResponse

router = APIRouter(prefix="", tags=['SensorData'])

@router.get("/getusers")
async def get_users(request: Request, username: str = Query(...), password: str = Query(...)) -> dict:
    db_users = request.app.users  # Get users collection from the app's database
    
    try:
        # Log received parameters
        print(f"Received parameters: username={username}, password={password}")
        
        # Query MongoDB with case-insensitive search for username
        user = db_users.find_one({"user_name": {"$regex": f"^{username}$", "$options": "i"}})

        # Log query result
        print(f"Query result: {user}")

        # Check if user exists and password matches
        if user and user["password"] == password:
            print("User authenticated successfully")
            return {
                "status": "success",
                "message": "Valid user",
                "user": {
                    "user_name": user["user_name"],
                    "password": user["password"]
                }
            }
        else:
            print("Authentication failed: Invalid username or password")
            return {"status": "fail", "message": "Invalid username or password"}
    
    except Exception as e:
        print(f"Error during authentication: {e}")
        return {"status": "error", "message": str(e)}
