import base_client
import category
import article


def add_command(cls):
    enabled_commands.append(cls)
    base_client.PluginCommandBase.register(cls)

enabled_commands = []

add_command(category.CategoryListCommand)
add_command(category.CategoryShowSchemaCommand)
add_command(category.CategoryGetOneCommand)
add_command(category.CategoryFindByCommand)
add_command(category.CategoryStatsCommand)
