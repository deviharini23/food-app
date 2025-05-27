def suggest_dish(order_text):
    order_text = order_text.lower()
    if "pizza" in order_text:
        return "You might like Margherita Pizza!"
    elif "burger" in order_text:
        return "Try our Double Cheeseburger!"
    elif "chicken" in order_text:
        return "Grilled Chicken sounds perfect!"
    return "How about trying today's special combo meal?"
