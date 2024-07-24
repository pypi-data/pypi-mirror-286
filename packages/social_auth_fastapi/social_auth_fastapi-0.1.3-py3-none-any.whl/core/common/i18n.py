import gc
import locale

from functools import lru_cache
from gettext import GNUTranslations
from subprocess import run
from typing import Any, Dict, Set


class BabelCli:
    __module_name__ = 'pybabel'

    def extract(self, watch_dir: str) -> None:
        run(
            [
                BabelCli.__module_name__,
                'extract',
                '-F',
                'babel.cfg',
                '-o',
                'locale/messages.pot',
                watch_dir,
            ]
        )

    def init(self, lang: str | None = None) -> None:
        run(
            [
                BabelCli.__module_name__,
                'init',
                '-i',
                'locale/messages.pot',
                '-d',
                'locale',
                '-l',
                lang or 'en_US',
            ]
        )

    def update(self, watch_dir: str | None = None) -> None:
        run(
            [
                BabelCli.__module_name__,
                'update',
                '-i',
                'locale/messages.pot',
                '-d',
                watch_dir or 'locale',
            ]
        )

    def compile(self, lang: str | None = None):
        run(
            [
                BabelCli.__module_name__,
                'compile',
                '-f',
                '-d',
                'locale',
                '-l',
                lang or 'en_US',
            ]
        )

    def run(self):
        from click import echo, group, option

        @group('cmd')
        def cmd():
            pass

        @cmd.command('extract')
        @option('-d', '--dir', 'dir', help='watch dir')
        def extract(dir):
            try:
                self.extract(dir)
            except Exception as err:
                echo(err)

        @cmd.command('init')
        @option(
            '-l',
            '--lang',
            'lang',
            help='locale directory name and path, default is en_US',
            default='en_US',
        )
        def init(lang: str | None = None):
            try:
                self.init(lang)
            except Exception as err:
                echo(err)

        @cmd.command('compile')
        @option(
            '-l',
            '--lang',
            'lang',
            help='locale directory name and path, default is en_US',
            default='en_US',
        )
        def compile(lang: str | None = None):
            try:
                self.compile(lang)
            except Exception as err:
                echo(err)

        @cmd.command('update')
        @option('-d', '--dir', 'dir', help='locale directory name and path')
        def update(dir: str | None = None):
            try:
                self.update(dir)
            except Exception as err:
                echo(err)

        cmd()


class I18N:
    instance: Any | None = None

    def __init__(self):
        I18N.instance = self
        self._locales: Dict[str, Set[GNUTranslations]] = {}
        self._language: str = self.set_language()

    def load_translations(self, translations: Dict[str, GNUTranslations]):
        for language, trans in translations.items():
            if language in self._locales:
                self._locales[language].add(trans)
            else:
                self._locales[language] = {trans}

    def set_language(self, language: str = None) -> str:
        language = language or locale.getlocale()[0] or 'en_US'
        self._language = 'en_US' if language.lower().startswith(('en_US', 'en')) else language
        I18N.gettext.cache_clear()  # clear cache after language has changed
        gc.collect()
        return self._language

    def get_language(self):
        return self._language

    @lru_cache()
    def gettext(self, value: str, language: str = None) -> str:
        language = language or self._language
        if language in self._locales:
            for trans in self._locales[language]:
                # noinspection PyProtectedMember
                if value in trans._catalog:  # type: ignore
                    value = trans.gettext(value)
        return value

    def __call__(self, value, language: str = None) -> str:
        return self.gettext(str(value), language)


i18n: I18N = I18N()
