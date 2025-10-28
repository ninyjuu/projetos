var builder = WebApplication.CreateBuilder(args);

// Adiciona serviços ao contêiner.

// 1. Configuração do CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("CorsPolicy", builder => builder
        .AllowAnyOrigin()
        .AllowAnyMethod()
        .AllowAnyHeader());
});

// Adiciona suporte a Controllers (para o RelatoriosController)
builder.Services.AddControllers(); 
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configura o pipeline de requisição HTTP.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

// REMOVIDO: app.UseHttpsRedirection(); 

// 2. Aplica a política CORS AQUI
app.UseCors("CorsPolicy"); 

app.UseAuthorization();

// 3. Mapeia os endpoints do Controller
app.MapControllers();

app.Run();