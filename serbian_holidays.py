#!/usr/bin/env python3
"""
Serbian Holidays and Non-Working Days Calculator
Includes fixed holidays, Orthodox Easter-based holidays, and weekend detection
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Tuple, Optional
import calendar

class SerbianHolidays:
    """Calculate Serbian holidays and non-working days."""
    
    # Fixed holidays (month, day)
    FIXED_HOLIDAYS = {
        (1, 1): "Нова година",
        (1, 2): "Нова година",
        (1, 7): "Божић (Orthodox Christmas)",
        (2, 15): "Дан државности",
        (2, 16): "Дан државности",
        (5, 1): "Празник рада",
        (5, 2): "Празник рада",
        (11, 11): "Дан примирја",
    }
    
    # Serbian month names
    MONTH_NAMES = {
        1: "Јануар", 2: "Фебруар", 3: "Март", 4: "Април",
        5: "Мај", 6: "Јун", 7: "Јул", 8: "Август",
        9: "Септембар", 10: "Октобар", 11: "Новембар", 12: "Децембар"
    }
    
    # Day names
    DAY_NAMES = {
        0: "Пон", 1: "Уто", 2: "Сре", 3: "Чет", 4: "Пет", 5: "Суб", 6: "Нед"
    }
    
    @staticmethod
    def calculate_orthodox_easter(year: int) -> date:
        """Calculate Orthodox Easter date using the Julian calendar method."""
        # Orthodox Easter calculation
        a = year % 4
        b = year % 7
        c = year % 19
        d = (19 * c + 15) % 30
        e = (2 * a + 4 * b - d + 34) % 7
        month = (d + e + 114) // 31
        day = ((d + e + 114) % 31) + 1
        
        # Convert from Julian to Gregorian calendar
        orthodox_easter = date(year, month, day)
        
        # Add 13 days for the difference between Julian and Gregorian calendars
        if year >= 1900:
            orthodox_easter += timedelta(days=13)
        
        return orthodox_easter
    
    @staticmethod
    def get_easter_based_holidays(year: int) -> Dict[date, str]:
        """Get holidays based on Orthodox Easter date."""
        easter = SerbianHolidays.calculate_orthodox_easter(year)
        
        return {
            easter - timedelta(days=2): "Велики петак (Good Friday)",
            easter - timedelta(days=1): "Велика субота (Holy Saturday)", 
            easter: "Васкрс (Orthodox Easter)",
            easter + timedelta(days=1): "Васкрсни понедељак (Easter Monday)",
        }
    
    @staticmethod
    def get_all_holidays(year: int) -> Dict[date, str]:
        """Get all holidays for a given year."""
        holidays = {}
        
        # Add fixed holidays
        for (month, day), name in SerbianHolidays.FIXED_HOLIDAYS.items():
            try:
                holiday_date = date(year, month, day)
                holidays[holiday_date] = name
            except ValueError:
                # Skip invalid dates (like Feb 29 in non-leap years)
                pass
        
        # Add Easter-based holidays
        holidays.update(SerbianHolidays.get_easter_based_holidays(year))
        
        return holidays
    
    @staticmethod
    def is_weekend(date_obj: date) -> bool:
        """Check if date is weekend (Saturday=5, Sunday=6)."""
        return date_obj.weekday() >= 5
    
    @staticmethod
    def is_holiday(date_obj: date) -> Optional[str]:
        """Check if date is a holiday and return holiday name."""
        holidays = SerbianHolidays.get_all_holidays(date_obj.year)
        return holidays.get(date_obj)
    
    @staticmethod
    def is_non_working_day(date_obj: date) -> Tuple[bool, str]:
        """Check if date is non-working (weekend or holiday) and return reason."""
        # Check if it's a weekend
        if SerbianHolidays.is_weekend(date_obj):
            day_name = SerbianHolidays.DAY_NAMES[date_obj.weekday()]
            return True, f"Викенд ({day_name})"
        
        # Check if it's a holiday
        holiday_name = SerbianHolidays.is_holiday(date_obj)
        if holiday_name:
            return True, holiday_name
        
        return False, ""
    
    @staticmethod
    def get_month_calendar_info(year: int, month: int) -> Dict[int, Dict[str, any]]:
        """
        Get detailed calendar information for a month.
        Returns dict with day number as key and info dict as value.
        """
        month_info = {}
        days_in_month = calendar.monthrange(year, month)[1]
        
        for day in range(1, days_in_month + 1):
            date_obj = date(year, month, day)
            is_non_working, reason = SerbianHolidays.is_non_working_day(date_obj)
            
            month_info[day] = {
                'date': date_obj,
                'weekday': date_obj.weekday(),
                'weekday_name': SerbianHolidays.DAY_NAMES[date_obj.weekday()],
                'is_weekend': SerbianHolidays.is_weekend(date_obj),
                'is_holiday': SerbianHolidays.is_holiday(date_obj) is not None,
                'holiday_name': SerbianHolidays.is_holiday(date_obj),
                'is_non_working': is_non_working,
                'non_working_reason': reason
            }
        
        return month_info
    
    @staticmethod
    def get_working_days_count(year: int, month: int) -> Tuple[int, int, int]:
        """
        Get count of working days, weekends, and holidays in a month.
        Returns (working_days, weekend_days, holiday_days)
        """
        month_info = SerbianHolidays.get_month_calendar_info(year, month)
        
        working_days = 0
        weekend_days = 0 
        holiday_days = 0
        
        for day_info in month_info.values():
            if day_info['is_holiday']:
                holiday_days += 1
            elif day_info['is_weekend']:
                weekend_days += 1
            else:
                working_days += 1
        
        return working_days, weekend_days, holiday_days

# Utility functions for the UI
def get_month_dropdown_values() -> List[Tuple[int, str]]:
    """Get month values for dropdown (number, name)."""
    return [(i, SerbianHolidays.MONTH_NAMES[i]) for i in range(1, 13)]

def get_year_dropdown_values() -> List[int]:
    """Get year values for dropdown (from 2010 to current year + 5)."""
    current_year = datetime.now().year
    return list(range(2010, current_year + 6))

def get_days_in_month(year: int, month: int) -> int:
    """Get number of days in a month."""
    return calendar.monthrange(year, month)[1]