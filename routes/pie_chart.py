from typing import Dict, List, Tuple
import logging
import math
from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/pie-chart', methods=['POST'])
def solve_pie_chart():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    res: Dict[str, list[int]] = calculate_pie_chart_angles(data)

    logging.info("My result :{}".format(res))
    return res


def calculate_pie_chart_angles(data):
    part = data["part"]
    instruments = data["data"]
    
    # Calculate total investment in the portfolio
    total_investment = [instrument["quantity"] * instrument["price"] for instrument in instruments]
    print("TOTAL INVESTMENTS", total_investment)
    # Calculate proportions (percentages) of each instrument's investment relative to the total
    proportions = [(instrument["quantity"] * instrument["price"] / total_investment) * 100 for instrument in instruments]
    
    # Sort instruments based on proportions in descending order
    sorted_instruments = [instrument for _, instrument in sorted(zip(proportions, instruments), reverse=True)]
    minimum_investment = total_investment * 0.05
    for instrument in range(len(sorted_instruments)):
        if sorted_instruments[instrument]["quantity"] * sorted_instruments[instrument]["price"] < minimum_investment:
            sorted_instruments[instrument]["quantity"] = minimum_investment / sorted_instruments[instrument]["price"]
    # Calculate angles for the boundaries of the slices/arcs of the pie chart
    angles = [0.0]
    cumulative_angle = 0.0
    for instrument in sorted_instruments:
        proportion = (instrument["quantity"] * instrument["price"] / total_investment)
        angle = proportion * 2 * math.pi
        cumulative_angle += angle
        angles.append(cumulative_angle)
    
    # Ensure that angles meet the minimum angle constraint
    min_angle = 0.00314159
    for i in range(len(angles) - 1):
        if angles[i + 1] - angles[i] < min_angle:
            angles[i + 1] = angles[i] + min_angle
    
    # Return the calculated angles
    return {"instruments": angles}