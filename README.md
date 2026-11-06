# XAML for Zed

WPF XAML support for [Zed](https://zed.dev): syntax highlighting, outline, snippets, build tasks, and
completion, diagnostics, hover and go to definition through
[wpf-xaml-ls](https://github.com/Zurisen/wpf-xaml-language-server).

C# itself is handled by Zed's `csharp` extension.

## Install the language server

The server is not on NuGet yet, so it is built from source. It needs the .NET 10 SDK:

```powershell
winget install Microsoft.DotNet.SDK.10
git clone https://github.com/Zurisen/wpf-xaml-language-server
cd wpf-xaml-language-server
dotnet pack src/WpfXaml.LanguageServer -c Release -o artifacts -p:WarningsNotAsErrors=NU1902
dotnet tool install -g --add-source artifacts WpfXaml.LanguageServer --prerelease
```

`WarningsNotAsErrors=NU1902` is needed because a dependency of the server (`MessagePack` 2.5.302) has a
[moderate-severity advisory](https://github.com/advisories/GHSA-qhrr-8q5h-9q3h), which otherwise fails the build.

Run `dotnet restore` in your WPF project: the server cannot load a project that has not been restored.

## Settings

All of them are optional. `initialization_options` are passed to the server as they are.

```json
{
  "lsp": {
    "wpf-xaml-ls": {
      "binary": { "path": "C:\\path\\to\\wpf-xaml-ls.exe" },
      "initialization_options": { "solution": "src/App.sln" }
    }
  }
}
```

## Tasks and snippets

- Tasks: `dotnet build`, `dotnet run` and `dotnet watch` for the project nearest to the open `.xaml` file.
- Snippets: `grid`, `style`, `datatemplate`, `bind`.

## Limitations

- WPF only: no `.axaml` (Avalonia), WinUI or MAUI.
- No designer or live preview: Zed's extension API has no custom panels.
- The server is an early alpha with no rename, find references, code actions or formatting.
- `{Binding ...}` is highlighted as a single token.

## Development

```powershell
pip install tree-sitter tree-sitter-xml
python tests/check_queries.py
```

Install locally with `zed: install dev extension`.

## License

MIT
