import pandas as pd
from datetime import datetime
import json
import requests

lego_data = pd.read_csv('./lego_sets.csv')


def get_set_details_by_id(set_id):
    """Fetch the details of a specific LEGO set using its set_id."""
    set_details = lego_data[lego_data['set_id'] == set_id]
    if not set_details.empty:
        return set_details.to_dict(orient='records')[0]
    else:
        return None  
    

def filter_sets_by_theme(theme_name):
    """Retrieve all sets that belong to a specific theme."""
    return lego_data[lego_data['theme'].str.contains(theme_name, case=False)].to_dict(orient='records')


def average_price_by_theme(theme_name):
    """Calculate the average retail price of LEGO sets for a given theme."""
    theme_sets = lego_data[lego_data['theme'].str.contains(theme_name, case=False)]
    avg_price = theme_sets['US_retailPrice'].mean()
    count = theme_sets.shape[0]
    return avg_price, count


def find_sets_by_year_range(start_year, end_year):
    """Get all sets released within a specific year range."""
    return lego_data[(lego_data['year'] >= start_year) & (lego_data['year'] <= end_year)].to_dict(orient='records')


def top_n_sets_by_pieces(N):
    """Retrieve the top N LEGO sets with the highest number of pieces."""
    return lego_data.nlargest(N, 'pieces').to_dict(orient='records')


def search_sets_by_name(keyword):
    """Search for LEGO sets based on a keyword in their name."""
    return lego_data[lego_data['name'].str.contains(keyword, case=False)].to_dict(orient='records')


def distribution_of_pieces():
    """Return statistics on the distribution of pieces in LEGO sets."""
    return lego_data['pieces'].describe().T


def minifigures_count_summary():
    """Calculate summary statistics for the number of minifigures across all sets."""
    return lego_data['minifigs'].describe().T


def price_comparison_by_category():
    """Compare average retail prices across different categories of LEGO sets."""
    return lego_data.groupby('category')['US_retailPrice'].mean()


def url_generator(set_id=None, theme_name=None):
    """Generate a list of thumbnail and image URLs for a specific set or theme."""
    if set_id:
        set_details = lego_data[lego_data['set_id'] == set_id]
        if not set_details.empty:
            return {
                "thumbnail": set_details['thumbnailURL'].values[0],
                "image": set_details['imageURL'].values[0]
            }
    elif theme_name:
        theme_sets = lego_data[lego_data['theme'].str.contains(theme_name, case=False, na=False)]
        return {
            "thumbnails": theme_sets['thumbnailURL'].tolist(),
            "images": theme_sets['imageURL'].tolist()
        }
    return None


def get_all_set_ids():
    """Return a list of all LEGO set IDs."""
    return lego_data['set_id'].unique().tolist()


def get_currency_data(currency: str, price: str) -> str:
    today = datetime.today().strftime('%Y-%m-%d')
    r = requests.get(f"https://{today}.currency-api.pages.dev/v1/currencies/eur.json")
    data = json.loads(r.text)
    currency = currency.lower()
    output_price = float(price.lstrip('$')) * (data['eur'][currency]) / data['eur']['usd']
    return f"{output_price:.2f}"


TOOL_REGISTRY = {
    "get_set_details_by_id": get_set_details_by_id,
    "filter_sets_by_theme": filter_sets_by_theme,
    "average_price_by_theme": average_price_by_theme,
    "find_sets_by_year_range": find_sets_by_year_range,
    "top_n_sets_by_pieces": top_n_sets_by_pieces,
    "search_sets_by_name": search_sets_by_name,
    "distribution_of_pieces": distribution_of_pieces,
    "minifigures_count_summary": minifigures_count_summary,
    "price_comparison_by_category": price_comparison_by_category,
    "url_generator": url_generator,
    "get_all_set_ids": get_all_set_ids,
    "get_currency_data": get_currency_data
}