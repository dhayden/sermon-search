using Microsoft.EntityFrameworkCore;
using SermonSearch.Data;
using SermonSearch.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// SQL Server
builder.Services.AddDbContext<SermonDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Sermon search services
builder.Services.AddHttpClient<GeminiService>();
builder.Services.AddSingleton<IndexingQueue>();
builder.Services.AddSingleton<IndexingStatus>();
builder.Services.AddScoped<PdfIndexService>();
builder.Services.AddScoped<SearchService>();
builder.Services.AddHostedService<IndexingWorker>();

// CORS — allow React web + mobile
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
        policy.WithOrigins(
                builder.Configuration.GetSection("AllowedOrigins").Get<string[]>() ?? [])
              .AllowAnyHeader()
              .AllowAnyMethod());
});

var app = builder.Build();

// Run migrations on startup — safe to run repeatedly, never drops data
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<SermonDbContext>();
    db.Database.Migrate();
}

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseCors();
app.MapControllers();
app.Run();
