set_details_from_id_tool = {
        "name": "get_set_details_by_id",
        "description": "Fetch the details of a specific LEGO set using its set_id.",
        "parameters": {
            "type": "object",
            "properties": {
                "set_id": {
                    "type": "string",
                    "description": "The unique ID of the LEGO set."
                }
            },
            "required": ["set_id"],
            "additionalProperties": False
        }
    }
filter_sets_by_theme_tool = {
        "name": "filter_sets_by_theme",
        "description": "Retrieve all sets that belong to a specific theme.",
        "parameters": {
            "type": "object",
            "properties": {
                "theme_name": {
                    "type": "string",
                    "description": "The name of the theme to filter by."
                }
            },
            "required": ["theme_name"],
            "additionalProperties": False
        }
    }
average_price_by_theme_tool = {
        "name": "average_price_by_theme",
        "description": "Calculate the average retail price of LEGO sets for a given theme.",
        "parameters": {
            "type": "object",
            "properties": {
                "theme_name": {
                    "type": "string",
                    "description": "The name of the theme to calculate average price."
                }
            },
            "required": ["theme_name"],
            "additionalProperties": False
        }
    }
find_sets_by_year_range_tool = {
        "name": "find_sets_by_year_range",
        "description": "Get all sets released within a specific year range.",
        "parameters": {
            "type": "object",
            "properties": {
                "start_year": {
                    "type": "integer",
                    "description": "The starting year of the range."
                },
                "end_year": {
                    "type": "integer",
                    "description": "The ending year of the range."
                }
            },
            "required": ["start_year", "end_year"],
            "additionalProperties": False
        }
    }
top_n_sets_by_pieces_tool = {
        "name": "top_n_sets_by_pieces",
        "description": "Retrieve the top N LEGO sets with the highest number of pieces.",
        "parameters": {
            "type": "object",
            "properties": {
                "N": {
                    "type": "integer",
                    "description": "The number of top sets to retrieve."
                }
            },
            "required": ["N"],
            "additionalProperties": False
        }
    }
search_sets_by_name_tool = {
        "name": "search_sets_by_name",
        "description": "Search for LEGO sets based on a keyword in their name.",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "The keyword to search in set names."
                }
            },
            "required": ["keyword"],
            "additionalProperties": False
        }
    }
distribution_of_pieces_tool = {
        "name": "distribution_of_pieces",
        "description": "Return statistics on the distribution of pieces in LEGO sets.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
minifigures_count_summary_tool = {
        "name": "minifigures_count_summary",
        "description": "Calculate summary statistics for the number of minifigures across all sets.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
price_comparison_by_category_tool = {
        "name": "price_comparison_by_category",
        "description": "Compare average retail prices across different categories of LEGO sets.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
url_generator_tool = {
        "name": "url_generator",
        "description": "Generate a list of thumbnail and image URLs for a specific set or theme.",
        "parameters": {
            "type": "object",
            "properties": {
                "set_id": {
                    "type": "string",
                    "description": "The unique ID of the LEGO set (optional)."
                },
                "theme_name": {
                    "type": "string",
                    "description": "The name of the theme (optional)."
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
get_all_set_ids_tool = {
        "name": "get_all_set_ids",
        "description": "Return a list of all LEGO set IDs.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
get_currency_data_tool = {
    "name": "get_currency_data",
    "description": "Calculate the price in different currencies with today's currency rates",
    "parameters": {
        "type": "object",
        "properties": {
            "currency": {
                "type": "string",
                "description": "The currency we need to calculate price to"
            },
            "price": {
                "type": "string",
                "description": "The price in USD that we start from"
            }
        },
        "required": ["currency", "price"],
        "additionalProperties": False
    }
}



TOOLS = [{"type": "function", "function": set_details_from_id_tool},
         {"type": "function", "function": filter_sets_by_theme_tool},
         {"type": "function", "function": average_price_by_theme_tool},
         {"type": "function", "function": find_sets_by_year_range_tool},
         {"type": "function", "function": top_n_sets_by_pieces_tool},
         {"type": "function", "function": search_sets_by_name_tool},
         {"type": "function", "function": distribution_of_pieces_tool},
         {"type": "function", "function": minifigures_count_summary_tool},
         {"type": "function", "function": price_comparison_by_category_tool},
         {"type": "function", "function": url_generator_tool},
         {"type": "function", "function": get_all_set_ids_tool},
         {"type": "function", "function": get_currency_data_tool}
         ]

