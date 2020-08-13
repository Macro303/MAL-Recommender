<img src="https://raw.githubusercontent.com/Macro303/MAL-Recommender/main/logo.png" align="left" width="120" height="120" alt="MAL Recommender Logo"/>

# MAL Recommender
[![Version](https://img.shields.io/github/tag-pre/Macro303/MAL-Recommender.svg?label=version&style=flat-square)](https://github.com/Macro303/MAL-Recommender/releases)
[![Issues](https://img.shields.io/github/issues/Macro303/MAL-Recommender.svg?style=flat-square)](https://github.com/Macro303/MAL-Recommender/issues)
[![Contributors](https://img.shields.io/github/contributors/Macro303/MAL-Recommender.svg?style=flat-square)](https://github.com/Macro303/MAL-Recommender/graphs/contributors)

*Description*

## Built Using
 - [Python: 3.8.5](https://www.python.org/)
 - [pip: 20.2.2](https://pypi.org/project/pip/)
 - [PyInstaller: 4.0](https://pypi.org/project/PyInstaller/)
 - [requests: 2.24.0](https://pypi.org/project/requests/)
 - [PyYAML: 5.3.1](https://pypi.org/project/PyYAML/)

## Execution
1. Create an ID with the App Type `other` on [My Anime List (MAL)](https://myanimelist.net/apiconfig)
2. Run the following:
    ```bash
    $ pip install -r requirements.txt
    $ python -m Recommender
    ```
3. Put your Client ID into the generated **config.yaml**
4. Run the following:
    ```bash
    $ python -m Recommender
    ```

## Arguments
*You can find all these by using the `-h` or `--help` argument*

| Arg | Description | Default |
| --- | ----------- | ------- |
| `--username` | The MAL username of the Watchlist to get | @me |
| `--score` | Minimum score to check Recommendations against | 7.5 |
| `--recs` | Minimum Recommendations to add to the list | 10 |
| `--max` | Maximum amount of Recommendations returned | 100 |

## Socials
[![Discord | The Playground](https://discord.com/api/v6/guilds/618581423070117932/widget.png?style=banner2)](https://discord.gg/nqGMeGg)
