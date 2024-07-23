from ..exceptions.health_exception import ClaimException

def check_claim_dependents(policy, dependent):
    policy_premium = policy.policy_premium
    print('dependents: ', policy.dependents)
    if policy_premium and dependent:
        policy_type = policy_premium.policy.policy_type
        # if dependent not in policy.dependents:
        #     raise ClaimException('This dependent is not attached to this policy')
        
        if policy_type == 'Individual':
            if dependent.relation != 'Self':
                raise ClaimException('dependents: Individual policy can only have self as dependent.')

        elif policy_type == 'Family':
            if dependent.relation not in ['Self', 'Spouse', 'Child']:
                raise ClaimException('dependents: Family policy dependents must be self, spouse, 2 children.')

        elif policy_type == 'Senior':
            if dependent.relation != 'Parent':
                raise ClaimException(f'dependents: Senior Citizens policy dependents must be Parent.')


def validate_claim_insurance(policy, claim, prev_claim_amount):
    if policy.policy_premium.policy.sum_assurance <(claim.claim_amount+prev_claim_amount):
        raise ClaimException("claim amount is greater than balance")
    if policy.end_date < claim.claim_date:
        raise ClaimException("Policy is already expired")
    check_claim_dependents(policy, claim.dependent)