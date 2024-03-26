def loginPrompt() -> tuple[str, str, str, str]:
    email = input("Enter email address: ")
    password = input("Enter password: ")
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    
    return (email, password, first_name, last_name)
