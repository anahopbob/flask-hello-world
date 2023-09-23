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
    instrument_list = [instrument["quantity"] * instrument["price"] for instrument in instruments]
    total_investment = sum(instrument_list)
    minimum_investment = total_investment * 0.05
    for instrument in range(len(instrument_list)):
        if instrument_list[instrument]["quantity"] * instrument_list[instrument]["price"] < minimum_investment:
            instrument_list[instrument]["quantity"] = minimum_investment
    total_investment = sum(instrument_list)
    proportions = [(instrument / total_investment) * 100 for instrument in instrument_list]
    
    # Sort instruments based on proportions in descending order
    proportions = sorted(proportions, reverse=True)
    # Calculate angles for the boundaries of the slices/arcs of the pie chart
    angles = [0.0]
    cumulative_angle = 0.0
    for proportion in proportions:
        angle = proportion * 2 * math.pi
        cumulative_angle += angle
        angles.append(cumulative_angle)

    
    # Return the calculated angles
    return {"instruments": angles}