APP_TITLE = "Lista de regalos colaborativa"
CURRENCY = "¥"
gift_options = {f"{g.name} ({g.remaining:.2f}{CURRENCY} restantes)": g.id for g in gifts}
