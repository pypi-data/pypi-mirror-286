DEFAULT_ALL_OPPORTUNITIES_QUERY = """
SELECT
    id,
    OpportunityId,
    StageName,
    Amount,
    ExpectedRevenue,
    CloseDate,
    Probability,
    ForecastCategory,
    PrevAmount,
    PrevCloseDate
FROM
    OpportunityHistory
"""
