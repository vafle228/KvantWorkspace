def getUserPersonalInfo(user):
    if hasattr(user, 'studentpersonalinfo'):
        return user.studentpersonalinfo
    return user.staffpersonalinfo