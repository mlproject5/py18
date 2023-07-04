import streamlit as st
import requests
st.set_page_config(page_title='Currency', page_icon='c.png', layout="centered", initial_sidebar_state="auto", menu_items=None)

def curr():
    def currency_converter(amount, from_currency, to_currency):
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url)
            data = response.json()
            conversion_rate = data['rates'][to_currency]
            converted_amount = amount * conversion_rate
            return converted_amount
        except KeyError:
            st.warning("Invalid currency code. Please enter valid ISO currency codes.")
            return None
        except requests.exceptions.RequestException:
            st.warning("Failed to fetch exchange rates. Please check your internet connection.")
            return None

    def get_currency_names():
        try:
            url = "https://restcountries.com/v2/all"
            response = requests.get(url)
            data = response.json()
            currency_names = {}
            for country in data:
                if 'currencies' in country:
                    for currency in country['currencies']:
                        code = currency['code']
                        name = currency['name']
                        currency_names[code] = name
            return currency_names
        except requests.exceptions.RequestException:
            st.warning("Failed to fetch currency names. Please check your internet connection.")
            return None

    def main():
        st.markdown(
            "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 32px;'>Currency Price "
            "Tracker</h1></center>",
            unsafe_allow_html=True)

        currency_names = get_currency_names()
        if currency_names is not None:
            currency_codes = list(currency_names.keys())
            currency_codes.insert(0, "Select a currency")
            from_currency = st.selectbox("Convert from:", currency_codes, format_func=lambda code: currency_names[
                code] if code in currency_names else code)
            to_currency = st.selectbox("Convert to:", currency_codes, format_func=lambda code: currency_names[
                code] if code in currency_names else code)

            if from_currency != "Select a currency" and to_currency != "Select a currency":
                amount = st.number_input("Enter amount:", value=1.00, min_value=0.01)

                if st.button("Track"):
                    converted_amount = currency_converter(amount, from_currency, to_currency)
                    if converted_amount is not None:
                        st.success(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
        else:
            st.warning("Failed to fetch currency names. Please check your internet connection.")

    if __name__ == "__main__":
        main()


def crypto():
    def cryptocurrency_tracker(crypto_id):
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
            response = requests.get(url)
            data = response.json()
            if crypto_id in data:
                price = data[crypto_id]["usd"]
                return price
            else:
                st.warning("Invalid cryptocurrency ID. Please enter a valid ID.")
                return None
        except requests.exceptions.RequestException:
            st.warning("Failed to fetch cryptocurrency price. Please check your internet connection.")
            return None

    def get_cryptocurrency_ids():
        try:
            url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
            response = requests.get(url)
            data = response.json()
            crypto_ids = {}
            for crypto in data:
                crypto_ids[crypto["id"]] = crypto["name"]
            return crypto_ids
        except requests.exceptions.RequestException:
            st.warning("Failed to fetch cryptocurrency IDs. Please check your internet connection.")
            return None

    def main():
        st.markdown(
            "<center><h1 style='font-family: Comic Sans MS; font-weight: 300; font-size: 32px;'>Cryptocurrency Price Tracker</h1></center>",
            unsafe_allow_html=True)

        crypto_ids = get_cryptocurrency_ids()
        if crypto_ids is not None:
            crypto_ids_list = list(crypto_ids.keys())
            crypto_ids_list.insert(0, "Select a cryptocurrency")
            crypto_id = st.selectbox("Select cryptocurrency:", crypto_ids_list,
                                     format_func=lambda id: crypto_ids[id] if id in crypto_ids else id)

            if crypto_id != "Select a cryptocurrency":
                if st.button("Track"):
                    price = cryptocurrency_tracker(crypto_id)
                    if price is not None:
                        st.success(f"The current price of {crypto_ids[crypto_id]} is **${price:.2f}**")
        else:
            st.warning("Failed to fetch cryptocurrency IDs. Please check your internet connection.")

    if __name__ == "__main__":
        main()






st.sidebar.markdown("""
            <style>
                .sidebar-text {
                    text-align: center;
                    font-weight: 600;
                    font-size: 32px;
                    font-family: 'Comic Sans MS', cursive;
                }
            </style>
            <p class="sidebar-text">Identify</p>
            <br/>
        """, unsafe_allow_html=True)

st.sidebar.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5kljjA5bXv7R73_ppf7caHcv_2Ngpinj1ZQ&usqp=CAU")
st.sidebar.markdown(
            "<center><h1 style='font-family: Comic Sans MS; font-weight: 600; font-size: 18px;'>National "
            "Identification</h1></center>",
            unsafe_allow_html=True)
sidebar_options = {
    "Currency": curr,
    "Cryptocurrency": crypto,
}

selected_option = st.sidebar.radio("Select a URL shortener:", list(sidebar_options.keys()))

if "prev_option" not in st.session_state:
    st.session_state.prev_option = selected_option

if st.session_state.prev_option != selected_option:
    if selected_option == "Currency":
        st.session_state.long_url_1 = ""
    elif selected_option == "Cryptocurrency":
        st.session_state.long_url_2 = ""


st.session_state.prev_option = selected_option
sidebar_options[selected_option]()
