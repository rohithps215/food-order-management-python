from datetime import date
import json

# Food Delivery Order Processor

# Step 1: Menu
menu = {
    "Burger": 120,
    "Pizza": 250,
    "Sandwich": 100,
    "Pasta": 180,
    "French Fries": 80,
    "Biryani": 200,
    "Shawarma": 150,
    "Fried Rice": 160
}

# Step 2: Sample Orders
orders = [
    {"order_id": 1, "customer": "Alex", "items": [{"name": "Burger", "quantity": 2}]},
    {"order_id": 2, "customer": "John", "items": [{"name": "Pizza", "quantity": 1}, {"name": "French Fries", "quantity": 2}]},
    {"order_id": 3, "customer": "Emma", "items": [{"name": "Sandwich", "quantity": 3}]},
    {"order_id": 4, "customer": "David", "items": [{"name": "Pasta", "quantity": 2}, {"name": "Burger", "quantity": 1}]},
    {"order_id": 5, "customer": "Sophia", "items": [{"name": "Biryani", "quantity": 2}]},
    {"order_id": 6, "customer": "Michael", "items": [{"name": "Shawarma", "quantity": 3}]},
    {"order_id": 7, "customer": "Olivia", "items": [{"name": "Fried Rice", "quantity": 2}, {"name": "Sandwich", "quantity": 1}]},
    {"order_id": 8, "customer": "James", "items": [{"name": "Pizza", "quantity": 2}]},
    {"order_id": 9, "customer": "Isabella", "items": [{"name": "Burger", "quantity": 1}, {"name": "Pasta", "quantity": 1}]},
    {"order_id": 10, "customer": "Daniel", "items": [{"name": "Biryani", "quantity": 1}, {"name": "Shawarma", "quantity": 2}]},
    # Invalid sample orders to demonstrate error handling
    {"order_id": 11, "customer": "Ryan", "items": []},
    {"order_id": 12, "customer": "Mia", "items": [{"name": "Tacos", "quantity": 2}]}
]

DISCOUNT_THRESHOLD = 500
DISCOUNT_RATE = 0.10
DELIVERY_CHARGE = 40


# Step 3: Calculate order total
def calculate_order_total(order):
    if not order.get("items"):
        print(f"Order {order['order_id']} is empty. Skipping order.")
        return None

    subtotal = 0

    for item in order["items"]:
        name = item.get("name")
        quantity = item.get("quantity", 0)

        if name not in menu:
            print(f"Order {order['order_id']}: Invalid menu item '{name}'.")
            return None

        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            print(f"Order {order['order_id']}: Invalid quantity for '{name}'.")
            return None

        subtotal += menu[name] * quantity

    return subtotal


# Step 4: Apply discount
def apply_discount(subtotal):
    if subtotal >= DISCOUNT_THRESHOLD:
        return subtotal * DISCOUNT_RATE
    return 0


# Step 5: Add delivery charge
def calculate_final_bill(subtotal):
    discount = apply_discount(subtotal)
    delivery = DELIVERY_CHARGE
    total = subtotal - discount + delivery

    return {
        "subtotal": subtotal,
        "discount": discount,
        "delivery_charge": delivery,
        "total": total
    }


# Step 6: Process all orders
def process_orders():
    processed_orders = []
    total_revenue = 0

    print("\n========== FOOD DELIVERY BILLS ==========\n")

    for order in orders:
        subtotal = calculate_order_total(order)

        if subtotal is None:
            continue

        bill = calculate_final_bill(subtotal)

        order_result = {
            "order_id": order["order_id"],
            "customer": order["customer"],
            "items": order["items"],
            "subtotal": round(bill["subtotal"], 2),
            "discount": round(bill["discount"], 2),
            "delivery_charge": round(bill["delivery_charge"], 2),
            "total": round(bill["total"], 2)
        }

        processed_orders.append(order_result)
        total_revenue += bill["total"]

        print(f"Order ID       : {order['order_id']}")
        print(f"Customer       : {order['customer']}")
        print(f"Subtotal       : Rs. {bill['subtotal']:.2f}")
        print(f"Discount       : Rs. {bill['discount']:.2f}")
        print(f"Delivery Charge: Rs. {bill['delivery_charge']:.2f}")
        print(f"Final Bill     : Rs. {bill['total']:.2f}")
        print("-" * 40)

    return processed_orders, total_revenue


# Step 7: Identify highest-value order
def find_highest_value_order(processed_orders):
    if not processed_orders:
        return None

    return max(processed_orders, key=lambda order: order["total"])


# Step 8: Save order data and sales report
def save_order_data(processed_orders):
    with open("sample_orders.json", "w", encoding="utf-8") as file:
        json.dump(orders, file, indent=4)

    with open("processed_orders.json", "w", encoding="utf-8") as file:
        json.dump(processed_orders, file, indent=4)


def generate_sales_report(processed_orders, total_revenue, highest_order):
    report = []
    report.append("DAILY FOOD DELIVERY SALES REPORT")
    report.append("=" * 40)
    report.append(f"Date: {date.today()}")
    report.append(f"Total orders received: {len(orders)}")
    report.append(f"Successfully processed orders: {len(processed_orders)}")
    report.append(f"Invalid or empty orders: {len(orders) - len(processed_orders)}")
    report.append(f"Total revenue: Rs. {total_revenue:.2f}")

    if highest_order:
        report.append("")
        report.append("HIGHEST-VALUE ORDER")
        report.append(f"Order ID: {highest_order['order_id']}")
        report.append(f"Customer: {highest_order['customer']}")
        report.append(f"Order Value: Rs. {highest_order['total']:.2f}")
    else:
        report.append("No valid orders were processed.")

    report.append("")
    report.append("ORDER DETAILS")
    report.append("-" * 40)

    for order in processed_orders:
        report.append(
            f"Order {order['order_id']} | "
            f"Customer: {order['customer']} | "
            f"Total: Rs. {order['total']:.2f}"
        )

    with open("sales_report.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(report))

    print("\n========== SALES SUMMARY ==========\n")
    print("\n".join(report))


# Step 9: Obstacle log
def create_obstacle_log():
    obstacles = """
FOOD DELIVERY ORDER PROCESSOR - OBSTACLE LOG
=============================================

1. Invalid Menu Items
   Problem: An order may contain an item that is not in the menu.
   Solution: Check each item against the menu and skip invalid orders.

2. Empty Orders
   Problem: An order may not contain any items.
   Solution: Check whether the items list is empty before processing.

3. Invalid Quantities
   Problem: Zero, negative, or non-integer quantities may occur.
   Solution: Validate quantities before calculating the subtotal.

4. Discount Calculation
   Problem: Discounts must be applied only when the subtotal
   reaches the specified threshold.
   Solution: Use a separate function to calculate the discount.

5. Sales Report
   Problem: Processed data and daily sales details must be saved.
   Solution: Write the order data to JSON files and the sales
   summary to a text file.
"""

    with open("obstacle_log.txt", "w", encoding="utf-8") as file:
        file.write(obstacles.strip())


# Main program
def main():
    processed_orders, total_revenue = process_orders()

    highest_order = find_highest_value_order(processed_orders)

    if highest_order:
        print("\n========== HIGHEST-VALUE ORDER ==========")
        print(f"Order ID: {highest_order['order_id']}")
        print(f"Customer: {highest_order['customer']}")
        print(f"Total: Rs. {highest_order['total']:.2f}")

    save_order_data(processed_orders)

    generate_sales_report(
        processed_orders,
        total_revenue,
        highest_order
    )

    create_obstacle_log()

    print("\nFiles generated successfully:")
    print("1. sample_orders.json")
    print("2. processed_orders.json")
    print("3. sales_report.txt")
    print("4. obstacle_log.txt")


if __name__ == "__main__":
    main()