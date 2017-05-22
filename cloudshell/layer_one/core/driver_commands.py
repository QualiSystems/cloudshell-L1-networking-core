def l1_command(command_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print command_name
            return func(*args, **kwargs)
        return wrapper
    return decorator


class DriverCommands(object):
    pass


    @l1_command('test_command')
    def login(self):
        pass

    @l1_command('test_logout')
    def logout(self):
        pass
