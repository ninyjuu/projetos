using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Dapper;
using System.Data;
using AssetReportingAPI.Models;

namespace AssetReportingAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class RelatoriosController : ControllerBase
    {
        private readonly IConfiguration _config;
        private readonly string _connectionString;

        public RelatoriosController(IConfiguration config)
        {
            _config = config;
            _connectionString = _config.GetConnectionString("DefaultConnection");
        }

        [HttpGet("emolumentos/medio")]
        public async Task<IActionResult> GetEmolumentosMedios()
        {
            using (IDbConnection connection = new SqlConnection(_connectionString))
            {
                var resultados = await connection.QueryAsync<EmolumentoMedioModel>(
                    "sp_EmolumentosMediosPorAtivo",
                    commandType: CommandType.StoredProcedure);
                return Ok(resultados);
            }
        }

        [HttpGet("emolumentos/total")]
        public async Task<IActionResult> GetEmolumentosTotais()
        {
            using (IDbConnection connection = new SqlConnection(_connectionString))
            {
                var resultados = await connection.QueryAsync<EmolumentoTotalModel>(
                    "sp_EmolumentosTotaisPorDia",
                    commandType: CommandType.StoredProcedure);
                return Ok(resultados);
            }
        }

        [HttpGet("posicao")]
        public async Task<IActionResult> GetPosicao([FromQuery] DateTime? dataFinal, [FromQuery] string ativo = null)
        {
            var dataParaConsulta = dataFinal ?? DateTime.Today;

            using (IDbConnection connection = new SqlConnection(_connectionString))
            {
                var parametros = new
                {
                    DataFinal = dataParaConsulta.Date,
                    Ativo = ativo
                };

                var resultados = await connection.QueryAsync<PosicaoAtivoModel>(
                    "sp_PosicaoPorAtivoEData",
                    parametros,
                    commandType: CommandType.StoredProcedure);

                return Ok(resultados);
            }
        }
    }
}