CREATE PROCEDURE sp_EmolumentosMediosPorAtivo
AS
BEGIN
    SELECT
        Ativo,
        AVG(Emolumento) AS EmolumentoMedio
    FROM
        Ordem
    GROUP BY
        Ativo;
END
GO


CREATE PROCEDURE sp_EmolumentosTotaisPorDia
AS
BEGIN
    SELECT
        Data_Trade,
        SUM(Emolumento) AS EmolumentoTotal
    FROM
        Ordem
    GROUP BY
        Data_Trade
    ORDER BY
        Data_Trade;
END
GO


CREATE PROCEDURE sp_PosicaoPorAtivoEData
    @DataFinal DATE,
    @Ativo VARCHAR(100) = NULL
AS
BEGIN
    SELECT
        Ativo,
        SUM(Quantidade) AS PosicaoTotal
    FROM
        Ordem
    WHERE
        Data_Trade <= @DataFinal
        AND (@Ativo IS NULL OR Ativo = @Ativo)
    GROUP BY
        Ativo
    HAVING
        SUM(Quantidade) <> 0
    ORDER BY
        Ativo;
END
GO