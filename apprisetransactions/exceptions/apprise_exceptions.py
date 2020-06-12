class AppriseNotificationFailure(Exception):
    # Apprise returns false if something goes wrong
    # they do not have Exception objects, so we're creating a catch all here
    pass
