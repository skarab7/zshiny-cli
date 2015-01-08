import base_client
import category
import article


def add_command(cls):
    enabled_commands.append(cls)
    base_client.PluginCommandBase.register(cls)

enabled_commands = []

for cat_cmd in [category.CategoryListCommand,
                category.CategoryShowSchemaCommand,
                category.CategoryGetOneCommand,
                category.CategoryFindByCommand,
                category.CategoryStatsCommand]:
    add_command(cat_cmd)


for art_cmd in [article.ArticleListCommand,
                article.ArticleStatsCommand,
                article.ArticleFindByFilterCommand,
                article.ArticleGetOneCommand,
                article.ArticleShowSchemaCommand]:
    add_command(art_cmd)
