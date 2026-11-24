// SPDX-License-Identifier: GPL-3.0-only
namespace OmegaSolver.Optimized;
public sealed record PreviewResult(long Bytes, int Files, int Skipped, bool Truncated);
public static class CleanupPreview
{
    // Read-only scan of the current user's temporary directory; never deletes.
    public static Task<PreviewResult> ScanAsync(CancellationToken token = default,
        int maxEntries = 100_000) => Task.Run(() => Scan(token, maxEntries), token);

    private static PreviewResult Scan(CancellationToken token, int maxEntries)
    {
        ArgumentOutOfRangeException.ThrowIfNegativeOrZero(maxEntries);
        var root = Path.GetFullPath(Path.GetTempPath());
        var profile = Path.GetFullPath(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile));
        if (!root.StartsWith(Path.TrimEndingDirectorySeparator(profile) + Path.DirectorySeparatorChar,
            StringComparison.OrdinalIgnoreCase))
            throw new InvalidOperationException("Temporary directory is outside user profile.");
        for (DirectoryInfo? p = new(root); p != null; p = p.Parent)
            if ((p.Attributes & FileAttributes.ReparsePoint) != 0)
                throw new IOException("Reparse point in temporary directory ancestry.");
        long bytes = 0;
        int files = 0, skipped = 0, visited = 0;
        var pending = new Stack<string>();
        pending.Push(root);
        while (pending.TryPop(out var dir))
        {
            token.ThrowIfCancellationRequested();
            try
            {
                if ((File.GetAttributes(dir) & FileAttributes.ReparsePoint) != 0)
                { skipped++; continue; }
                foreach (var entry in Directory.EnumerateFileSystemEntries(dir))
                {
                    token.ThrowIfCancellationRequested();
                    if (visited++ >= maxEntries) return new(bytes, files, skipped, true);
                    try
                    {
                        var attributes = File.GetAttributes(entry);
                        if ((attributes & FileAttributes.ReparsePoint) != 0) { skipped++; continue; }
                        if ((attributes & FileAttributes.Directory) != 0) pending.Push(entry);
                        else { bytes = checked(bytes + new FileInfo(entry).Length); files++; }
                    }
                    catch (Exception e) when (e is IOException or UnauthorizedAccessException) { skipped++; }
                }
            }
            catch (Exception e) when (e is IOException or UnauthorizedAccessException) { skipped++; }
        }
        return new(bytes, files, skipped, false);
    }
}
