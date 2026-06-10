import streamlit as st
import services
from config import APP_TITLE, CURRENCY


st.set_page_config(page_title=APP_TITLE, layout="wide")


def show_header():
    st.title(APP_TITLE)
    st.write("Crea una lista de regalos y permite que otros contribuyan con la cantidad que quieran.")


def gift_creation_form():
    st.subheader("Añadir nuevo regalo")
    with st.form("new_gift_form", clear_on_submit=True):
        name = st.text_input("Nombre del regalo")
        url = st.text_input("URL del producto")
        price = st.number_input("Precio total", min_value=0.0, step=1.0, format="%.2f")
        submitted = st.form_submit_button("Guardar regalo")

        if submitted:
            if not name or price <= 0:
                st.error("Indica un nombre y un precio válido.")
            else:
                services.add_gift(name, url, price)
                st.success("Regalo añadido correctamente.")


def contribution_form():
    st.subheader("Hacer una contribución")
    gifts = services.get_all_gifts()

    if not gifts:
        st.info("No hay regalos todavía.")
        return

    gift_options = {f"{g.name} ({g.remaining:.2f}{CURRENCY} restantes)": g.id for g in gifts}

    with st.form("contribution_form", clear_on_submit=True):
        selected = st.selectbox("Elige un regalo", list(gift_options.keys()))
        gift_id = gift_options[selected]

        amount = st.number_input("Cantidad a contribuir", min_value=0.0, step=1.0, format="%.2f")
        anonymous = st.checkbox("Contribución anónima", value=False)
        contributor_name = None if anonymous else st.text_input("Tu nombre (opcional)")

        submitted = st.form_submit_button("Contribuir")

        if submitted:
            if amount <= 0:
                st.error("La cantidad debe ser mayor que 0.")
            else:
                contribution = services.add_contribution(gift_id, amount, contributor_name, anonymous)
                st.success(f"Contribución registrada: {contribution.amount:.2f}{CURRENCY}")


def gifts_table():
    st.subheader("Resumen de regalos")
    gifts = services.get_all_gifts()

    if not gifts:
        st.info("No hay regalos todavía.")
        return

    data = []
    for g in gifts:
        data.append({
            "Nombre": g.name,
            "Precio total": f"{g.price:.2f}{CURRENCY}",
            "Contribuido": f"{g.total_contributed:.2f}{CURRENCY}",
            "Restante": f"{g.remaining:.2f}{CURRENCY}",
            "URL": g.url
        })

    st.table(data)

    with st.expander("Ver contribuciones"):
        for g in gifts:
            st.markdown(f"### {g.name}")
            if not g.contributions:
                st.write("Sin contribuciones todavía.")
                continue

            rows = []
            for c in g.contributions:
                display_name = "Anónimo" if c.anonymous or not c.contributor_name else c.contributor_name
                rows.append({
                    "Nombre": display_name,
                    "Cantidad": f"{c.amount:.2f}{CURRENCY}",
                    "Fecha": c.created_at
                })

            st.table(rows)


def main():
    show_header()

    col1, col2 = st.columns(2)
    with col1:
        gift_creation_form()
    with col2:
        contribution_form()

    st.markdown("---")
    gifts_table()


if __name__ == "__main__":
    main()
