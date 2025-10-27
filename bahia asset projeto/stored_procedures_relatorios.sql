-- Teste 1: Emolumentos Médios por Ativo
EXEC sp_EmolumentosMediosPorAtivo;

-- Teste 2: Emolumentos Totais por Dia
EXEC sp_EmolumentosTotaisPorDia;

-- Teste 3: Posição (Saldo)
-- ***ATENÇÃO: Use uma data que exista no seu input.csv (ex: '2025-09-30' ou '2025-09-27')
EXEC sp_PosicaoPorAtivoEData @DataFinal = '2025-09-30';