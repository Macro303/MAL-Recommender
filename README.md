# MAL Recommender
[![Version](https://img.shields.io/github/tag-pre/Macro303/MAL-Recommender.svg?label=version&style=flat-square)](https://github.com/Macro303/MAL-Recommender/releases)
[![Issues](https://img.shields.io/github/issues/Macro303/MAL-Recommender.svg?style=flat-square)](https://github.com/Macro303/MAL-Recommender/issues)
[![Contributors](https://img.shields.io/github/contributors/Macro303/MAL-Recommender.svg?style=flat-square)](https://github.com/Macro303/MAL-Recommender/graphs/contributors)
[![License](https://img.shields.io/github/license/Macro303/MAL-Recommender.svg?style=flat-square)](https://opensource.org/licenses/MIT)

*TODO*

## Built Using
 - [Python: 3.9.2](https://www.python.org/)
 - [pip: 21.0.1](https://pypi.org/project/pip/)
 - [requests: 2.25.1](https://pypi.org/project/requests/)
 - [ruamel.yaml: 0.17.2](https://pypi.org/project/ruamel.yaml/)

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
| `--min-score` | The minimum score a recommendation must have | 7.5 |
| `--min-recs` | The minimum number of recommendations it must have | 10 |
| `--max-recs` | The top number of recommendations to return | 100 |
| `--debug` | | False |

## Socials
[![Discord | The DEV Environment](https://invidget.switchblade.xyz/618581423070117932)](https://discord.gg/nqGMeGg)
