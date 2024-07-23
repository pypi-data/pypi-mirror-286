class HealthPolicyException(Exception):
    def __init__(self, message="Details are not valid!"):
        self.message = message
        super().__init__(self.message)
        
class DependentException(Exception):
    def __init__(self, message="Dependent details invalid!"):
        self.message = message
        super().__init__(self.message)

class ClaimException(Exception):
    def __init__(self, message="Claim details invalid!"):
        self.message = message
        super().__init__(self.message)
