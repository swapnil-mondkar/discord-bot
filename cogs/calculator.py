# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# calculator.py

import math
from datetime import datetime, timedelta
import calendar

def setup(bot):

    # Define the `/calculate` command
    @bot.command()
    async def calculate(ctx, *, expression: str):
        try:
            # Sanitize input (optional) to only allow safe characters (digits, operators, parentheses)
            allowed_chars = "0123456789+-*/(). "
            if any(char not in allowed_chars for char in expression):
                await ctx.send("⚠️ Invalid characters in the expression.")
                return

            # Evaluate the expression safely
            result = eval(expression, {"__builtins__": None}, {"math": math})

            # Send the result back to the user
            await ctx.send(f"The result of `{expression}` is: {result}")
        
        except Exception as e:
            # Catch errors like invalid expressions
            await ctx.send("⚠️ There was an error in the expression. Please check the syntax.")
            print(f"Error in calculation: {e}")

    # Define the `/date_difference` command
    @bot.command()
    async def date_difference(ctx, date1: str, date2: str):
        """Calculate the difference between two dates."""
        try:
            date1 = datetime.strptime(date1, "%Y-%m-%d")
            date2 = datetime.strptime(date2, "%Y-%m-%d")
            delta = abs((date2 - date1).days)
            await ctx.send(f"📅 Difference: {delta} days, {delta // 7} weeks, approximately {delta // 30} months.")
        except ValueError:
            await ctx.send("⚠️ Please provide dates in the format `YYYY-MM-DD`.")

    # Define the `/add_days` command
    @bot.command()
    async def add_days(ctx, base_date: str, days: int):
        """Add or subtract days from a given date."""
        try:
            base_date = datetime.strptime(base_date, "%Y-%m-%d")
            new_date = base_date + timedelta(days=days)
            await ctx.send(f"📅 New date: {new_date.strftime('%Y-%m-%d')}")
        except ValueError:
            await ctx.send("⚠️ Please provide the date in the format `YYYY-MM-DD`.")

    # Define the `/day_of_week` command
    @bot.command()
    async def day_of_week(ctx, date: str):
        """Find the day of the week for a given date."""
        try:
            date = datetime.strptime(date, "%Y-%m-%d")
            await ctx.send(f"📅 The day of the week for {date.strftime('%Y-%m-%d')} is {date.strftime('%A')}.")
        except ValueError:
            await ctx.send("⚠️ Please provide the date in the format `YYYY-MM-DD`.")

    # Define the `/age` command
    @bot.command()
    async def age(ctx, birthdate: str):
        """Calculate age based on the birthdate."""
        try:
            birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
            today = datetime.now()
            delta = today - birthdate
            years = delta.days // 365
            months = (delta.days % 365) // 30
            days = (delta.days % 365) % 30
            await ctx.send(f"🎂 Age: {years} years, {months} months, and {days} days.")
        except ValueError:
            await ctx.send("⚠️ Please provide the birthdate in the format `YYYY-MM-DD`.")

    # Define the `/generate_calendar` command
    @bot.command()
    async def generate_calendar(ctx, year: int, month: int):
        """Generate a calendar for a given month and year."""
        try:
            cal = calendar.TextCalendar().formatmonth(year, month)
            await ctx.send(f"📅 Here is the calendar for {month}/{year}:\n```\n{cal}\n```")
        except Exception as e:
            await ctx.send("⚠️ There was an error generating the calendar. Please check the input.")
            print(f"Error in calendar generation: {e}")
