from datetime import datetime

import typer
from google_suite import Blogger
from rich.console import Console
from rich.table import Table

console = Console()

blogger = typer.Typer()


@blogger.command(help="Lists all the blogs available in the Blogger account.")
def list_blogs():
    """List all Blogger blogs."""
    blogs = Blogger.list_blogs()
    if blogs:
        table = Table(title="Blogger Blogs", show_lines=True)
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Name", style="magenta", justify="center")
        table.add_column("Posts", style="yellow", justify="center")
        for blog in blogs["items"]:
            table.add_row(blog["id"], blog["name"], str(blog["posts"]["totalItems"]))
        console.print(table)
        return blogs
    else:
        typer.echo("No blogs found.")


@blogger.command(help="Lists all the posts in the Blogger account.")
def list_posts():
    """List all Blogger posts."""
    posts = Blogger.list_posts()
    if posts:
        table = Table(title="Blogger Posts", show_lines=True)
        table.add_column("ID", style="cyan", justify="center", overflow="fold")
        table.add_column("Published", style="magenta", justify="center")
        table.add_column("Title", style="yellow", justify="center")
        table.add_column(
            "url",
            style="green",
            justify="center",
            overflow="fold",
        )
        for post in posts["items"]:
            published_date = datetime.strptime(
                post["published"], "%Y-%m-%dT%H:%M:%S%z"
            ).date()
            table.add_row(post["id"], str(published_date), post["title"], post["url"])
        console.print(table)
        return posts
    else:
        typer.echo("No posts found.")


@blogger.command(help="Get the content of a post by its ID.")
def get_post_content(post_id: str):
    """Get the content of a Blogger post by its ID."""
    post = Blogger.get_post_content(post_id)
    if post:
        typer.echo(post["content"])
    else:
        typer.echo("Post not found.")


@blogger.command(help="Search for a post by a query.")
def search_post(query: str):
    """Search for a Blogger post by a query."""
    posts = Blogger.search_post(query)
    if posts:
        table = Table(title="Blogger Posts", show_lines=True)
        table.add_column("ID", style="cyan", justify="center", overflow="fold")
        table.add_column("Published", style="magenta", justify="center")
        table.add_column("Title", style="yellow", justify="center")
        table.add_column(
            "url",
            style="green",
            justify="center",
            overflow="fold",
        )
        for post in posts["items"]:
            published_date = datetime.strptime(
                post["published"], "%Y-%m-%dT%H:%M:%S%z"
            ).date()
            table.add_row(post["id"], str(published_date), post["title"], post["url"])
        console.print(table)
        return posts
    else:
        typer.echo("No posts found.")


@blogger.command(help="Insert a new post in the blog.")
def insert_post(title: str, content: str):
    """Insert a new Blogger post."""
    post = Blogger.insert_post(title, content)
    if post:
        typer.echo(f"Post inserted: {title}")
    else:
        typer.echo("Failed to insert post.")


@blogger.command(help="Delete a post by its ID.")
def delete_post_by_id(post_id: str):
    """Delete a Blogger post by its ID."""
    Blogger.delete_post_by_id(post_id)
    typer.echo(f"Post deleted: {post_id}")


@blogger.command(help="Delete a post by its title.")
def delete_post_by_title(title: str):
    """Delete a Blogger post by its title."""
    posts = Blogger.list_posts()
    for post in posts:
        if post["title"] == title:
            Blogger.delete_post_by_id(post["id"])
            typer.echo(f"Post deleted: {title}")
            return
    typer.echo("Post not found.")


@blogger.command(help="List all comments for a post by its ID.")
def list_comments(post_id: str):
    """List all comments for a Blogger post by its ID."""
    comments = Blogger.list_comments(post_id)
    print(comments)
    # if comments:
    #     for comment in comments:
    #         typer.echo(comment["content"])
    # else:
    #     typer.echo("No comments found.")


@blogger.command(help="Get a comment by its ID.")
def get_comment_by_id(post_id: str, comment_id: str):
    """Get a Blogger comment by its ID."""
    comment = Blogger.get_comment_by_id(post_id, comment_id)
    if comment:
        typer.echo(comment["content"])
    else:
        typer.echo("Comment not found.")


@blogger.command(help="List all comments for the blog.")
def list_comments_by_blog():
    """List all comments for the Blogger blog."""
    comments = Blogger.list_comments_by_blog()
    if comments:
        for comment in comments:
            typer.echo(comment["content"])
    else:
        typer.echo("No comments found.")


@blogger.command(help="Mark a comment as spam.")
def mark_as_spam(post_id: str, comment_id: str):
    """Mark a Blogger comment as spam."""
    Blogger.mark_as_spam(post_id, comment_id)
    typer.echo(f"Comment marked as spam: {comment_id}")


@blogger.command(help="Mark a comment as not spam.")
def mark_as_not_spam(post_id: str, comment_id: str):
    """Mark a Blogger comment as not spam."""
    Blogger.mark_as_not_spam(post_id, comment_id)
    typer.echo(f"Comment marked as not spam: {comment_id}")


if __name__ == "__main__":
    blogger()
