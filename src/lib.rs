use zed_extension_api::{
    self as zed, serde_json::Value, settings::LspSettings, LanguageServerId, Result,
};

struct Xaml;

impl zed::Extension for Xaml {
    fn new() -> Self {
        Xaml
    }

    fn language_server_command(
        &mut self,
        id: &LanguageServerId,
        worktree: &zed::Worktree,
    ) -> Result<zed::Command> {
        // ponytail: settings + PATH only; add a NuGet download once the server is published there
        let binary = LspSettings::for_worktree(id.as_ref(), worktree)
            .ok()
            .and_then(|settings| settings.binary);
        let (path, args, extra_env) = match binary {
            Some(b) => (b.path, b.arguments, b.env),
            None => (None, None, None),
        };
        let command = path.or_else(|| worktree.which("wpf-xaml-ls")).ok_or(
            "wpf-xaml-ls not found. Install it (it needs .NET 10, see the README) \
             or set lsp.wpf-xaml-ls.binary.path",
        )?;

        let mut env = worktree.shell_env();
        env.extend(extra_env.into_iter().flatten());
        Ok(zed::Command {
            command,
            args: args.unwrap_or_default(),
            env,
        })
    }

    fn language_server_initialization_options(
        &mut self,
        id: &LanguageServerId,
        worktree: &zed::Worktree,
    ) -> Result<Option<Value>> {
        Ok(LspSettings::for_worktree(id.as_ref(), worktree)
            .ok()
            .and_then(|settings| settings.initialization_options))
    }
}

zed::register_extension!(Xaml);
