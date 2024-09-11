def create_approved_locker_email(name:str, locker_number:int, combination:str):
    """
    Create an email for an approved locker
    """
    return f"""Hello {name},\n\nYour locker rental has been approved. Your locker number is {locker_number} and your combination is {combination}.\n\nThank you,\nUACS"""