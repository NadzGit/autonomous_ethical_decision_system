# Ethical rules + thresholds

from dataclasses import dataclass

@dataclass
class SystemConfig:
    # risk thresholds
    max_risk_threshold: float = 0.6 # return if risk > 0.6
    critical_risk_threshold: float = 0.8 # emergency landing if risk > 0.8
    safe_risk_threshold: float = 0.3 # safe if < 0.3

    # battery thresholds
    min_battery_before_return: float = 0.25 # return if battery < 0.25 
    battery_safety_margin: float = 0.1 # don't let the battery go below 0.1

    # decision timings
    decision_timing_interval_seconds: int = 10 # seconds between decisions
    log_interval_seconds: int = 60 # seconds between logs

    # communications
    comms_reliability_threshold: float = 0.5 # return if comms < 0.5
    comms_timeout_investigate_seconds: int = 30 # max 30 seconds of no comms before human investigation
    comms_timeout_return_seconds: int = 600 # max 10 minutes of no comms before return (10 mins allowed for investigation)

    #confidence
    data_confidence_threshold: float = 0.5 # return if confidence < 0.5
    data_confidence_timeout_seconds: int = 600 # max 10 minutes of low confidence before return
    min_overall_confidence: float = 0.5 # return if overall confidence < 0.5

    # logging
    log_file_path: str = "mission_log.txt"
    enable_verbose_logging: bool = True

    #helper methods
    def is_emergency(self, risk: float, battery: float) -> bool:
        """Check if this is an emergency situation"""
        return (risk > self.critical_risk_threshold or 
                battery < self.battery_safety_margin)
    def should_return_to_base(self, risk: float, battery: float, confidence: float, data_confidence: float) -> bool:
        """Check if we should return to base"""
        return (risk > self.max_risk_threshold or
                battery < self.min_battery_before_return or
                confidence < self.min_overall_confidence or
                data_confidence < self.data_confidence_threshold)
    
    def should_investigate(self, risk: float) -> bool:
        """Check if we should enter investigation mode"""
        return self.safe_risk_threshold < risk <= self.max_risk_threshold

    def get_action(self, risk: float, battery: float, confidence: float, data_confidence: float) -> str:
        """Determine what action the drone should take"""
        if self.is_emergency(risk, battery):
            return "EMERGENCY_LAND"
        
        if self.should_return_to_base(risk, battery, confidence, data_confidence):
            return "RETURN_TO_BASE"
        
        if self.should_investigate(risk):
            return "INVESTIGATE"
        
        return "CONTINUE"