# OmegaSolver-Optimized

Experimental community edition by feedee093, based on [OmegaSolver V5.0.0](https://github.com/OMEGAALPHA10/OmegaSolver) by OmegaAlpha10 (copyright 2025–2026, GPL-3.0). Not an official release.

## Changes / modificaciones
The uploaded upstream ZIP was inspected and its SHA-256 matched the published release. The repository distributes a source importer and a reproducible community patch, not a prebuilt application.

| Change | Status |
| --- | --- |
| Verify original ZIP before extraction | Implemented |
| Skip reparse-point ancestors before cleanup traversal and recheck before deletion | Source patch; best-effort, not race-proof |
| Avoid collecting unused directories during measurement | Source patch |
| Report cancellation consistently between cleanup targets | Source patch |
| Add read-only `--preview-cleanup` command (logical bytes, not guaranteed reclaimable space) | Source patch |
| Atomic UI log scheduling; cap visible history to 1,000 lines | Source patch |
| Point update checker to community repository | Source patch |
| Independent bounded read-only preview library | Implemented separately |
| Windows compilation, integration tests, benchmarks | Not yet verified |
| Privilege separation, rollback improvements and lazy loading | Pending |

## Build / compilación
Windows, .NET 10 SDK and Python 3 required. From the repository root:

```powershell
powershell -File scripts/import-upstream.ps1
python scripts/apply-community-patch.py upstream/OmegaSolver-5.0.0-source
dotnet build upstream/OmegaSolver-5.0.0-source/OmegaSolver.csproj -c Release
```

Review and test in a disposable Windows VM before running any destructive operation. The community build is unsigned; do not reuse the original publisher's certificate or official installer manifests. The upstream archive is available at [the original release](https://github.com/OMEGAALPHA10/OmegaSolver/releases/tag/v5.0.0). No measured speed or RAM improvement is claimed.

## Español
Se revisó el código C# original y se añadió un parche reproducible para reducir asignaciones durante la medición, reforzar comprobaciones de enlaces de directorio, mejorar la cancelación, limitar el historial visual de registros y añadir una vista previa por consola sin borrado. Estas modificaciones aún requieren compilación y pruebas en Windows. Se conserva la autoría y licencia originales. No es una versión oficial.
