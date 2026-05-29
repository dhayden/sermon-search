using Microsoft.EntityFrameworkCore;
using SermonSearch.Models;

namespace SermonSearch.Data;

public class SermonDbContext : DbContext
{
    public SermonDbContext(DbContextOptions<SermonDbContext> options) : base(options) { }

    public DbSet<PdfDocument> PdfDocuments => Set<PdfDocument>();
    public DbSet<PdfChunk>    PdfChunks    => Set<PdfChunk>();

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);

        builder.Entity<PdfDocument>(b =>
        {
            b.Property(x => x.Title).HasMaxLength(500).IsRequired();
            b.Property(x => x.FileName).HasMaxLength(500).IsRequired();
        });

        builder.Entity<PdfChunk>(b =>
        {
            b.HasOne(x => x.Document)
             .WithMany(x => x.Chunks)
             .HasForeignKey(x => x.DocumentId)
             .OnDelete(DeleteBehavior.Cascade);

            b.Property(x => x.Content).HasColumnType("nvarchar(max)");
            b.Property(x => x.Embedding).HasColumnType("nvarchar(max)");
        });
    }
}
