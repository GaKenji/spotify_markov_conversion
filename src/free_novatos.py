def identificarFreeNovatos(df):

    novatos = df[
        (
            df["spotify_subscription_plan"] == "Free (ad-supported)"
        )
        &
        (
            df["spotify_usage_period"] == "Less than 6 months"
        )
    ].copy()

    print("\nANÁLISE DOS USUÁRIOS FREE NOVATOS")
    print(f"Total de usuários: {len(novatos)}")
    print("\nDisposição para assinar Premium:")
    print(
        novatos["premium_sub_willingness"]
        .value_counts()
    )

    return novatos