import argparse
import concurrent.futures

import requests
from bs4 import BeautifulSoup as bs


class MediaExtractor:
    """
    A class that extracts and downloads audio files of Valorant agent voice lines.
    """

    def __init__(self, output_path) -> None:
        """
        Initializes a MediaExtractor object.

        Args:
            output_path (str): The output path for the downloaded files.
        """
        self.baseurl = "https://valorant.fandom.com"
        self.agentoverview_url = self.baseurl + "/wiki/Agents"
        self.output_path = output_path

    def get_agent_quotes_urls(self):
        """
        Retrieves the URLs of the agent quotes pages from the Valorant Fandom website.

        Returns:
            agent_quotes_urls (list): A list of URLs of the agent quotes pages.
        """
        agent_quotes_urls = []
        response = requests.get(self.agentoverview_url, timeout=5)
        if response.status_code == 200:
            content = bs(response.content, "html.parser")
            quotes_links = content.find_all('a', title=lambda t: t and 'Quotes' in t)
            for link in quotes_links:
                agent_quotes_urls.append(self.baseurl + link['href'])
        return agent_quotes_urls

    def get_quotes(self, quotes_url, AgentName):
        """
        Retrieves the audio URLs of the agent voice lines from a specific quotes page.

        Args:
            quotes_url (str): The URL of the quotes page.
            AgentName (str): The name of the Valorant agent.

        Returns:
            audio_urls (list): A list of audio URLs of the agent voice lines.
        """
        audio_urls = []
        response = requests.get(quotes_url, timeout=5)
        if response.status_code == 200:
            content = bs(response.text, "html.parser")
            audio_buttons = content.find_all('span', class_='audio-button')
            for button in audio_buttons:
                audio = button.find('audio')
                if audio:
                    url = audio['src']
                    filename = url.split('/')[7]
                    if filename.startswith(AgentName):
                        audio_urls.append(url)
        return audio_urls

    def download_audio(self, url):
        """
        Downloads the audio file from the given URL.

        Args:
            url (str): An audio URL.
        """
        filename = url.split('/')[7]
        response = requests.get(url, stream=True, timeout=5)
        with open(f"{self.output_path}/{filename}", 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

    def main(self, agentname):
        """
        The main function that orchestrates the extraction and downloading of agent voice lines.

        Args:
            AgentName (str): The name of the Valorant agent.
        """
        quotes_urls = self.get_agent_quotes_urls()
        quotes = []
        for url in quotes_urls:
            quotes += self.get_quotes(url, agentname)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.download_audio, quotes)
        print(f"Found {len(quotes)} audio files for {agentname}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Valorant agent voice lines.')
    parser.add_argument('path', type=str, help='The output path for the downloaded files.')
    parser.add_argument('agent', type=str, help='The name of the Valorant agent.')
    args = parser.parse_args()

    quotesfinder = MediaExtractor(args.path)
    quotesfinder.main(args.agent)
