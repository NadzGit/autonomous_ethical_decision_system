#Decision, Environment, NormalisedMetrics, SystemConfig

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Environment:
    weather_conditions: str # "sunny", "rainy", "snowy", "foggy", "stormy"
    population_density: float
    time_of_day: str # "day", "night", "dawn", "dusk"
    battery_level: float
    comms_reliability: float

    def __repr__(self):
        return (f"Environment(weather_conditions={self.weather_conditions},"
        f"population_density={self.population_density},"
        f"time_of_day={self.time_of_day},"
        f"battery_level={self.battery_level},"
        f"comms_reliability={self.comms_reliability})") 


@dataclass 
class NormalisedMetrics:
    weather_severity: float
    population_density: float
    time_of_day: float
    battery_level: float
    comms_reliability: float

    def calculate_mission_risk(self):
        weights = {
            "weather_severity": 0.1,
            "population_density": 0.35, # we value human life - if there are too many people paired with other risk factors, we should return
            "time_of_day": 0.15, 
            "battery_level": 0.2, 
            "comms_reliability": 0.2 # we want to be able to communicate with the drone at all times if possible, otherwise we should return
        }

        risk_score = (
           weights["weather_severity"] * self.weather_severity +
           weights["population_density"] * self.population_density +
           weights["time_of_day"] * self.time_of_day +
           weights["battery_level"] * self.battery_level +
           weights["comms_reliability"] * self.comms_reliability)

        # if danger < 0.30 --> Safe
        # if danger < 0.40 --> Moderate
        # if danger < 0.70 --> High
        # if danger < 0.80--> Very High

        return max(0.0, min(1.0, risk_score)) # lower bound is 0, upper bound is 1
    
    def calculate_data_confidence(self):
        return self.comms_reliability * self.battery_level * self.weather_severity 


@dataclass
class Decision:
    timestamp: datetime
    action: str # "return", "investigate", "monitor"
    reason: str # "low_battery", "high_risk", "low_confidence", "high_population", "low_comms"
    sensor_snapshot: Environment
    risk_score: float
    data_confidence: float
    
    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "action": self.action,
            "reason": self.reason,
            "risk_score": self.risk_score,
            "data_confidence": self.data_confidence,

            "sensors": {
                "weather": self.sensor_snapshot.weather_conditions,
                "population": self.sensor_snapshot.population_density,
                "time_of_day": self.sensor_snapshot.time_of_day,
                "battery_level": self.sensor_snapshot.battery_level,
                "comms_reliability": self.sensor_snapshot.comms_reliability
            }
        }
@dataclass
class MissionState:
    """Current state of the mission - combines environment data with calculated metrics"""
    environment: Environment
    normalised_metrics: NormalisedMetrics
    current_decision: Decision

