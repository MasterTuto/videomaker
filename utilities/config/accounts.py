from typing import TypedDict, Literal

from utilities.config.folder import LOGINS_FOLDER
from utilities.types.languages import SupportedLanguages

AccountTypes = Literal['reddit_stories', 'simple_splits']

class AccountTypeDict:
    type: str

VideoConfig = str

class Account(TypedDict):
    login_file: str
    type: AccountTypes
    lang: SupportedLanguages
    videos_config: list[VideoConfig]

    
REDDIT_ENGLISH_TIKTOK: Account = {
    "login_file": f'{LOGINS_FOLDER}/tiktok_reddit_pt.json',
    "type": 'reddit_stories',
    "lang": 'pt-br',
    'videos_config': [
        'showerthoughts_pt.json',
        'askreddit_pt.json',
        'nosleep_pt.json',
        'desabafos_pt.json',
        'perguntereddit_pt.json',
        'shittymoviedetails_pt.json',
        'tiodopave_pt.json',
    ]
}

INVESTMENTS_TIKTOK: Account = {
    "login_file": f"{LOGINS_FOLDER}/tiktok_series_pt.json",
    "type": 'simple_splits',
    "lang": 'pt-br',
    'videos_config': [
        'gemeos_investem.json',
        'renda_extra.json',
        'nerd_negocios.json',
        'marketing_digital.json',
        'atitude_alfa.json'
    ]
}

ACCOUNTS = [
    REDDIT_ENGLISH_TIKTOK,
    INVESTMENTS_TIKTOK
]