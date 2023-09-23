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
    proportions = [(instrument / total_investment) for instrument in instrument_list]
    unadjusted_proportions = []
    temp = 0
    logging.info("My proportions :{}".format(proportions))
    for proportion in range(len(proportions)):
        if proportions[proportion] < 0.05:
            proportions[proportion] = 0.05
            temp += 1
        else:
            unadjusted_proportions.append(proportions[proportion])
    new_total = sum(unadjusted_proportions)
    final = []
    for proportion in unadjusted_proportions:
        final.append((proportion / new_total) * (1-temp*0.05))
    for i in range(temp):
        final.append(0.05)
    # Sort instruments based on proportions in descending order
    final = sorted(final, reverse=True)
    # Calculate angles for the boundaries of the slices/arcs of the pie chart
    angles = [0.0]
    cumulative_angle = 0.0
    for proportion in final:
        angle = proportion * 2 * math.pi
        cumulative_angle += angle
        angles.append(cumulative_angle)

    
    # Return the calculated angles
    return {"instruments": angles}