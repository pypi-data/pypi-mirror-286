import click
import requests
import websockets
import asyncio

API_URL = "https://api.quotable.io/random"
WEBSOCKET_SERVER = "wss://echo.websocket.org"

@click.command()
@click.option('--author', default=None, help='Filter by author.')
@click.option('--send-to-websocket', is_flag=True, help='Send the quote to a WebSocket server.')
def main(author, send_to_websocket):
    """
    Fetches a random quote from the API.
    """
    params = {}
    if author:
        params['author'] = author

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        quote = data.get('content')
        author = data.get('author')
        click.echo(f"Random Quote: {quote}")
        if author:
            click.echo(f"- {author}")

        if send_to_websocket:
            asyncio.run(send_to_websocket_server(quote))

    except requests.RequestException as e:
        click.echo(f"Error fetching quote: {e}")

async def send_to_websocket_server(message):
    async with websockets.connect(WEBSOCKET_SERVER) as websocket:
        await websocket.send(message)
        click.echo(f"Sent to WebSocket: {message}")

        # Receiving and handling server response
        response = await websocket.recv()
        click.echo(f"Received from WebSocket: {response}")


if __name__ == '__main__':
    main()
