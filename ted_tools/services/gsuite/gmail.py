import typer
from google_suite import Gmail
from rich.console import Console
from rich.table import Table

console = Console()

gmail = typer.Typer()


@gmail.command(help="Lists all the labels available in the Gmail account.")
def list_labels():
    """List all Gmail labels."""
    labels = Gmail.list_labels()
    if labels:
        table = Table(title="Gmail Labels", show_lines=True)
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        for name, id in labels.items():
            table.add_row(id, name)
        console.print(table)
    else:
        typer.echo("No labels found.")


@gmail.command(help="Creates a new label in the Gmail account with the specified name.")
def create_label(label_name: str):
    """Create a new Gmail label."""
    label = Gmail.create_label(label_name)
    if label:
        typer.echo(f"Label created: {label_name}")
    else:
        typer.echo("Failed to create label.")


@gmail.command(
    help="Updates an existing Gmail label. Allows changing the label's name, visibility, and message visibility."
)
def update_label(
    label_name: str,
    new_label_name: str = typer.Option(
        None, "--new-name", help="The new name for the label."
    ),
    label_visibility: str = typer.Option(
        None, "--label-visibility", help="The new visibility setting for the label."
    ),
    message_visibility: str = typer.Option(
        None,
        "--message-visibility",
        help="The new message visibility setting for the label.",
    ),
):
    """Update a Gmail label."""
    label = Gmail.update_label(
        label_name, new_label_name, label_visibility, message_visibility
    )
    if label:
        typer.echo(f"Label updated: {new_label_name}")
    else:
        typer.echo("Failed to update label.")


@gmail.command(help="Deletes a specified Gmail label.")
def delete_label(label_name: str):
    """Delete a Gmail label."""
    Gmail.delete_label(label_name)
    typer.echo(f"Deleted label: {label_name}")


@gmail.command(
    help="Sends a new email message with optional file attachment and thread ID."
)
def send_message(
    from_sender: str,
    to: str,
    subject: str,
    message_text: str,
    file: str = typer.Option(
        None, "--file", help="Path to a file to attach to the message."
    ),
    thread_id: str = typer.Option(
        None, "--thread-id", help="Thread ID to send the message in."
    ),
):
    """Send a new email message."""
    message = Gmail.send_message(
        from_sender, to, subject, message_text, file, thread_id
    )
    if message:
        print(f"Message sent successfully: {subject}\n\n To: {to}")
    else:
        typer.echo("Failed to send message.")


@gmail.command()
def list_unread_messages(
    label_id: str = typer.Option(
        None, "--label-id", help="Label ID to filter messages by."
    ),
    sender: str = typer.Option(
        None, "--sender", help="Sender email address to filter messages by."
    ),
):
    """
    List unread messages filtered by label ID or sender. Each message is represented as an instance of the Message model, containing fields like msg_id, threadId, labelIds, snippet, historyId, internalDate, payload, sizeEstimate, and raw. \n\n \
    ```python \n\n \
    class Message(BaseModel): \n\n \
        msg_id: str\n\n \
        threadId: str\n\n \
        labelIds: list[str] | None\n\n \
        snippet: str | None\n\n \
        historyId: str | None\n\n \
        internalDate: str | None\n\n \
        payload: MessagePart | None\n\n \
        sizeEstimate: int | None\n\n \
        raw: str | None\n\n \n\n \
    class UserMessageList(BaseModel):\n\n \
        messages: list[Message] | None\n\n \
        nextPageToken: str | None\n\n \
        resultSizeEstimate: int | None\n\n \
    ```\n\n \
    """
    messages = Gmail.list_unread_messages(label_id, sender)
    if messages:
        for message in messages:
            typer.echo(f"Message ID: {message.msg_id}, Snippet: {message.snippet}")
    else:
        typer.echo("No unread messages found.")


@gmail.command(help="Marks a single message as read by its ID.")
def mark_read(msg_id: str):
    """Mark a single message as read."""
    Gmail.mark_read(msg_id)
    typer.echo(f"Message {msg_id} marked as read.")


@gmail.command(help="Marks a single message as unread by its ID.")
def mark_unread(msg_id: str):
    """Mark a single message as unread."""
    Gmail.mark_unread(msg_id)
    typer.echo(f"Message {msg_id} marked as unread.")


@gmail.command(
    help="Marks all unread messages as read, optionally filtered by label ID or sender."
)
def mark_all_read(
    label_id: str = typer.Option(
        None, "--label-id", help="Label ID to filter messages by."
    ),
    sender: str = typer.Option(
        None, "--sender", help="Sender email address to filter messages by."
    ),
):
    """Mark all unread messages as read, filtered by label ID or sender."""
    Gmail.mark_all_read(label_id, sender)
    typer.echo("Marked all messages as read.")


@gmail.command(
    help="Downloads attachments from messages filtered by label name or sender."
)
def download_attachment(
    label_name: str = typer.Option(
        None, "--label-name", help="Label name to filter messages by."
    ),
    sender: str = typer.Option(
        None, "--sender", help="Sender email address to filter messages by."
    ),
):
    """Download attachment from messages filtered by label name or sender."""
    path = Gmail.download_attachment(label_name, sender)
    if path:
        typer.echo(f"Attachment downloaded to: {path}")
    else:
        typer.echo("No attachment found or download failed.")


@gmail.command(help="Lists all Gmail filters.")
def list_filters():
    """List all Gmail filters."""
    filters = Gmail.list_filters()
    if filters:
        table = Table(title="Gmail Filters", show_lines=True)
        table.add_column("Filter ID", style="cyan", overflow="fold")
        table.add_column("Criteria", style="magenta")
        table.add_column("Action", style="yellow")
        for f in filters:
            table.add_row(f.id, str(f.criteria), str(f.action))
        console.print(table)
    else:
        typer.echo("No filters found.")


@gmail.command(help="Retrieves details of a specific Gmail filter by its ID.")
def get_filter(
    filter_id: str = typer.Option(
        None,
        "--filter-id",
        help="The ID of the filter to retrieve details for.",
    )
):
    """Get details of a specific filter by its ID."""
    filt = Gmail.get_filter(filter_id)
    if filt:
        table = Table(title="Gmail Filter Details", show_lines=True)
        table.add_column("Filter ID", style="cyan", overflow="fold")
        table.add_column("Criteria", style="magenta")
        table.add_column("Action", style="yellow")
        table.add_row(filt.id, str(filt.criteria), str(filt.action))
        console.print(table)
    else:
        typer.echo("Failed to retrieve filter details.")


@gmail.command(
    help="Creates a new Gmail filter based on specified criteria such as label name, sender, subject, and query."
)
def create_filter(
    label_name: str = typer.Option(
        None, "--label-name", help="The name of the label to add to the filter."
    ),
    remove_from_inbox: bool = typer.Option(
        False,
        "--remove-from-inbox",
        help="Whether to skip the inbox for filtered emails.",
    ),
    filter_from: str = typer.Option(
        None, "--from", help="The email address of the sender to add to the filter."
    ),
    subject: str = typer.Option(
        None, "--subject", help="The subject of the email message to add to the filter."
    ),
    query: str = typer.Option(
        None,
        "--query",
        help="All emails that DO contain the string i.e. 'secret knock'",
    ),
    negatedQuery: str = typer.Option(
        None,
        "--negated-query",
        help="All emails that do not contain the string i.e. 'secret knock'",
    ),
):
    """Create a new Gmail filter."""
    _filter = Gmail.create_filter(
        label_name, remove_from_inbox, filter_from, subject, query, negatedQuery
    )
    if _filter:
        table = Table(title="Gmail Filter Created", show_lines=True)
        table.add_column("Filter ID", style="cyan")
        table.add_column("Criteria", style="magenta")
        table.add_column("Action", style="yellow")
        table.add_row(_filter.id, str(_filter.criteria), str(_filter.action))
        console.print(table)
    else:
        typer.echo("Failed to create filter.")


@gmail.command(help="Deletes a specified Gmail filter by its ID.")
def delete_filter(filter_id: str):
    """Delete a Gmail filter."""
    Gmail.delete_filter(filter_id)
    typer.echo(f"Filter deleted: {filter_id}")


if __name__ == "__main__":
    gmail()
