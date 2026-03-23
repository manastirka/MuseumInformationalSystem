#!/usr/bin/env python3
"""
Convert bird ringing coordinates to standard decimal degree format
Handles multiple input formats and converts to: "latitude, longitude"
"""

import sqlite3
import re

DB_PATH = 'data/bird_ringing.db'

def dms_to_decimal(degrees, minutes, seconds, direction):
    """Convert degrees, minutes, seconds to decimal degrees."""
    decimal = float(degrees) + float(minutes) / 60 + float(seconds) / 3600

    # Apply direction (S and W are negative)
    if direction in ['S', 'W']:
        decimal = -decimal

    return decimal

def parse_coordinates(coord_string):
    """
    Parse various coordinate formats and return standardized decimal degrees.

    Returns: (latitude, longitude) as floats, or None if parsing fails
    """
    if not coord_string or coord_string.strip() == '':
        return None

    coord_string = coord_string.strip()

    # Skip invalid/placeholder entries
    if coord_string.upper() in ['U.M.', 'N/A', 'UNKNOWN', '']:
        return None

    # Skip text descriptions instead of coordinates
    if any(word in coord_string.lower() for word in ['uzete', 'uzeti', 'mere', 'podaci', 'nema']):
        return None

    # Replace Cyrillic characters with Latin equivalents first
    coord_string = coord_string.replace('С', 'N').replace('Е', 'E').replace('с', 'N').replace('е', 'E')
    # Replace fancy Unicode quotes with regular ones
    coord_string = coord_string.replace('"', '"').replace('"', '"').replace(''', "'").replace(''', "'")
    # Fix common typos
    coord_string = coord_string.replace('o20', '020').replace('O20', '020')  # Letter O instead of zero

    # Format 1: Decimal degrees with N/S/E/W
    # Example: "45.2363554N 20.3153327E" or "45.2363554 N 20.3153327 E"
    pattern1 = r'([0-9.]+)\s*([NS])\s+([0-9.]+)\s*([EW])'
    match = re.search(pattern1, coord_string, re.IGNORECASE)
    if match:
        lat = float(match.group(1))
        lat_dir = match.group(2).upper()
        lon = float(match.group(3))
        lon_dir = match.group(4).upper()

        if lat_dir == 'S':
            lat = -lat
        if lon_dir == 'W':
            lon = -lon

        return (lat, lon)

    # Format 2: DMS (Degrees Minutes Seconds)
    # Example: "46°05´17,69´´ N  20°03´03,15´´E"
    # Note: Uses ´ (acute accent) instead of ' (apostrophe)
    pattern2 = r'([0-9]+)°([0-9]+)´([0-9,\.]+)´´\s*([NS])\s+([0-9]+)°([0-9]+)´([0-9,\.]+)´´\s*([EW])'
    match = re.search(pattern2, coord_string, re.IGNORECASE)
    if match:
        lat_deg = match.group(1)
        lat_min = match.group(2)
        lat_sec = match.group(3).replace(',', '.')  # Handle comma as decimal separator
        lat_dir = match.group(4).upper()

        lon_deg = match.group(5)
        lon_min = match.group(6)
        lon_sec = match.group(7).replace(',', '.')
        lon_dir = match.group(8).upper()

        lat = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
        lon = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)

        return (lat, lon)

    # Format 3: DMS with regular degree symbol (º) and quotes
    # Example: "N 45º  01'  01.08"  E 020º  57'  29.33""
    pattern3 = r'([NS])\s*([0-9]+)º\s*([0-9]+)[\'\´]\s*([0-9.]+)"\s*([EW])\s*([0-9]+)º\s*([0-9]+)[\'\´]\s*([0-9.]+)"'
    match = re.search(pattern3, coord_string, re.IGNORECASE)
    if match:
        lat_dir = match.group(1).upper()
        lat_deg = match.group(2)
        lat_min = match.group(3)
        lat_sec = match.group(4)

        lon_dir = match.group(5).upper()
        lon_deg = match.group(6)
        lon_min = match.group(7)
        lon_sec = match.group(8)

        lat = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
        lon = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)

        return (lat, lon)

    # Format 4: Standard DMS with ° ' "
    # Example: "45°18'36.81"N,  19°50'22.61"E"
    pattern4 = r'([0-9]+)°([0-9]+)[\'\´]([0-9.]+)"([NS])[,\s]+([0-9]+)°([0-9]+)[\'\´]([0-9.]+)"([EW])'
    match = re.search(pattern4, coord_string, re.IGNORECASE)
    if match:
        lat_deg = match.group(1)
        lat_min = match.group(2)
        lat_sec = match.group(3)
        lat_dir = match.group(4).upper()

        lon_deg = match.group(5)
        lon_min = match.group(6)
        lon_sec = match.group(7)
        lon_dir = match.group(8).upper()

        lat = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
        lon = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)

        return (lat, lon)

    # Format 5: Compressed format +DDMMSS+DDDMMSS
    # Example: "+460240+0200579"
    pattern5 = r'^([+-])([0-9]{2})([0-9]{2})([0-9]{2})([+-])([0-9]{3})([0-9]{2})([0-9]{2})$'
    match = re.search(pattern5, coord_string)
    if match:
        lat_sign = match.group(1)
        lat_deg = match.group(2)
        lat_min = match.group(3)
        lat_sec = match.group(4)

        lon_sign = match.group(5)
        lon_deg = match.group(6)
        lon_min = match.group(7)
        lon_sec = match.group(8)

        lat_dir = 'S' if lat_sign == '-' else 'N'
        lon_dir = 'W' if lon_sign == '-' else 'E'

        lat = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
        lon = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)

        return (lat, lon)

    # Format 6: Already in decimal format "lat, lon" or "lat lon"
    pattern6 = r'^([0-9.-]+)[,\s]+([0-9.-]+)$'
    match = re.search(pattern6, coord_string)
    if match:
        lat = float(match.group(1))
        lon = float(match.group(2))

        # Validate ranges
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return (lat, lon)

    # Format 7: Decimal degrees with direction first
    # Example: "N 44.760123° E 21.363646°"
    pattern7 = r'([NS])\s*([0-9.]+)°?\s+([EW])\s*([0-9.]+)°?'
    match = re.search(pattern7, coord_string, re.IGNORECASE)
    if match:
        lat_dir = match.group(1).upper()
        lat = float(match.group(2))
        lon_dir = match.group(3).upper()
        lon = float(match.group(4))

        if lat_dir == 'S':
            lat = -lat
        if lon_dir == 'W':
            lon = -lon

        return (lat, lon)

    # Format 8: Space-separated DMS without symbols
    # Example: "N 44 55 19; E 21 08 63"
    pattern8 = r'([NS])\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s*;\s*([EW])\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)'
    match = re.search(pattern8, coord_string, re.IGNORECASE)
    if match:
        lat_dir = match.group(1).upper()
        lat_deg = match.group(2)
        lat_min = match.group(3)
        lat_sec = match.group(4)

        lon_dir = match.group(5).upper()
        lon_deg = match.group(6)
        lon_min = match.group(7)
        lon_sec = match.group(8)

        lat = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
        lon = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)

        return (lat, lon)

    # Format 9: Decimal minutes (degrees and decimal minutes)
    # Example: "N 44° 45.347' E 21° 33.154'"
    pattern9 = r'([NS])\s*([0-9]+)°\s*([0-9.]+)[\'\´]\s+([EW])\s*([0-9]+)°\s*([0-9.]+)[\'\´]'
    match = re.search(pattern9, coord_string, re.IGNORECASE)
    if match:
        lat_dir = match.group(1).upper()
        lat_deg = match.group(2)
        lat_min = match.group(3)

        lon_dir = match.group(4).upper()
        lon_deg = match.group(5)
        lon_min = match.group(6)

        # Convert decimal minutes to decimal degrees
        lat = float(lat_deg) + float(lat_min) / 60
        lon = float(lon_deg) + float(lon_min) / 60

        if lat_dir == 'S':
            lat = -lat
        if lon_dir == 'W':
            lon = -lon

        return (lat, lon)

    # Format 10: DMS missing N prefix (assume northern hemisphere)
    # Example: "41° 4'14.66" E20°51'37.73""
    pattern10 = r'^([0-9]+)°\s*([0-9]+)[\'\´]([0-9.]+)"\s*([EW])?\s*([0-9]+)°\s*([0-9]+)[\'\´]([0-9.]+)"'
    match = re.search(pattern10, coord_string)
    if match:
        lat_deg = match.group(1)
        lat_min = match.group(2)
        lat_sec = match.group(3)
        lon_dir = match.group(4).upper() if match.group(4) else 'E'
        lon_deg = match.group(5)
        lon_min = match.group(6)
        lon_sec = match.group(7)

        # Assume northern hemisphere for Serbia
        lat = dms_to_decimal(lat_deg, lat_min, lat_sec, 'N')
        lon = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)

        return (lat, lon)

    # Format 11: Decimal minutes with direction AFTER value
    # Example: "44° 48.512'N E  20° 28.519'E" (also handles fancy quotes)
    pattern11 = r'([0-9]+)°\s*([0-9.]+)[\'\´][""]?\s*([NS])\s+([EW])?\s*([0-9]+)°\s*([0-9.]+)[\'\´][""]?'
    match = re.search(pattern11, coord_string, re.IGNORECASE)
    if match:
        lat_deg = match.group(1)
        lat_min = match.group(2)
        lat_dir = match.group(3).upper()
        lon_dir = match.group(4).upper() if match.group(4) else 'E'
        lon_deg = match.group(5)
        lon_min = match.group(6)

        # Convert decimal minutes to decimal degrees
        lat = float(lat_deg) + float(lat_min) / 60
        lon = float(lon_deg) + float(lon_min) / 60

        if lat_dir == 'S':
            lat = -lat
        if lon_dir == 'W':
            lon = -lon

        return (lat, lon)

    # Format 11b: DMS with spaces between components
    # Example: "46° 4'30.06"N,  19°43'7.48"E"
    pattern11b = r'([0-9]+)°\s*([0-9]+)[\'\´]([0-9.]+)"([NS])[,\s]+([0-9]+)°\s*([0-9]+)[\'\´]([0-9.]+)"([EW])'
    match = re.search(pattern11b, coord_string, re.IGNORECASE)
    if match:
        lat_deg = match.group(1)
        lat_min = match.group(2)
        lat_sec = match.group(3)
        lat_dir = match.group(4).upper()

        lon_deg = match.group(5)
        lon_min = match.group(6)
        lon_sec = match.group(7)
        lon_dir = match.group(8).upper()

        lat = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
        lon = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)

        return (lat, lon)

    # Format 12: DMS with fancy double quotes for seconds
    # Example: "N 44 48' 46.89''; E 20 30' 59.89''"
    pattern12 = r'([NS])\s+([0-9]+)\s+([0-9]+)[\'\´]\s*([0-9.,]+)[\'\´][\'\´]\s*;\s*([EW])\s+([0-9]+)\s+([0-9]+)[\'\´]\s*([0-9.,]+)[\'\´][\'\´]'
    match = re.search(pattern12, coord_string, re.IGNORECASE)
    if match:
        lat_dir = match.group(1).upper()
        lat_deg = match.group(2)
        lat_min = match.group(3)
        lat_sec = match.group(4).replace(',', '.')

        lon_dir = match.group(5).upper()
        lon_deg = match.group(6)
        lon_min = match.group(7)
        lon_sec = match.group(8).replace(',', '.')

        lat = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
        lon = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)

        return (lat, lon)

    # Format 13: DMS with straight quotes (no degree symbol)
    # Example: "N 45°47'16" E 19°05'54""
    pattern13 = r'([NS])\s+([0-9]+)°([0-9]+)[\'\´]([0-9]+)"?\s+([EW])\s+([0-9]+)°([0-9]+)[\'\´]([0-9]+)"?'
    match = re.search(pattern13, coord_string, re.IGNORECASE)
    if match:
        lat_dir = match.group(1).upper()
        lat_deg = match.group(2)
        lat_min = match.group(3)
        lat_sec = match.group(4)

        lon_dir = match.group(5).upper()
        lon_deg = match.group(6)
        lon_min = match.group(7)
        lon_sec = match.group(8)

        lat = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
        lon = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)

        return (lat, lon)

    # Format 14: DMS with dash separator
    # Example: "N 43 51 40,8 - E 21 24 26,5"
    pattern14 = r'([NS])\s+([0-9]+)\s+([0-9]+)\s+([0-9.,]+)\s*-\s*([EW])\s+([0-9]+)\s+([0-9]+)\s+([0-9.,]+)'
    match = re.search(pattern14, coord_string, re.IGNORECASE)
    if match:
        lat_dir = match.group(1).upper()
        lat_deg = match.group(2)
        lat_min = match.group(3)
        lat_sec = match.group(4).replace(',', '.')

        lon_dir = match.group(5).upper()
        lon_deg = match.group(6)
        lon_min = match.group(7)
        lon_sec = match.group(8).replace(',', '.')

        lat = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
        lon = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)

        return (lat, lon)

    # Format 15: Compressed format with space prefix
    # Example: "+ 454328+0201636"
    pattern15 = r'^\+?\s*([+-])([0-9]{2})([0-9]{2})([0-9]{2})([+-])([0-9]{3})([0-9]{2})([0-9]{2})$'
    match = re.search(pattern15, coord_string)
    if match:
        lat_sign = match.group(1)
        lat_deg = match.group(2)
        lat_min = match.group(3)
        lat_sec = match.group(4)

        lon_sign = match.group(5)
        lon_deg = match.group(6)
        lon_min = match.group(7)
        lon_sec = match.group(8)

        lat_dir = 'S' if lat_sign == '-' else 'N'
        lon_dir = 'W' if lon_sign == '-' else 'E'

        lat = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
        lon = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)

        return (lat, lon)

    # Format 16: Space-separated DMS without symbols (no semicolon)
    # Example: "N 45 16 49 E 020 16 55"
    pattern16 = r'([NS])\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([EW])\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)'
    match = re.search(pattern16, coord_string, re.IGNORECASE)
    if match:
        lat_dir = match.group(1).upper()
        lat_deg = match.group(2)
        lat_min = match.group(3)
        lat_sec = match.group(4)

        lon_dir = match.group(5).upper()
        lon_deg = match.group(6)
        lon_min = match.group(7)
        lon_sec = match.group(8)

        lat = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
        lon = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)

        return (lat, lon)

    # Format 17: Compressed format with space between coordinates
    # Example: "+433648 +0223011"
    pattern17 = r'([+-])([0-9]{2})([0-9]{2})([0-9]{2})\s+([+-])([0-9]{3})([0-9]{2})([0-9]{2})'
    match = re.search(pattern17, coord_string)
    if match:
        lat_sign = match.group(1)
        lat_deg = match.group(2)
        lat_min = match.group(3)
        lat_sec = match.group(4)

        lon_sign = match.group(5)
        lon_deg = match.group(6)
        lon_min = match.group(7)
        lon_sec = match.group(8)

        lat_dir = 'S' if lat_sign == '-' else 'N'
        lon_dir = 'W' if lon_sign == '-' else 'E'

        lat = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
        lon = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)

        return (lat, lon)

    # Format 18: Partial coordinates (only E given, assume N)
    # Example: "44.73323° E 21.57840°"
    pattern18 = r'^([0-9.]+)°?\s+([EW])\s*([0-9.]+)°?$'
    match = re.search(pattern18, coord_string, re.IGNORECASE)
    if match:
        lat = float(match.group(1))
        lon_dir = match.group(2).upper()
        lon = float(match.group(3))

        # Assume northern hemisphere for Serbia
        if lon_dir == 'W':
            lon = -lon

        return (lat, lon)

    return None

def format_coordinates(lat, lon):
    """Format coordinates as 'latitude, longitude' with 6 decimal places."""
    return f"{lat:.6f}, {lon:.6f}"

def convert_all_coordinates():
    """Convert all coordinates in the database to standard format."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all records with coordinates
    cursor.execute("""
        SELECT id, coordinates
        FROM bird_ringing
        WHERE coordinates IS NOT NULL AND coordinates != ''
    """)

    records = cursor.fetchall()
    print(f"Found {len(records):,} records with coordinates")
    print("=" * 80)

    successful = 0
    failed = 0
    already_standard = 0
    failed_records = []

    for record_id, original_coords in records:
        parsed = parse_coordinates(original_coords)

        if parsed:
            lat, lon = parsed
            standardized = format_coordinates(lat, lon)

            # Check if already in standard format
            if original_coords.strip() == standardized:
                already_standard += 1
                continue

            # Update the database
            cursor.execute("""
                UPDATE bird_ringing
                SET coordinates = ?
                WHERE id = ?
            """, (standardized, record_id))

            successful += 1

            if successful <= 10:  # Show first 10 conversions
                print(f"ID {record_id}:")
                print(f"  Original: {original_coords}")
                print(f"  Standardized: {standardized}")
                print()
        else:
            failed += 1
            failed_records.append((record_id, original_coords))

    # Commit changes
    conn.commit()

    print("=" * 80)
    print(f"Conversion complete!")
    print(f"  Successfully converted: {successful:,}")
    print(f"  Already in standard format: {already_standard:,}")
    print(f"  Failed to parse: {failed:,}")

    if failed_records and failed > 0:
        print("\nFailed to parse these coordinates:")
        for record_id, coords in failed_records[:20]:  # Show first 20 failures
            print(f"  ID {record_id}: '{coords}'")
        if failed > 20:
            print(f"  ... and {failed - 20} more")

    conn.close()

if __name__ == '__main__':
    print("Bird Ringing Coordinate Conversion")
    print("Converting coordinates to standard format: 'latitude, longitude'")
    print()

    convert_all_coordinates()
