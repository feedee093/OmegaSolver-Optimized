# SPDX-License-Identifier: GPL-3.0-only
"""Apply reviewed community changes to the pinned upstream source."""
from pathlib import Path
import sys

root = Path(sys.argv[1])
def edit(path, changes):
    p = root / path
    text = p.read_text(encoding="utf-8-sig")
    for old, new in changes:
        if text.count(old) != 1:
            raise RuntimeError(f"Unexpected upstream content: {path}: {old[:80]}")
        text = text.replace(old, new, 1)
    p.write_text(text, encoding="utf-8")

edit("Modules/Cleanup/CleanupEngine.cs", [
("            cancellationToken.ThrowIfCancellationRequested();\n            try\n            {\n                await Task.Run", "            if (cancellationToken.IsCancellationRequested) { report.Cancelled = true; break; }\n            try\n            {\n                await Task.Run"),
("                var allDirs = new List<DirectoryInfo>();\n                foreach (FileInfo file in EnumerateFiles(directory, allDirs, cancellationToken))", "                foreach (FileInfo file in EnumerateFiles(directory, null, cancellationToken))"),
("        List<DirectoryInfo> allDirectories,", "        List<DirectoryInfo>? allDirectories,"),
("                    allDirectories.Add(subdirectory);", "                    allDirectories?.Add(subdirectory);"),
("        stack.Push(root);", "        if (!SafeAncestry(root)) yield break;\n        stack.Push(root);"),
("            FileSystemInfo[] entries;\n            try { entries = current.GetFileSystemInfos(\"*\", FlatEnumeration); }", "            if (!SafeAncestry(current)) continue;\n            FileSystemInfo[] entries;\n            try { entries = current.GetFileSystemInfos(\"*\", FlatEnumeration); }"),
("                if (!subdirectory.Exists) continue;", "                if (!subdirectory.Exists || !SafeAncestry(subdirectory)) continue;"),
("                length = file.Length;", "                file.Refresh();\n                if (Protected(file.FullName) || file.Directory is null || !SafeAncestry(file.Directory) ||\n                    (file.Attributes & FileAttributes.ReparsePoint) != 0) return false;\n                length = file.Length;"),
("    private static bool Protected(string path)", """    private static bool SafeAncestry(DirectoryInfo directory)
    {
        try
        {
            for (DirectoryInfo? current = directory; current != null; current = current.Parent)
            {
                current.Refresh();
                if (!current.Exists || (current.Attributes & FileAttributes.ReparsePoint) != 0)
                    return false;
            }
            return !Protected(directory.FullName);
        }
        catch { return false; }
    }

    private static bool Protected(string path)""")
])
edit("Cli.cs", [
('                case "--clean-safe":', '''                case "--preview-cleanup":
                    var targets = CleanupTargets.Build(Settings.Load(), deep: false);
                    var preview = CleanupEngine.MeasureAsync(targets, CancellationToken.None).GetAwaiter().GetResult();
                    Console.WriteLine($"files={preview.Files}|logical_bytes={preview.Bytes}");
                    return 0;
                case "--clean-safe":''')
])
edit("UI/MainWindow.xaml.cs", [
("    private bool _flushScheduled;", "    private int _flushScheduled;"),
("        if (_flushScheduled) return;\n        _flushScheduled = true;", "        if (System.Threading.Interlocked.Exchange(ref _flushScheduled, 1) != 0) return;"),
("        catch { _flushScheduled = false; }", "        catch { System.Threading.Interlocked.Exchange(ref _flushScheduled, 0); }"),
("        _flushScheduled = false;\n        bool changed = false;", "        System.Threading.Interlocked.Exchange(ref _flushScheduled, 0);\n        bool changed = false;"),
("        if (_logHistory.Count > 4000) _logHistory.RemoveRange(0, _logHistory.Count - 4000);\n        txtLog.Text = string.Join(Environment.NewLine, _logHistory);", "        if (_logHistory.Count > 1000) _logHistory.RemoveRange(0, _logHistory.Count - 1000);\n        txtLog.Text = string.Join(Environment.NewLine, _logHistory);")
])
edit("Core/UpdateService.cs", [
('public const string Repo = "OMEGAALPHA10/OmegaSolver";', 'public const string Repo = "feedee093/OmegaSolver-Optimized";')
])
print("Applied community patch. Build and test on Windows before use.")
