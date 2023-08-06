from firebase import db

async def getUsersIdList():
    usersRef = db.collection('users')
    users = await usersRef.get()
    idsList = []

    for user in users:
        userId: str = user.id
        idsList.append(userId)
        
    return idsList