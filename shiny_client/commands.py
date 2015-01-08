import base_client
import category
import article
import article_filter


def add_command(cls):
    enabled_commands.append(cls)
    base_client.PluginCommandBase.register(cls)

enabled_commands = []


for art_cmd in [article.ArticleListCommand,
                article.ArticleStatsCommand,
                article.ArticleFindByFilterCommand,
                article.ArticleGetOneCommand,
                article.ArticleShowSchemaCommand]:
    add_command(art_cmd)


for cat_cmd in [category.CategoryListCommand,
                category.CategoryShowSchemaCommand,
                category.CategoryGetOneCommand,
                category.CategoryFindByCommand,
                category.CategoryStatsCommand]:
    add_command(cat_cmd)


for art_filter in [article_filter.FilterGetOneCommand,
                   article_filter.FilterListCommand,
                   article_filter.FilterShowSchemaCommand,
                   article_filter.FilterGetOneCommand]:
    add_command(art_filter)
