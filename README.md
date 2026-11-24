# OmegaSolver-Optimized
Community development project by feedee093, inspired by [OmegaSolver V5.0.0](https://github.com/OMEGAALPHA10/OmegaSolver) by OmegaAlpha10 (GPL-3.0). Not an official release.

## Implemented in this repository
- A verified-source bootstrap script: downloads the upstream source ZIP and checks its pinned SHA-256 before extraction.
- A standalone .NET 10 read-only cleanup preview component, with cancellation, bounded traversal, conservative path handling and no deletion.
- GPL-3.0 license and upstream attribution.

## Not yet integrated or tested
The upstream C# source could not be downloaded in the development environment. The preview component is independent and not wired into WPF. No performance improvements have been measured. Privilege separation, rollback, lazy loading, async UI integration and Windows CI remain pending.

## Start
On Windows, run `powershell -File scripts/import-upstream.ps1` from the repository root to retrieve the official source into upstream/. Inspect the source before building. Build the independent preview library using `dotnet build src/Preview/Preview.csproj` with .NET 10 SDK.

## Español
Proyecto comunitario experimental, no versión oficial. Se incorpora un importador con verificación SHA-256 y un componente de simulación de limpieza sin borrado, cancelable y con límites. No se ha integrado aún con la interfaz original ni se han validado mejoras de rendimiento.

Original: OmegaAlpha10, OmegaSolver V5.0.0, copyright 2025–2026. License: GPL-3.0.
