class CommandExecutor(object):
    def __init__(self, driver_commands):
        """
        :param driver_commands:
        :type driver_commands: cloudshell.layer_one.core.driver_commands_interface.DriverCommandsInterface
        """
        self._driver_commands = driver_commands
        self._registered_commands = {'Login': self.login}

    def execute_command(self, command):
        """
        :param command:
        :type command: cloudshell.layer_one.core.entities.command.Command
        :return:
        """
        if command.command_name in self._registered_commands:
            self._registered_commands[command.command_name](command)

    def login(self, command):
        """
        :param command:
        :type command: cloudshell.layer_one.core.entities.command.Command
        :return: 
        """
        address = command.command_params.get('address')
        user = command.command_params.get('user')
        password = command.command_params.get('password')

        try:
            command.response_info = self._driver_commands.login(address, user, password)
            command.success = True
        except Exception as e:
            command.success = False
            command.error = e.message
