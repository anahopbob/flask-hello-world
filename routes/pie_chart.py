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
    logging.info("My proportions :{}".format(proportions))
    checked = False
    while not checked:
        unadjusted_proportions = []
        temp = 0
        checked = True
        for proportion in range(len(proportions)):
            if proportions[proportion] < 0.0005:
                proportions[proportion] = 0.0005
                temp += 1
            else:
                unadjusted_proportions.append(proportions[proportion])
        new_total = sum(unadjusted_proportions)
        final = []
        for proportion in unadjusted_proportions:
            final.append((proportion / new_total) * (1-temp*0.0005))
        for i in range(temp):
            final.append(0.0005)
        proportions = final
        for i in range(len(proportions)):
            if proportions[i] < 0.0005:
                checked = False
    # Sort instruments based on proportions in descending order
    final = sorted(final, reverse=True)
    # Calculate angles for the boundaries of the slices/arcs of the pie chart
    logging.info("My final :{}".format(final))
    angles = [0.0]
    cumulative_angle = 0.0
    for proportion in final:
        angle = proportion * 2 * math.pi
        cumulative_angle += angle
        angles.append(cumulative_angle)

    
    # Return the calculated angles
    return {"instruments": angles}