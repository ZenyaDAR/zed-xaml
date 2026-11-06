"""Compile the tree-sitter queries and check the XAML-specific captures.

Usage: pip install tree-sitter tree-sitter-xml && python tests/check_queries.py
"""
from pathlib import Path

import tree_sitter_xml
from tree_sitter import Language, Parser, Query, QueryCursor

LANG = Language(tree_sitter_xml.language_xml())
QUERIES = Path(__file__).parent.parent / "languages" / "xaml"
SAMPLE = b"""<Window x:Class="App.Main" xmlns="http://x" Title="Hi">
  <Grid x:Name="Root" Margin="1">
    <Grid.RowDefinitions>
      <RowDefinition Height="Auto" />
    </Grid.RowDefinitions>
    <Button Content="{Binding Save}" Name="SaveButton" />
    <TextBlock Text="plain" />
  </Grid>
</Window>
"""


def text(node):
    return node.text.decode()


def run(name):
    query = Query(LANG, (QUERIES / f"{name}.scm").read_text(encoding="utf-8"))
    tree = Parser(LANG).parse(SAMPLE)
    assert not tree.root_node.has_error
    return QueryCursor(query).matches(tree.root_node)


def main():
    for name in ("highlights", "brackets", "indents", "outline"):
        run(name)  # raises on an invalid node name or a malformed pattern

    # Zed lets the later pattern win, so record the last capture for each node.
    last = {}
    for _, captures in sorted(run("highlights"), key=lambda m: m[0]):
        for capture, nodes in captures.items():
            for node in nodes:
                last[(node.start_byte, node.end_byte)] = (capture, text(node))
    found = set(last.values())
    assert ("keyword", "x:Name") in found
    assert ("keyword", "xmlns") in found
    assert ("property", "Grid.RowDefinitions") in found
    assert ("tag", "Grid") in found
    assert ("property", "Margin") in found
    assert ("string.special", '"{Binding Save}"') in found
    assert ("string", '"plain"') in found

    # Every element is listed once, plus one entry for each x:Name / Name.
    outline = sorted(
        (captures["item"][0].start_byte, text(captures["name"][0]))
        for _, captures in run("outline")
    )
    assert [name for _, name in outline] == [
        "Window",
        "Grid",
        '"Root"',
        "Grid.RowDefinitions",
        "RowDefinition",
        "Button",
        '"SaveButton"',
        "TextBlock",
    ], outline
    print("ok")


main()
