# Import required libraries
import cloudscraper  # For bypassing bot protection on websites
import json         # For working with JSON data
import requests     # For making HTTP requests
import re           # For working with regular expressions

def myhome(url):
    """
    Function to parse real estate data from MyHome.ge
    
    Args:
        url (str): URL of the listing page
        
    Returns:
        str: Formatted string with property information
    """
    try:
        # Create a scraper instance to bypass Cloudflare protection
        scraper = cloudscraper.create_scraper()
        
        # Perform GET request to the URL
        response = scraper.get(url)
        dirt = response.text  # Get the HTML content of the page
        
        # Extract JSON data from HTML using string splitting
        try:
            data = dirt.split('[{"state":{"data":{"result":true,"data":')[1].split(',"additional_information":["appear_rs_code"],"gallery":[{"image":{"large"')[0]
            
            # Check and fix JSON structure if incomplete
            if not data.strip().endswith("}"):
                data += "}}"
            
            # Parse JSON data
            parsed_json = json.loads(data)
            statement = parsed_json['statement']
        except (IndexError, json.JSONDecodeError) as e:
            print(f"Error parsing JSON data: {e}")
            return "Failed to process listing data"

        # Extract nearby places data
        nearby_places = statement.get("nearby_places", {})
        nearby_list = "\n".join(f"- {key}" for key in nearby_places.keys())

        # Format output with property information
        output = f"""
        🏠 Apartment for Sale in Batumi  
        📍 Address: {statement.get('address', 'Not specified')}  
        🏢 Property Type: Apartment (Studio)  
        🏷 Condition: {statement.get('condition', 'Not specified')}  
        📏 Area: {statement.get('area', 'Not specified')} m²  
        📐 Ceiling Height: {statement.get('height', 'Not specified') / 100:.2f} m  
        🔢 Floor: {statement.get('floor', 'Not specified')} out of {statement.get('total_floors', 'Not specified')}  

        ---

        💰 Price & Conditions  
        💵 Total Price: {statement.get('total_price', 'Not specified')} USD  
        💲 Price per m²: {statement['price']['2'].get('price_square', 'Not specified')} USD  
        🔄 Negotiable: ❌ (Not available)  
        🔁 Exchange: ❌ (Not possible)  

        ---

        🛏 Rooms  
        🚪 Apartment Type: 2-room (Studio + Bedroom)  
        🛏 Bedrooms: {statement.get('bedroom_type_id', 'Not specified')}  
        🛁 Bathrooms: {statement.get('bathroom_type_id', 'Not specified')}  
        🛋 Living Room: Studio-type  
        🌅 Balcony: ✅ ({statement.get('balcony_area', 'Not specified')} m²)  

        ---

        🔥 Comfort & Amenities  
        💧 Hot Water: {statement.get('hot_water_type', 'Not specified')}  
        🔥 Heating: Central  
        🚗 Parking: ✅ Available  

        ---

        📌 Location & Surroundings  
        🏙 City: {statement.get('city_name', 'Not specified')}  
        🏡 District: {statement.get('district_name', 'Not specified') if statement.get('district_name') else '(Not specified)'}  
        🏢 Residential Complex: {statement.get('urban_name', 'Not specified') if statement.get('urban_name') else '(Not specified)'}  
        🗺 Coordinates: [{statement.get('lat', 'Not specified')}, {statement.get('lng', 'Not specified')}]  
        🛍 Nearby Places:  
        {nearby_list}

        ---

        👤 Owner & Listing Details  
        🆔 Listing ID: {statement.get('id', 'Not specified')}  
        👤 Owner's Name: {statement.get('owner_name', 'Not specified')}  
        📅 Published Date: {statement.get('created_at', 'Not specified')}  
        📞 Phone: {statement.get('user_phone_number', 'Not specified')}  
        👀 Views: {statement.get('views', 'Not specified')}  
        """
        return output

    except Exception as e:
        print(f"Error processing MyHome URL: {e}")
        return "An error occurred while processing the request"

def korter(url):
    """
    Function to parse real estate data from Korter.ge
    
    Args:
        url (str): URL of the listing page
        
    Returns:
        str: Formatted string with property information
    """
    try:
        # Perform GET request to the URL
        r = requests.get(url)
        dirt = r.text  # Get the HTML content of the page
        
        # Extract raw JSON data from HTML
        raw_data = dirt.split('"isStaticPage":false},')[1].split(";\n")[0]
        raw_data = "{" + raw_data

        # Find complete JSON structure using regex
        match = re.search(r"\{.*\}", raw_data, re.DOTALL)
        if match:
            fixed_data = match.group(0)
        else:
            print("❌ JSON not found!")
            return "Failed to extract JSON data"

        # Fix incomplete JSON structure
        if fixed_data.count("{") > fixed_data.count("}"):
            fixed_data += "}"

        # Parse JSON data
        try:
            data = json.loads(fixed_data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return "Failed to process JSON data"

        # Extract property details
        address = data.get("layoutLandingStore", {}).get("layout", {}).get("address", "Not specified")
        property_type = data.get("layoutLandingStore", {}).get("layout", {}).get("propertyType", {}).get("name", "Not specified")
        condition = data.get("layoutLandingStore", {}).get("layout", {}).get("description", "Not specified")
        area = data.get("layoutLandingStore", {}).get("layout", {}).get("area", "Not specified")
        floor = data.get("layoutLandingStore", {}).get("layout", {}).get("floorsByHouse", [{}])[0].get("floorNumbers", ["Not specified"])[0]
        total_floors = data.get("layoutLandingStore", {}).get("layout", {}).get("floorsByHouse", [{}])[0].get("floorCount", "Not specified")
        price = data.get("layoutLandingStore", {}).get("layout", {}).get("price", "Not specified")
        bedrooms = data.get("layoutLandingStore", {}).get("layout", {}).get("bedroomCount", "Not specified")
        bathrooms = data.get("layoutLandingStore", {}).get("layout", {}).get("bathroomCount", "Not specified")
        parking = data.get("layoutLandingStore", {}).get("layout", {}).get("parking", "Not specified")
        city = data.get("building", {}).get("city", "Not specified")

        # Extract district information from geo objects
        geo_objects = data.get("building", {}).get("geoObjects", [])
        if len(geo_objects) > 1:
            district = geo_objects[1].get("nominative", "Not specified")
        elif len(geo_objects) == 1:
            district = geo_objects[0].get("nominative", "Not specified")
        else:
            district = "Not specified"

        # Extract listing details
        listing_id = data.get("layoutLandingStore", {}).get("objectId", "Not specified")
        owner_name = data.get("contactsStore", {}).get("seller", {}).get("name", "Not specified")
        phone = data.get("contactsStore", {}).get("seller", {}).get("phones", [{}])[0].get("displayNumber", "Not specified")
        publish_date = data.get("layoutLandingStore", {}).get("layout", {}).get("publishTime", "Not specified")

        # Format output with property information
        output = f"""
        🏠 Apartment Details
        📍 Address: {address}
        🏢 Property Type: {property_type}
        🏷 Condition: {condition}
        📏 Area: {area} m²
        🔢 Floor: {floor} out of {total_floors}

        ---

        💰 Price & Conditions
        💵 Total Price: {price} USD

        ---

        🛏 Rooms
        🚪 Apartment Type: {property_type}
        🛏 Bedrooms: {bedrooms}
        🛁 Bathrooms: {bathrooms}

        ---

        🔥 Comfort & Amenities
        🚗 Parking: {parking}

        ---

        📌 Location & Surroundings
        🏙 City: {city}
        🏡 District: {district}

        ---

        👤 Owner & Listing Details
        🆔 Listing ID: {listing_id}
        👤 Owner's Name: {owner_name}
        📅 Published Date: {publish_date}
        📞 Phone: {phone}
        """
        return output

    except Exception as e:
        print(f"Error processing Korter URL: {e}")
        return "An error occurred while processing the request"

def ssge(url):
    """
    Function to parse real estate data from home.ss.ge
    
    Args:
        url (str): URL of the listing page
        
    Returns:
        str: Formatted string with property information
    """
    try:
        # Perform GET request to the URL
        r = requests.get(url)
        dirt = r.text  # Get the HTML content of the page
        
        # Extract raw JSON data from HTML
        raw_data = dirt.split('"applicationData":')[1].split(',"hideHeaderMobile"')[0]

        # Find complete JSON structure using regex
        match = re.search(r"\{.*\}", raw_data, re.DOTALL)
        if match:
            fixed_data = match.group(0)
        else:
            print("❌ JSON not found!")
            return "Failed to extract JSON data"

        # Fix incomplete JSON structure
        if fixed_data.count("{") > fixed_data.count("}"):
            fixed_data += "}"

        # Parse JSON data
        try:
            data = json.loads(fixed_data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return "Failed to process JSON data"

        # Extract address details
        address = data.get("address", {})
        city = address.get("cityTitle", "Not specified")
        district = address.get("districtTitle", "Not specified")
        subdistrict = address.get("subdistrictTitle", "Not specified")
        street = address.get("streetTitle", "Not specified")
        street_number = address.get("streetNumber", "Not specified")

        # Extract pricing information
        price_usd = data.get("price", {}).get("priceUsd", "Not specified")
        price_per_m2 = data.get("price", {}).get("unitPriceUsd", "Not specified")

        # Extract property specifications
        total_area = data.get("totalArea", "Not specified")
        floor = data.get("floor", "Not specified")
        total_floors = data.get("floors", "Not specified")
        rooms = data.get("rooms", "Not specified")
        bedrooms = data.get("bedrooms", "Not specified")
        bathrooms = data.get("toilet", "Not specified")

        # Extract property type and condition
        property_type = data.get("realEstateType", "Not specified")
        condition = data.get("state", "Not specified")
        project = data.get("project", "Not specified")

        # Extract amenities
        heating = "Yes" if data.get("heating", False) else "No"
        hot_water = "Yes" if data.get("hotWater", False) else "No"
        air_conditioning = "Yes" if data.get("airConditioning", False) else "No"
        elevator = "Yes" if data.get("elevator", False) else "No"
        furniture = "Yes" if data.get("furniture", False) else "No"
        parking = "Yes" if data.get("garage", False) else "No"

        # Extract location coordinates
        latitude = data.get("locationLatitude", "Not specified")
        longitude = data.get("locationLongitude", "Not specified")

        # Extract owner and listing details
        owner_name = data.get("contactPerson", "Not specified")
        phone_numbers = [phone.get("phoneNumber", "Not specified") for phone in data.get("applicationPhones", [])]
        images = [img.get("fileName", "Not specified") for img in data.get("appImages", [])]
        views = data.get("viewCount", "Not specified")
        listing_id = data.get("applicationId", "Not specified")
        listing_status = data.get("status", "Not specified")

        # Format output with property information
        output = f"""
        🏠 Apartment Details
        📍 Address: {street} {street_number}, {subdistrict}, {district}, {city}
        🏢 Property Type: {property_type}
        🏷 Condition: {condition}
        📏 Area: {total_area} m²
        🔢 Floor: {floor} out of {total_floors}
        🛏 Rooms: {rooms}, Bedrooms: {bedrooms}
        🛁 Bathrooms: {bathrooms}

        ---

        💰 Price & Conditions
        💵 Total Price: {price_usd} USD
        💲 Price per m²: {price_per_m2} USD

        ---

        🔥 Comfort & Amenities
        🌡 Heating: {heating}
        💧 Hot Water: {hot_water}
        ❄ Air Conditioning: {air_conditioning}
        🛋 Furniture: {furniture}
        🚗 Parking: {parking}
        🛗 Elevator: {elevator}

        ---

        📌 Location & Surroundings
        🌍 Coordinates: [{latitude}, {longitude}]

        ---

        👤 Owner & Listing Details
        🆔 Listing ID: {listing_id}
        👤 Owner's Name: {owner_name}
        📞 Phone Numbers: {', '.join(phone_numbers)}
        👀 Views: {views}
        📌 Status: {listing_status}

        ---

        🖼 Images:
        {', '.join(images)}
        """
        return output

    except Exception as e:
        print(f"Error processing SSGE URL: {e}")
        return "An error occurred while processing the request"

# Main execution block
if __name__ == "__main__":
    try:
        # Prompt user for URL input
        url = input("Please enter your URL from MyHome.ge, Korter.ge, or home.ss.ge:\n")
        
        # Check URL and call appropriate parsing function
        if "https://www.myhome.ge/" in url:
            print(myhome(url))
        elif "https://korter.ge/" in url:
            print(korter(url))
        elif "https://home.ss.ge/" in url:
            print(ssge(url))
        else:
            print("Your URL is incorrect")
    except Exception as e:
        print(f"Error in main execution: {e}")