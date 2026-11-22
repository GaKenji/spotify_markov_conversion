def analisarFrequencias(df):
    print("\nFREQUÊNCIA DOS PLANOS DE ASSINATURA")

    frequencia_planos = df[
        "spotify_subscription_plan"
    ].value_counts()

    print(frequencia_planos)
    print("\nDISPOSIÇÃO PARA ASSINAR PREMIUM")

    frequencia_interesse = df[
        "premium_sub_willingness"
    ].value_counts()

    print(frequencia_interesse)
    print("\nTEMPO DE UTILIZAÇÃO")

    frequencia_tempo = df[
        "spotify_usage_period"
    ].value_counts()

    print(frequencia_tempo)

    return {
        "planos": frequencia_planos,
        "interesse": frequencia_interesse,
        "tempo": frequencia_tempo
    }