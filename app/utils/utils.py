def create_approved_locker_email(name:str, locker_number:int, combination:str):
    """
    Create an email for an approved locker
    """
    return f"""Hello {name},\n\nYour locker rental has been approved. Your locker number is {locker_number} and your combination is {combination}.\n\nThank you,\nUACS"""

def create_rejected_locker_email(name:str, notes:str):
    """
    Create an email for a rejected locker
    """
    return f"""Hello {name},\n\nYour locker rental has been rejected. Reason: {notes}.\n\nIf you have any further questions email us at execs@uacs.ca.\n\nThank you,\nUACS"""