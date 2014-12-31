import base_client
import category


def add_command(cls):
    enabled_commands.append(cls)
    base_client.PluginClientBase.register(cls)

enabled_commands = []

add_command(category.CategoryListCommand)
