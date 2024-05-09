#!/usr/bin/env python3

from __future__ import annotations


from nltk.corpus import wordnet

wordnet.ensure_loaded()

from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, Markdown


class TTD(App):
    """Searches ab dictionary API as-you-type."""

    CSS_PATH = "ttd.tcss"

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search for a word")
        with VerticalScroll(id="results-container"):
            yield Markdown(id="results")

    def on_mount(self) -> None:
        """Called when app starts."""
        # Give the input focus, so we can start typing straight away
        self.query_one(Input).focus()

    def on_input_changed(self, message: Input.Changed) -> None:
        if message.value:
            self.lookup_word(message.value)
        else:
            self.query_one("#results", Markdown).update("...")

    def lookup_word(self, word: str) -> None:
        synsets = wordnet.synsets(word)
        if len(synsets) <= 0:
            self.query_one("#results", Markdown).update(f'"{word}" not found :/')
            return

        markdown = ""
        for s in synsets:
            lemmas = s.lemmas()
            markdown += f"**{lemmas[0].name()}** ({s.pos()}): {s.definition()}\n\n"

            examples = s.examples()
            if len(examples) > 0:
                markdown += "**Examples:**\n"
                for ex in s.examples():
                    markdown += f"- {ex}\n"

            if len(lemmas) > 1:
                synonyms = []
                antonyms = []

                for l in lemmas:
                    if l.name() != word:
                        synonyms.append(f"- {l.name()}")

                        lemma_antonyms = l.antonyms()
                        if len(lemma_antonyms) > 0:
                            antonyms.append(f"- {lemma_antonyms[0].name()}")

                if len(synonyms) > 0:
                    markdown += "\n**Synonyms:**\n"
                    markdown += "\n".join(synonyms)

                if len(antonyms) > 0:
                    markdown += "\n\n**Antonyms:**\n"
                    markdown += "\n".join(antonyms)

            markdown += "\n---\n"

        markdown += "\n"
        self.query_one("#results", Markdown).update(markdown)


if __name__ == "__main__":
    app = TTD()
    app.run()
