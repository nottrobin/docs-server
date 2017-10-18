# Core packages
import re
import yaml


class UrlMap:
    def __init__(self, filepath):
        """
        Given the path to a YAML file of redirect definitions like:

            hello/(?P<person>.*)?: "/say-hello?name={person}"
            google/(?P<search>.*)?: "https://google.com/?q={search}"

        Return a list of compiled Regex matches and destination strings:

            [
                (<regex>, "/say-hello?name={person}"),
                (<regex>, "https://google.com/?q={search}"),
            ]
        """

        self.matches = []

        with open(filepath) as redirects_file:
            for url_match, target_url in yaml.load(redirects_file).items():
                # Make sure all matches start with slash
                if url_match[0] != '/':
                    url_match = '/' + url_match

                self.matches.append(
                    (re.compile(url_match), target_url)
                )

    def get_target(self, url_path):
        for (match, target) in self.matches:
            result = match.fullmatch(url_path)

            if result:
                parts = {}
                for name, value in result.groupdict().items():
                    parts[name] = value or ''
                return target.format(**parts)
