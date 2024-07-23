from ..exceptions.health_exception import HealthPolicyException, ClaimException
def get_user_claims(policies, claims):
    user_claims = []
    for policy in policies:
        user_claims.extend(claims.objects.filter(policy=policy))
    return user_claims

def get_claims_amount_by_status(policies, claims, status):
    total_claim_amount = 0
    for policy in policies:
        for claim in claims.objects.filter(policy=policy, status=status):
            total_claim_amount+=claim.claim_amount
    return total_claim_amount

def get_user_policies(user, health_policies):
    return health_policies.objects.filter(user=user)

def get_dependents(user, dependents):
    return dependents.objects.filter(user=user)

def get_total_claim_amount(health_policies, claims):
    total_claim_amount = 0
    total_assurance = 0
    for policy in health_policies:
        total_assurance+=policy.policy_premium.policy.sum_assurance
        for claim in claims.objects.filter(policy=policy):
            total_claim_amount+=claim.claim_amount
    return total_claim_amount, total_assurance

def get_health_policy(health_policies, pk):
    try:
        return health_policies.objects.get(id=pk)
    except Exception as e:
        print('Unable to get healthpolicy: ', pk)
        raise HealthPolicyException("Policy not found by ID: ", pk)
    