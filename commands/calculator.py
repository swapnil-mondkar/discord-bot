# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# calculator.py

import math

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
