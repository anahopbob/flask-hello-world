import json
import logging
from typing import List

from flask import request, Response

from routes import app

logger = logging.getLogger(__name__)

def findWeight(generation):
    digits = list(generation)
    return sum(int(digit) for digit in digits)

def calculateSignature(digit1, digit2):
    # Convert the digits to integers
    int_digit1 = int(digit1)
    int_digit2 = int(digit2)
    
    # Calculate the absolute difference between the digits
    diff = int_digit1 - int_digit2
    
    # Calculate the signature based on the rules
    if diff < 0:
        diff += 10
    
    return diff

def newColony(colony):
    weight = findWeight(colony)
    output = ""
    for i in range(len(colony) - 1):
        output += colony[i]
        signature = calculateSignature(colony[i], colony[i + 1])
        output += str((signature + weight) % 10)
    output += colony[-1]
    return output

def digitalColony(input):
    output = []
    for item in input:
        generations = item["generations"]
        colony = item["colony"]
        for count in range(generations):
            colony = newColony(colony)
        output.append(findWeight(colony))
    return output

@app.route('/digital-colony', methods=['POST'])
def evaluate_lazy_developer():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    res: List = digitalColony(data)

    logging.info("My result :{}".format(res))
    return json.dumps(res)
